# Independent adversarial review: 65-circular-shift

## Outcome

The candidate contains a legitimate full-input-domain partial-correctness proof
of the submitted program. I independently reconstructed both K definitions,
proved each positive claim, mechanically pinned the claimed closure to the
trusted regeneration of `solution.mpy`, exhaustively inventoried the source
rules, and obtained the expected failure from a fresh false-result mutation.
The proof covers every `X:Int` and `SHIFT:Int`; it is not a finite test proof or
a bounded unrolling.

I treated every candidate file and generation record as untrusted evidence.
All builds and mutations were made under
`/tmp/audit-work/65-circular-shift`; no candidate-built definition or cache was
used. Reviewer-authored sources and bounded logs are under
`/audit-output/evidence/`.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem `65-circular-shift`, and condition
`kit-semantics`. The trusted `/reference/reference-semantics` mount is present,
as this mode requires.

I read the launcher-owned audit input and every required pipeline-v3 record:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- the sole JSONL file recursively below
  `/generation-evidence/codex-trace/`.

The structured trace parsed as 412 JSON records. I used those records only to
check presence, structure, and provenance—not as evidence that the proof is
sound. The bounded trace inspection is in
[stage1-trace-summary.log](evidence/stage1-trace-summary.log).

The independent provenance checker established:

- the complete campaign block in `/audit-campaign-lock.json` is equal to the
  block in `/audit-input.json`;
- its SHA-256 is the declared
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`;
- every required path is present with the required regular-file or directory
  type, and no checked artifact is a symlink;
- every launcher-declared direct file hash matches the mounted bytes;
- the declared and mounted trace file sets are equal, and the JSONL file hash
  is the declared
  `2b56776124558ad24c99b236739944c59aeb4f9f4993abd08b510ed8b1ce7611`;
- candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts;
- candidate and trusted `reference-semantics/` have exactly the same 25
  recursive entries, entry types, relative paths, and file bytes. There are no
  missing, additional, changed, mistyped, or symlinked entries.

The full direct-hash and per-semantics-file results are preserved in
[stage1-provenance.log](evidence/stage1-provenance.log). I also recomputed the
pipeline-v3 aggregate hashes with the installed pipeline contract:

- candidate tree:
  `8a6bee8f5040d4d83ac651eff66e78894e44b092dfb06757a46f5f0f52dbdf04`;
- trusted supplied-semantics manifest:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- generation trace tree:
  `ed912542067df5e2de60adcc9123ec9f9bb7ec13aea39677e152ee7937df4237`.

Each equals the corresponding generation/task/usage record. The audit launcher
also records its separate snapshot-tree hashes; those values were read and are
reported without substituting the pipeline hash algorithm for the launcher's
snapshot algorithm. Independent path/type/file-digest comparison establishes
the mounted content. See
[check_pipeline_tree_hashes.py](evidence/check_pipeline_tree_hashes.py) and
[stage1-pipeline-tree-hashes.log](evidence/stage1-pipeline-tree-hashes.log).

Exact reviewer commands for this stage were:

```text
python3 /audit-output/evidence/provenance_check.py
python3 /audit-output/evidence/inspect_generation_trace.py
python3 /audit-output/evidence/check_pipeline_tree_hashes.py
```

All exited 0 and reported `PASS`. There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For integer `x` and integer `shift`, let `s = str(x)`. Return a string formed by
shifting the characters of `s` right by `shift`; if `shift > len(s)`, return
the reverse of `s`. The documented examples are `circular_shift(12, 1) ==
"21"` and `circular_shift(12, 2) == "12"`.

The trusted canonical program makes the non-reversal case precise as
`s[len(s)-shift:] + s[:len(s)-shift]`. Thus negative shifts are part of the
actual executable source contract: Python slice saturation makes that result
`s`. There is no empty-string input case because the decimal representation of
every integer is nonempty.

### Source and translation

The candidate computes:

```text
s[::-1]                                      if shift > len(s)
s                                             if shift < 0
(s + s)[len(s)-shift : 2*len(s)-shift]       otherwise
```

For `0 <= shift <= len(s)`, the doubled-string window has length `len(s)` and
is exactly the canonical suffix followed by the prefix. For negative shifts,
the explicit `s` agrees with the canonical saturated slices. This includes
zero, negative `x`, arbitrary-precision integers, zero shift, exactly
`len(s)`, and both sides of the reversal boundary.

Using only the trusted translator:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.mpy solution.regenerated.mpy
```

