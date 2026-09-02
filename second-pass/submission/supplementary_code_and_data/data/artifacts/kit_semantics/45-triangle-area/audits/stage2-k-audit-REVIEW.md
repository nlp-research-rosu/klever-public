# Independent adversarial review: 45-triangle-area

## Outcome

The candidate contains a legitimate, non-vacuous reachability proof of the
exact translated function body under the supplied MPY semantics. All four
symbolic Int/Float sort combinations close independently from a clean build,
the result is fixed rather than existential or tautological, and
`verification.k` adds no proof-local rule or oracle.

The result is not an unconditional theorem about every CPython numeric/control
edge. Its Float arithmetic is intentionally structural and conditional on
supplied opaque primitives. A fresh concrete witness also shows that MPY
finishes normally for an integer-to-float overflow input on which both Python
implementations raise `OverflowError`. In addition, an imported but
target-unreachable Float comparison rule mishandles NaN. Those fixed-semantics
limitations do not help close this target and do not substitute its body, but
they prevent a clean unconditional `PASS`.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, problem `45-triangle-area`, and the
expected candidate and reference mounts. The trusted
`/reference/reference-semantics` mount is present, as this mode requires.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, all six required small generation
records, `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured
trace. The trace contains one 205-line JSONL file, 41 tool calls and 41 tool
outputs. The raw generation records were treated only as claims; the output
shows several construction-time failures before its eventual reported
`#Top`.

Independent integrity results:

- The campaign-lock JSON object exactly equals the `audit_campaign` object in
  `/audit-input.json`.
- The lock SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the launcher-recorded value.
- Every launcher-required path is present, readable, of the expected regular
  file/directory kind, and not a symlink.
- All launcher-recorded hashes for the canonical, trusted prompt, translator,
  run/task/result/invocation records, metrics, runtime metrics, usage,
  generation prompt, last message, and raw output match freshly computed
  hashes.
- The only trace file hashes to
  `fffa06f6af71c5006a71c6a257a64adf68e91f0bd42412e4ddec768b23e72c5a`,
  matching both `generation-result.json` and `invocation.json`.
- Recursive path and byte comparison of the candidate and trusted
  `reference-semantics/` trees is exact. Candidate `prompt.py` and `py2mpy.py`
  are byte-identical to their trusted mounts. No candidate/reference/generation
  symlinks exist.
- A reviewer manifest independently hashes all 769 candidate files. Candidate
  compiled directories were inventoried but never copied or used.

Evidence:
[provenance checks](/audit-output/evidence/01-provenance.log),
[trace inventory](/audit-output/evidence/02-trace-inventory.log),
[supplied-tree comparison command](/audit-output/evidence/20-supplied-integrity.command),
[generation-output scan](/audit-output/evidence/21-generation-output-scan.log),
and [candidate file hashes](/audit-output/evidence/22-candidate-file-hashes.log).
There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks for `triangle_area(a, h)`: given a side length and
height, return the triangle's area; its example requires
`triangle_area(5, 3) == 7.5`. The trusted canonical implementation returns
`a * h / 2.0`.

Candidate `solution.py` is exactly:

```python
def triangle_area(a, h):
    return a * h / 2.0
```

Regeneration in scratch with the trusted translator produced a file
byte-identical to submitted `solution.mpy`; both have SHA-256
`bfcc62dbb7589f372bfcd3cef4475c6b6251f23d3113772b56061e9e7ca2c0c7`.
See [translation command](/audit-output/evidence/03-translate-identity.command)
and [result](/audit-output/evidence/03-translate-identity.log).

The independent [differential script](/audit-output/evidence/differential_audit.py)
loads the trusted canonical and generated entry points under distinct modules.
It checks the documented example, zero and signed-zero boundaries, positive
and negative values, all Int/Float combinations, subnormal/max/overflowing
floats, NaN and infinities, safe and overflowing large integers, plus
non-material Bool/Fraction/Decimal/complex/string and arity probes. There are no
source branches, so there are no branch thresholds to enumerate. All 29
outcomes, including return bit patterns and exception classes/arguments, match
([log](/audit-output/evidence/04-python-differential.log), exit 0).

The material contract interpretation is ordinary numeric side/height values,
represented by MPY `Int` and `Float`. The prompt contains no positivity or
finite-range restriction, and the claims impose none. Python values such as
complex numbers, strings, overloaded objects, and Booleans are not ordinary
geometric lengths; their omission is an intent interpretation, not a hidden
finite bound. Differential equivalence establishes program fidelity, not the K
theorem.

## 3. Clean proof reconstruction

Only candidate source proof files and trusted mounted sources were copied to
`/tmp/audit-work/45-triangle-area`. Candidate `runtime-kompiled/`,
`verification-kompiled/`, caches, traces, and binaries were excluded. The
reconstruction used K v7.1.293
([toolchain log](/audit-output/evidence/05-toolchain.log)).

Fresh concrete definition:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