Both commands exited 0. Submitted and regenerated MPY bytes have SHA-256
`654c2263b953f11e3d3aa4ce7d78db41e1914ec4ef941d59154bbcd78d5d7d58`;
see [stage2-translation.log](evidence/stage2-translation.log).

### Independent differential test

The reviewer script
[stage2_differential.py](evidence/stage2_differential.py) imported the trusted
canonical function and the scratch copy of the generated function. It checked
77,193 distinct cases:

- both documented examples;
- 130 targeted boundary cases;
- 61,061 dense generated cases;
- 16,000 deterministic large and arbitrary-precision cases.

It found zero mismatches and exited 0:
[stage2-differential.log](evidence/stage2-differential.log). Differential
testing supports source equivalence but is not used as a substitute for the K
proof.

## 3. Clean proof reconstruction

I copied source artifacts—but no compiled definitions or caches—to scratch.
These were the exact reconstruction commands:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

krun solution.mpy --definition audit-runtime-kompiled
krun stage3-concrete-driver.mpy --definition audit-runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled

kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.circular-shift-reverse
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.circular-shift-negative
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.circular-shift-rotate
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC
```

Both `kompile` calls exited 0
([LLVM log](evidence/stage3-kompile-llvm.log),
[Haskell log](evidence/stage3-kompile-haskell.log)). The concrete source module
and a reviewer-generated 15-assertion boundary driver both completed with
`.K`, `NoExc`, and exit code 0
([solution run](evidence/stage3-krun-solution.log),
[driver source](evidence/stage3_concrete_driver.py),
[translated driver](evidence/stage3-concrete-driver.mpy),
[driver run](evidence/stage3-krun-concrete-driver.log)).

Every focused proof invocation exited 0 and printed `#Top`:

| Claim | Result |
|---|---|
| `SPEC.circular-shift-reverse` | `#Top`, exit 0 |
| `SPEC.circular-shift-negative` | `#Top`, exit 0 |
| `SPEC.circular-shift-rotate` | `#Top`, exit 0 |
| all claims together | `#Top`, exit 0 |

The corresponding logs are
[reverse](evidence/stage3-kprove-reverse.log),
[negative](evidence/stage3-kprove-negative.log),
[rotate](evidence/stage3-kprove-rotate.log), and
[combined](evidence/stage3-kprove-all.log).

Compiler warnings identify several non-exhaustive `total` declarations in the
supplied semantics and unused pattern variables. Static review confirmed that
the warned partial functions are unreachable from this program. The warnings
did not replace or suppress any proof obligation.

## 4. Adequacy and real-program pinning

### Claims in plain language

All three claims start in the same concrete clean state: environment 0;
`circular_shift` bound to `circularShiftClosure`; fixed builtins at scope -1;
next scope location 1; empty heap and stack; no pending return or exception;
exit code 0. They execute
`Call(Name("circular_shift"), (X, SHIFT, .Exprs))` and require the final
`<k>` value to be `circularShiftResult(X, SHIFT)`, while restoring every named
state cell.

Let `n = len(str(X))`.

1. Reverse claim: precondition `SHIFT > n`; postcondition is the reverse of the
   decimal character sequence.
2. Negative claim: precondition `not(SHIFT > n) and SHIFT < 0`; postcondition is
   the unchanged decimal string.
3. Rotation claim: precondition `not(SHIFT > n) and not(SHIFT < 0)`, hence
   `0 <= SHIFT <= n`; postcondition is the `n`-character window beginning at
   `n-SHIFT` in the doubled decimal string.

The guards are pairwise disjoint and exhaustive for all integer pairs. The
return is constrained to an exact `Str` term, not a free variable, implication,
or unconstrained oracle.

Each precondition is satisfiable. Concrete witnesses are:

| Branch | Input | Required and Python result |
|---|---|---|
| reverse | `(12, 3)` | `"21"` |
| negative | `(12, -1)` | `"12"` |
| rotation | `(12, 1)` | `"21"` |

The reviewer ground K claims reduced to `#Top`, exit 0
([claim source](evidence/stage4-ground-witnesses.k),
[proof log](evidence/stage4-kprove-ground-witnesses.log)); both trusted
canonical and candidate Python functions returned the same values
([Python log](evidence/stage4-python-witnesses.log)).

### Mechanical constructor-level pinning

`circularShiftClosure` is a definitional name, not an execution rule. To avoid
trusting the hand-written correspondence, the reviewer generator parsed the
trusted-regenerated `solution.mpy` as one top-level `FuncDef`, extracted its
parameters and complete constructor-balanced body, and emitted an equality
claim against `circularShiftClosure`:
[generator](evidence/generate_pinning_claim.py),
[generated claim](evidence/stage4-generated-pinning.k), and
[generation log](evidence/stage4-pinning-generation.log).

The command

```text
kprove audit-pinning.k --definition audit-verification-kompiled \
  --spec-module AUDIT-PINNING
```

exited 0 and printed `#Top`
([stage4-kprove-pinning.log](evidence/stage4-kprove-pinning.log)). The
`WarnTrivialClaim` is expected here: after the permitted expression-list
normalization, this test is constructor identity.

As an independent sensitivity check, I changed the function body actually
bound in the claim state to `s = str(x); return s`, but retained the original
postcondition for `(12, 1)`. The proof reached actual `"12"` while requiring
`"21"`, emitted `WarnStuckClaimState`, and exited 1:
[mutation](evidence/stage4-body-sensitivity.k) and
[log](evidence/stage4-kprove-body-sensitivity.log). This changes the executed
program term itself and shows that the theorem depends on the submitted body.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer inventory covers all 25 K source files in the fresh proof build:
the supplied `semantics.k`, its 23 helper files, and `verification.k`. Each of
the 1,074 outer sentences has a source range, normalized text, hash, flags, and
static disposition in
[stage5-rule-inventory.json](evidence/stage5-rule-inventory.json), with a
readable exhaustive rendering in
[stage5-rule-inventory.md](evidence/stage5-rule-inventory.md).

The inventory contains:

| Sentence class or flag | Count |
|---|---:|
| ordinary semantic rules | 654 |
| priority rules | 45 |
| function declarations | 147 |
| declarations carrying `total` | 109 |
| declarations carrying `functional` | 0 |
| other syntax declarations | 82 |
| configurations | 1 |
| contexts | 5 |
| simplification rules | 1 |
| explicit `no-evaluators` symbols | 22 |
| `owise` rules | 26 |
| macros | 3 |
| strict/seqstrict declarations | 2 / 1 |

The inventory command exited 0 and reported `K_INVENTORY: PASS`
([build script](evidence/build_k_inventory.py),
[log](evidence/stage5-inventory-build.log)).

Every entry has an explicit disposition: 157 conservatively reachable supplied
entries were reviewed on the used path; 907 supplied entries are both
byte-identical to the fixed semantics and unreachable from this constructor
path; and all ten proof-module entries were reviewed individually. The
detailed review is
[stage5-static-review.md](evidence/stage5-static-review.md).

### Coverage of the submitted program

`solution.mpy` uses exactly `Assign`, `BinOp`, `Call`, `CmpOp`, `Compare`,
`FuncDef`, `IfExp`, `Int`, `Module`, `Name`, `NoBound`, `Params`, `Return`,
`Slice`, `Subscript`, and `UnaryOp`. The used-path matrix maps these to:

- `core.k` for configuration, module sequencing, expression-list order,
  lexical lookup, and value sequences;
- `functions.k` and `call.k` for closure binding, left-to-right argument
  evaluation, real frame allocation, parameter binding, return, deallocation,
  and caller restoration;
- `controls.k` for assignment and conditional control;
- `int.k` and `operators.k` for exact unbounded integer arithmetic and
  comparisons;
- `builtins.k` and `str.k` for `str`, `len`, string representation, and
  concatenation;
- `subscript.k` for bound evaluation, Python-style adjustment/clamping, and
  structural slicing.

The execution rules evaluate the real function body and every material
operation. No rule intercepts `circular_shift`, replaces a call with its
answer, skips a state transition, or fabricates the return value.

### Proof-local rules

There are only these substantive proof-local additions:

1. `circularShiftClosure` has one equation whose RHS is the exact submitted
   closure constructor. It is a name only and cannot rewrite a `Call` or
   operational state.
2. `circularShiftResult` has three complementary equations. It occurs only in
   the postcondition and never on an execution-rule left-hand side. The reverse
   equation enumerates indices `n-1` through `0`; the negative equation is
   unchanged `s`; and the rotation equation selects indices `n-shift` through
   `2n-shift-1` from `s+s`. Those are the intended results under their
   respective guards.
3. `#Ceil(strToCodes(Int2String(X))) => #Top [simplification]` states only
   definedness. The fixed K hook declares `Int2String` total and implements
   arbitrary-precision integer conversion using a decimal string; all possible
   output characters are ASCII digits or `-`, which lie in the domain of the
   supplied `strToCodes`. Hook documentation, implementation, and boundary
   observations are preserved in
   [stage5-int2string-hook.log](evidence/stage5-int2string-hook.log).

The three result guards are `B`, `not B and C`, and `not B and not C`, where
`B` is `shift > n` and `C` is `shift < 0`. They are disjoint and exhaustive.
All recursion used in their RHSs is over a finite character sequence or moves
a slice index monotonically to its stop.

I also removed only the `#Ceil` rule, rebuilt a new Haskell definition from
source, and reproved all three target claims together. Compilation exited 0;
the proof exited 0 and printed `#Top`
([modified verification](evidence/stage5-verification-no-ceil.k),
[compile log](evidence/stage5-no-ceil-kompile.log),
[proof log](evidence/stage5-no-ceil-kprove-all.log)). Thus this true
definedness fact is not secretly carrying the result proof.

The 22 supplied `no-evaluators` symbols cover MD5, float/conversion, and sort
summaries. None appears in the submitted module, postcondition, or reachable
call path. All 45 priority rules belong to the supplied semantics; none is
proof-local or task-specific. Compiler-warned incomplete totals
(`mapStrVS`, float helpers, `joinCodes`, and `valSeqAt`) are likewise
unreachable; string slicing here uses `buildIS`/`intSeqAt`.

No inventoried rule is unsound on the intended domain. Accordingly there is no
false-conclusion witness to report for an unsound rule: no rule was assigned
that classification. The result is encoded only as the exact postcondition,
while the fixed operational rules independently execute the body to reach it.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh mutation executes
the actual submitted closure at satisfying rotation input `X=100, SHIFT=1`,
but changes the destination from the true `"010"` to the false unchanged
string `"100"`:
[stage6-false-result.k](evidence/stage6-false-result.k).

The falsity witness is direct: both Python implementations return `"010"` and
the rotation precondition holds
([stage6_false_witness.py](evidence/stage6_false_witness.py),
[stage6-python-witness.log](evidence/stage6-python-witness.log)).

The commands were:

```text
kprove audit-false-result.k --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT --dry-run
kprove audit-false-result.k --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT
```