It exited 0. The compiler reported supplied-semantics warnings about several
non-exhaustive total helpers; none is in this target's rule slice. Seven
ordinary/mixed cases and six additional rounding/large-safe cases translated
and ran to `.K`, `NoExc`, exit code 0:
[LLVM build](/audit-output/evidence/07-kompile-llvm.log),
[normal cases](/audit-output/evidence/08-krun-concrete-cases.log), and
[rounding cases](/audit-output/evidence/26-krun-concrete-rounding.log).

The separate huge-int program also reaches `.K`, `NoExc`, exit 0 under MPY
([log](/audit-output/evidence/09-krun-huge-int.log)); Stage 5 accounts for the
corresponding CPython discrepancy.

Fresh proof definition:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

It exited 0
([command](/audit-output/evidence/10-kompile-haskell.command),
[log](/audit-output/evidence/10-kompile-haskell.log)). Each positive claim was
then selected and run independently:

| Claim | Result |
|---|---|
| `SPEC.triangle-area-int-int` | exit 0, `#Top` |
| `SPEC.triangle-area-int-float` | exit 0, `#Top` |
| `SPEC.triangle-area-float-int` | exit 0, `#Top` |
| `SPEC.triangle-area-float-float` | exit 0, `#Top` |

Exact commands and outputs are in
[Int/Int](/audit-output/evidence/11-kprove-int-int.command),
[Int/Float](/audit-output/evidence/12-kprove-int-float.command),
[Float/Int](/audit-output/evidence/13-kprove-float-int.command), and
[Float/Float](/audit-output/evidence/14-kprove-float-float.command), with the
same-basename `.log` and `.status` files. Every log begins with `#Top`; every
status is 0.

## 4. Adequacy and real-program pinning

All four entry preconditions fix the complete default MPY state: module
environment 0, empty module scope with the supplied builtins parent, fresh
scope location 1, empty heap/location 0, empty stack, `noRet`, `NoExc`, and
exit code 0. They add only a sort constraint for each argument pair and have no
sign, magnitude, example, or finite-range guard.

Their plain-language postconditions are:

| Argument sorts | Postcondition |
|---|---|
| `Int, Int` | the exact opaque Python true-division term for `(A *Int H) / 2.0` |
| `Int, Float` | `intToF(A)` multiplied by `H`, then divided by `2.0` |
| `Float, Int` | `A` multiplied by `intToF(H)`, then divided by `2.0` |
| `Float, Float` | `A` multiplied by `H`, then divided by `2.0` |

Each postcondition consumes the entire computation and restores/constrains
every modeled state cell. No RHS-only result variable appears.

The [mechanical pinning check](/audit-output/evidence/program_pinning.py)
normalizes submitted/regenerated constructors and finds the entire exact
translated `Module(FuncDef(...))` under `#loadAll` exactly four times—once per
entry claim. The claim then calls the freshly installed `triangle_area`
binding. The submitted body is therefore the body executed by the theorem, not
an external source file or substituted summary
([result](/audit-output/evidence/15-program-pinning.log)).

Satisfying witnesses are `(5,3)`, `(3,2.5)`, `(2.5,4)`, and `(2.5,1.5)` for
the four claims. Both Python implementations return respectively `7.5`,
`3.75`, `5.0`, and `1.875`, and the freshly translated K assertions for those
same concrete primitive interpretations finish successfully.

A reviewer-authored body-sensitivity claim changes the *executed constructor
body* from divisor `2.0` to `3.0` while retaining the old `/2.0`
postcondition. It parses and executes to
`intFloatDiv(A *Int H, 3.0)`, then exits 1 with the expected unmet equality
against `/2.0`
([mutation](/audit-output/evidence/audit-body-mutation.k),
[log](/audit-output/evidence/24-fresh-body-mutation.log)).

## 5. Rule-by-rule static soundness review

The exhaustive [line-level inventory](/audit-output/evidence/16-k-inventory.log)
covers every supplied K source file, `verification.k`, and `spec.k`. It records
695 `rule` declarations, 227 syntax declarations, 149 function declarations,
110 `total` occurrences, 45 priority occurrences, 36 concrete occurrences, 25
symbols, 22 `no-evaluators` declarations, and four claims. There are no local
`functional` or `simplification` declarations.

The complete module-by-module decision record is
[RULE_REVIEW.md](/audit-output/evidence/RULE_REVIEW.md); all special attributes
are independently listed in
[23-special-k-attributes.log](/audit-output/evidence/23-special-k-attributes.log).
The target dependency slice is:

| Source construct | Fixed declarations/rules |
|---|---|
| module/definition | syntax `Module`, `FuncDef`, `Params`; `#loadAll`; statement sequencing; ordinary definition |
| call/binding | generic callee and left-to-right argument evaluation; ordinary closure frame; two parameter binds |
| expression order | `BinOp` `seqstrict(2,3)`; strict `Return`; `Name` lookup; `Float` literal |
| Int×Int product | `applyBin("*", Int, Int) => *Int` |
| true division | Int/Float dispatch to `intFloatDiv`; Float/Float dispatch to `divF` |
| mixed product | promotion through `intToF`, then `mulF` |
| return/state | return-to-`retV`, frame pop, restoration of all caller cells |