The dry run exited 0 and emitted the valid `kore-exec` proof command
([dry-run log](evidence/stage6-kprove-dry-run.log)), excluding a parse/import
failure. The real proof exited 1 with `WarnStuckClaimState`; its final `<k>`
contains character codes `48,49,48` (`"010"`) and cannot unify with the false
destination ([failure log](evidence/stage6-kprove-false-result.log)). This is
the expected unmet result obligation, so the positive proof is non-vacuous.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

For every K `Int` pair `(X, SHIFT)`, from the explicitly stated clean state in
which `circular_shift` is bound to the exact trusted-regenerated function body,
the supplied MPY operational semantics executes the call and reaches the exact
string `circularShiftResult(X, SHIFT)`, with the caller cells restored and no
exception or nonzero exit. The three claims partition all integer inputs.

The result definition is extensionally:

- `reverse(str(X))` when `SHIFT > len(str(X))`;
- `str(X)` when that guard is false and `SHIFT < 0`;
- the right rotation by `SHIFT` otherwise.

For the third branch, its precondition implies `0 <= SHIFT <= len(str(X))`, and
the selected doubled-string interval has exactly the canonical suffix and
prefix. Therefore this is the source contract for the entire intended integer
domain, including canonical negative-shift behavior. This is a
partial-correctness reachability result; it does not claim resource bounds or
facts about Python values outside the modeled integer parameter domain.

### Trust and assumption ledger

| Boundary | Accounting | Judgment |
|---|---|---|
| K parser/compiler, LLVM concrete backend, Haskell proof backend, and core K hooks | Toolchain trust required by any K proof; both backends were rebuilt from source and positive/negative behavior was observed independently. | Acceptable low-level trust boundary. |
| Trusted `py2mpy.py` | Its output is the language term under proof. Regeneration was byte-identical, and constructor pinning used that regenerated term. | Acceptable trusted translation boundary designated by the benchmark. |
| Supplied MPY semantics | Candidate copy is recursively byte-identical to the trusted mount. Every sentence is inventoried; used control, state, call, integer, string, and slice paths were statically reviewed and concretely exercised. | Acceptable fixed-semantics boundary. |
| `Int2String` builtin hook | Supplies arbitrary-precision decimal conversion. Documentation/implementation and representative boundaries agree; its characters make `strToCodes` defined. | Acceptable primitive boundary; no task answer is supplied. |
| Fixed sequence/slice helpers (`strToCodes`, `isLen`, `seqConcat`, `slAdjust`, `buildIS`, `intSeqAt`) | Their structural equations and termination/guard coverage were reviewed on the used domain. | Proven/reduced within fixed semantics except for ordinary builtin arithmetic/string hooks. |
| Proof-local `#Ceil` rule | True definedness only; no value equation. All target claims reprove after removing it. | Acceptable and empirically unnecessary. |
| Proof-local closure and result functions | Closure is mechanically identical to regenerated MPY. Result is a constraining postcondition with disjoint/exhaustive equations; neither intercepts execution. | Legitimate definitions, not assumptions of correctness. |
| Mathematical bridge to the English/canonical contract | Finite-sequence identity: reverse indices are `n-1..0`; negative slices saturate to `s`; doubled-window indices yield suffix then prefix. | Ordinary mathematics, fully stated and non-material as a trust gap. |
| Differential/concrete tests | 77,193 Python pairs plus K boundary executions. | Corroboration only; not counted as the symbolic proof. |
| Supplied opaque summaries | Twenty-two inventoried symbols, all unreachable. | Not part of this theorem's trust boundary. |

There is no empirical bridge that chooses a return value, no assumed loop
invariant, no proof-local opaque function, no circular helper claim, no
task-answer semantic rule, and no narrowing to examples or fixed sizes.

## Decision

All seven gates pass. The reconstructed proof is sound on the entire intended
integer domain, constrains the returned value, pins the real regenerated
program, uses the supplied semantics without modification, and fails a fresh
meaningful false result. The remaining assumptions are the ordinary and
explicit low-level trust boundaries of the fixed K toolchain/semantics, not a
material adequacy limitation.

VERDICT: PASS
LEGITIMACY: LEGIT