`verification.k` contributes no syntax, function, totality assertion, opaque
symbol, priority, operational rule, simplification, lemma, bridge, or auxiliary
claim. Thus there is no candidate-local rule that encodes the answer, skips the
body, fixes a binding without executing lookup, or fabricates a result.

The result-bearing supplied primitives are `intFloatDiv`, `intToF`, `mulF`,
and `divF`. They are fixed external arithmetic operations, not summaries of
program-defined code. The theorem is structural/interpretation-parametric:
ordinary execution produces those exact terms, and the postcondition repeats
the terms without adding a separate numerical equation. The LLVM concrete
rules and finite runs support their intended interpretation but are not a
universal Haskell connection theorem.

Two concrete model findings require qualification:

1. For `A = 2**1024, H = 1`, both trusted canonical and generated CPython
   functions raise `OverflowError`, while MPY finishes normally. This witnesses
   that an unconditional bridge from the all-`Int` K normal-completion claim to
   exact CPython exception behavior is false. It is target-reachable and is the
   main reason for `CONCERNS`. The result theorem remains legitimate as a
   partial-correctness theorem relative to the supplied primitive/exception
   model; it must not be reported as exact total CPython behavior.
2. Imported `float.k` defines `>=` as the negation of `<` and `<=` as the
   negation of `>`; with NaN, Python makes both ordered comparisons false while
   those negations are true. This is a false-rule witness for a comparison
   theorem. The submitted program contains no comparison, so this rule cannot
   fire or contribute to any target proof.

The fixed division rules also omit Python zero-division exceptions, but the
target denominator is always the nonzero literal `2.0`; there is no satisfying
target input that reaches the bad divisor. Other under-specified total helpers
and opaque sort/digest operations are target-unreachable. No target-path false
rewrite witness was found for the fixed divisor and ordinary finite Int/Float
inputs.

## 6. Fresh non-vacuity test

The candidate's mutation files were not accepted as evidence. I authored
[audit-false-mutation.k](/audit-output/evidence/audit-false-mutation.k), which
keeps the exact program and symbolic Int inputs but changes the required result
to Boolean `false`. `(A,H)=(5,3)` is a concrete satisfying witness and returns
the Float result `7.5`, so the mutation is meaningfully false.

Two preliminary ground-result variants caused the Haskell backend to call its
unsupported `Int2Float` hook. Those exits are preserved in
[17-fresh-false-mutation.log](/audit-output/evidence/17-fresh-false-mutation.log)
and
[18-fresh-false-mutation-valid.log](/audit-output/evidence/18-fresh-false-mutation-valid.log)
but are expressly rejected as non-vacuity evidence.

The final symbolic mutation:

```text
kprove audit-false-mutation.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-MUTATION
```

parses and executes successfully, reaches the real result
`intFloatDiv(A *Int H, 2.0) ~> .K`, then exits 1 with
`WarnStuckClaimState` because it does not unify with the false destination.
There is no parser error, missing import, timeout, or unrelated backend crash.
See the [exact command](/audit-output/evidence/19-fresh-false-mutation-symbolic.command)
and [residual](/audit-output/evidence/19-fresh-false-mutation-symbolic.log).
This establishes result discrimination.

## 7. Proven versus assumed accounting

What is formally established: under the supplied MPY theory, from the exact
initial state, loading the exact regenerated function and calling it on any of
the four symbolic Int/Float sort pairs executes definition, lookup, argument
order, binding, arithmetic dispatch, return, and frame restoration, and reaches
the exact result term stated in `spec.k`.

What is not established by `kprove`:

| Boundary | Dependents | Assessment |
|---|---|---|
| K parser/compiler/Haskell reachability implementation | all claims | ordinary trusted toolchain boundary; fresh failures show the proof is discriminating |
| supplied MPY operational semantics | all claims | benchmark-fixed semantics; target rules execute the body, but the documented exception/NaN limitations bar an unconditional CPython claim |
| `intFloatDiv` | Int×Int result | acceptable external primitive for the structural K theorem; numerical/exception interpretation is conditional |
| `intToF`, `mulF`, `divF` | mixed and Float×Float results | same; finite LLVM evidence, not universal proof |
| trusted `py2mpy.py` translation | source-to-constructor bridge | deterministic byte-identical regeneration plus exact constructor pinning |
| interpretation of “length” as ordinary Int/Float scalar | theorem domain | covers all material modeled numeric combinations without bounds; exotic Python numeric/object protocols are excluded |
| canonical/generated and LLVM tests | finite bridge evidence | useful evidence only; never substituted for the K proof |

The proof is not example-only, finitely unrolled, vacuous, or about a replaced
program. It does not materially narrow the ordinary Int/Float source-contract
domain. Its limitation is the explicit supplied-semantics trust boundary,
especially exact CPython exception behavior at extreme integer-to-float
conversion, plus an off-target imported NaN comparison defect. Those
limitations warrant `CONCERNS`, but because no such rule assists the target
proof and the theorem is honestly structural/conditional, they do not make the
candidate `NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
