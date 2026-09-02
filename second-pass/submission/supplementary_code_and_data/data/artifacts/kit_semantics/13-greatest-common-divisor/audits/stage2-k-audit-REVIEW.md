# Independent adversarial audit: 13-greatest-common-divisor

## Executive decision

The candidate contains a legitimate partial-correctness proof of its real
generated program. Fresh builds close both compositional claims, the claims
execute the constructor-identical submitted body under the supplied semantics,
the result is constrained to a guarded and mathematically sound Euclidean
summary, and fresh false-result and body mutations are rejected for the
expected reasons.

The verdict is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, for one
contract-level ambiguity. The prompt says “a greatest common divisor of two
integers” with no positivity restriction. The candidate proves and implements
the conventional non-negative gcd on all integers. The trusted canonical
returns a negative associate when its final `a` is negative (for example,
`canonical(0,-7) == -7`, while the candidate, `math.gcd`, and the K theorem
return `7`). This does not narrow the source-contract domain and does not make
the K theorem false, but it is a material behavioral conflict between two
trusted intent signals. In addition, the bridge from the Euclidean recurrence
to the English “greatest common divisor” property is ordinary mathematical
reasoning rather than a separate K theorem.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, and a mounted trusted semantics tree.
That is internally consistent with the rendered audit condition.

I independently checked the launcher records with
[`evidence/stage1_integrity.py`](evidence/stage1_integrity.py); the exact
command is in [`evidence/stage1-command.txt`](evidence/stage1-command.txt) and
the bounded output is in
[`evidence/stage1-integrity.log`](evidence/stage1-integrity.log).
The command exited 0.

Results:

- `/audit-campaign-lock.json` is a regular file, exactly equals the
  `audit_campaign` object, and has the recorded SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt` are present,
  readable, non-symlink regular files. Every recorded file hash matches.
- The structured trace contains one regular JSONL file and no symlink or
  special entry. All 456 records parse. Its individual file hash matches the
  generation result, and the independently reconstructed pipeline tree hash
  `8a542d...` matches `usage.json`.
- The mounted candidate tree has independently reconstructed pipeline digest
  `5589ecdf...`, exactly the `workspace_sha256` in both the generation result
  and invocation. This confirms that the mounted workspace is the recorded
  generated workspace; candidate-provided compiled outputs were not trusted
  or reused.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts, with the recorded hashes.
- The candidate and trusted `reference-semantics/` trees contain the same 25
  directory/file entries and identical bytes for every file. There are no
  missing, added, changed, mistyped, or symlinked entries. The independent
  per-file hashes are recorded in the stage-1 log.
- The campaign/generation prose, logs, trace, prior `#Top`, and `PROOF.md`
  were treated only as untrusted historical claims.

No infrastructure breach or candidate provenance defect was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt declares:

```text
greatest_common_divisor(a: int, b: int) -> int
Return a greatest common divisor of two integers a and b.
Examples: (3,5) -> 1 and (25,15) -> 5.
```

The trusted canonical repeatedly assigns `(a,b) = (b,a % b)` while `b` is
truthy and returns `a`. The generated solution uses the same recurrence with
three scalar assignments and returns `abs(a)`.

Using the trusted translator:

```text
python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/candidate/solution.py > /tmp/audit-work/candidate/solution.regenerated.mpy
cmp -s /tmp/audit-work/candidate/solution.regenerated.mpy /tmp/audit-work/candidate/solution.mpy
```

Both commands exited 0. The regenerated and submitted files are byte-identical
and share SHA-256
`61e6b834270cacb40cb008270471d85e98b6495e67b8718c573b65dd53463dc6`.
Commands and results are in
[`evidence/stage2-commands.txt`](evidence/stage2-commands.txt) and
[`evidence/stage2-translation.log`](evidence/stage2-translation.log).

### Independent differential test

[`evidence/differential_gcd.py`](evidence/differential_gcd.py) independently
imports both trusted canonical and generated entry points. It covers the two
examples, `(0,0)`, both zero axes, sign quadrants, `b = 0, ±1`, equal and
coprime values, large integers, booleans, all 6,561 pairs in `[-40,40]^2`,
5,000 seeded signed 30-digit pairs, and missing-argument behavior.

The command intentionally exits nonzero on any canonical/generated mismatch.
It exited 1 with:

```text
total_cases=11578
canonical_generated_mismatches=5775
canonical_math_mismatches=5775
generated_math_mismatches=0
```

The mismatches are all the sign distinction described above; representative
cases and the exact exit are in
[`evidence/stage2-differential.log`](evidence/stage2-differential.log).
Both implementations reject missing arguments with `TypeError`.

Judgment: this is material evidence, but not evidence of an incorrect
generated gcd. On the prompt’s unrestricted integer wording, the candidate
returns the standard non-negative greatest common divisor and the canonical
returns a negative associate on part of that domain. I therefore retain this
as a non-fatal contract concern, not a domain-narrowing failure.

## 3. Clean proof reconstruction

All candidate kompiled directories and caches were ignored. Source artifacts
were copied to `/tmp/audit-work/candidate`, and both definitions were built
fresh with K v7.1.293. Exact commands are in
[`evidence/stage3-commands.txt`](evidence/stage3-commands.txt).

Concrete definition:

```text
kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled-audit
```

Exit 0. A fresh `krun concrete.mpy --definition runtime-kompiled-audit`
exited 0 with empty `<k>`, `NoExc`, exit code 0, and results `1`, `5`, `7`,
and `0` for `(3,5)`, `(25,15)`, `(0,-7)`, and `(0,0)`.
See [`evidence/stage3-kompile-llvm.log`](evidence/stage3-kompile-llvm.log) and
[`evidence/stage3-krun-concrete.log`](evidence/stage3-krun-concrete.log).

Proof definition:

```text
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled-audit
```

Exit 0. Every positive target was then run independently:

```text
kprove spec.k --definition verification-kompiled-audit --spec-module SPEC --claims SPEC.gcd-loop
kprove spec.k --definition verification-kompiled-audit --spec-module SPEC --claims SPEC.gcd-entry
kprove spec.k --definition verification-kompiled-audit --spec-module SPEC
```

Each command printed `#Top` and exited 0. Logs:

- [`evidence/stage3-kprove-gcd-loop.log`](evidence/stage3-kprove-gcd-loop.log)
- [`evidence/stage3-kprove-gcd-entry.log`](evidence/stage3-kprove-gcd-entry.log)
- [`evidence/stage3-kprove-all.log`](evidence/stage3-kprove-all.log)

The compile warnings concern unused variables or non-exhaustive fixed helpers
for unrelated string/float/subscript constructs; none occurs in this program
or its claims.

## 4. Adequacy and real-program pinning

### Claims in plain language

`gcd-entry` has no restriction on the mathematical integers `A,B`. Its state
is the exact post-module environment: env 0, a global scope containing the
`greatest_common_divisor` closure, builtins at -1, next scope 1, and empty
heap/stack with no return, exception, or nonzero exit. It proves that calling
the closure evaluates the docstring and `remainder = 0`, allocates local scope
1, binds `a=A,b=B,remainder=0`, pushes the caller frame, and reaches the exact
internal while-head plus return continuation.

`gcd-loop` starts at that while-head for arbitrary integer locals `A,B` and an
irrelevant prior remainder. It requires an exact plain frame and that the
global map does not shadow `abs`. It proves execution reaches
`gcdEuclid(A,B) ~> CONT`, restores env 0, removes local scope/frame, resets the
scope allocator, and preserves the empty heap, no exception, and exit code 0.

### Mechanical identity and composition

[`evidence/stage4_pinning.py`](evidence/stage4_pinning.py) performs a
constructor-level comparison, not a source filename comparison. It checks the
trusted regenerated `FuncDef` signature/body against both closure occurrences
in `spec.k`, and compares `gcd-entry`’s target `<k>` term with `gcd-loop`’s
source. It exited 0 with:

```text
closure_occurrences=2
closure_body_matches=[True, True]
entry_target_loop_source_control_exact_match=True
composition_cell_unifier=GLOBALS:<entry global map>,_R:0,CONT:.K
```

The exact output and concrete substitutions are in
[`evidence/stage4-pinning-witness.log`](evidence/stage4-pinning-witness.log).
Thus reachability transitivity composes the two independently proved claims;
the entry result is not free or tautological.

Fresh concrete execution of the submitted `solution.mpy` reaches the exact
function binding used by the claim; see
[`evidence/stage4-krun-solution.log`](evidence/stage4-krun-solution.log).
Omitting module initialization from the claim is therefore a demonstrated
semantically inert proof setup, not a substituted body.

Satisfiable witness: `A=25, B=15`, actual module global map, `_R=0`,
`CONT=.K`. The K summary, generated Python, trusted canonical, and `math.gcd`
all give 5. For the additional satisfying witness `A=0,B=-7`, the K summary
and generated Python give 7, the canonical gives -7, and `math.gcd` gives 7.

## 5. Rule-by-rule static soundness review

The exhaustive inventory and the per-entry review are:

- [`evidence/k-rule-inventory.md`](evidence/k-rule-inventory.md)
- [`evidence/k-rule-inventory.json`](evidence/k-rule-inventory.json)
- [`evidence/stage5-static-review.md`](evidence/stage5-static-review.md)

Inventory SHA-256:
`ec054996094f700acd4a31dd662b7d92f38554e1e8787984f313e5a1a6175b83`.
It contains 228 syntax declarations, one configuration, five contexts, 697
rules, and two claims. It records every source location, attributes, role,
normalized text, and stable ID.

The 695 fixed rules are the exact trusted supplied semantics. Every source
file was reviewed. The static review maps all program constructs and reachable
internal terms through module loading, closure selection, left-to-right
evaluation, local assignment, guard evaluation, Python modulo, loop control,
calls, builtin lookup, return, and frame cleanup. Rules outside that slice
require constructors absent from this Int-only program and cannot affect its
claims. All 22 opaque fixed symbols are float, sort, or MD5 operations and are
unreachable/result-irrelevant here. Relevant priority/`owise` overlaps are
guard- or sort-disjoint.

The complete proof-local extension inventory is:

1. `gcdEuclid(Int,Int) [function,total]`: definitional summary; never an
   operational `<k>` bridge.
2. `gcdEuclid(A,0) => absInt(A) [simplification]`: correct base case.
3. `gcdEuclid(A,B) => gcdEuclid(B,pyMod(A,B))` when `B != 0`: correct Euclidean
   recurrence.

The guards are disjoint and cover all integer second arguments. For nonzero
`B`, `pyMod(A,B)` has strictly smaller absolute magnitude and preserves the
set of common divisors, so recursion is well-founded and the equations define
the non-negative gcd. There is no local ordinary rewrite, priority rule,
opaque symbol, operational bridge, result oracle, task-answer rule, or
fabricated execution. No unsound rule or false-conclusion witness was found.

## 6. Fresh non-vacuity and body-sensitivity tests

I did not rely on the candidate’s mutation report. I authored
[`evidence/audit-spec-vacuity.k`](evidence/audit-spec-vacuity.k), changing the
result obligation to `gcdEuclid(A,B) +Int 2`. Witness
`A=25,B=15,GLOBALS=.Map,_R=0,CONT=.K` satisfies the source and would require
7 instead of 5.

```text
kprove audit-spec-vacuity.k --definition verification-kompiled-audit --spec-module AUDIT-SPEC-VACUITY --dry-run
```

Exit 0, proving the mutation parsed and built. The same command without
`--dry-run` exited 1 with `WarnStuckClaimState` and the unmet implication
`absInt(A) +Int 2 = absInt(A)`. See
[`evidence/stage6-vacuity-dry-run.log`](evidence/stage6-vacuity-dry-run.log)
and [`evidence/stage6-vacuity-proof.log`](evidence/stage6-vacuity-proof.log).
This is the expected semantic rejection, not a parser/import/tool failure.

I also authored a terminating body mutation,
[`evidence/audit-spec-body-sensitivity.k`](evidence/audit-spec-body-sensitivity.k),
which changes the actually executed assignment `remainder = a % b` to
`remainder = 0`. At `(25,15)` it returns 15 instead of 5. Its dry run exited 0,
and its proof exited 1 with `WarnStuckClaimState` and the expected residual
comparing `absInt(B)` to the Euclidean recurrence. Logs:
[`evidence/stage6-body-dry-run.log`](evidence/stage6-body-dry-run.log) and
[`evidence/stage6-body-proof.log`](evidence/stage6-body-proof.log).

The proof is both result-discriminating and sensitive to the executed body.

## 7. Proven versus assumed accounting

### What is machine-checked

Under the freshly compiled supplied MPY semantics plus the two `gcdEuclid`
equations, for every K integer pair `A,B`:

1. the exact submitted closure call reaches its exact loop-head state; and
2. that loop, return expression, builtin call, and frame cleanup reach
   `gcdEuclid(A,B)`.

The exact intermediate configurations unify, so their reachability theorems
compose. This is partial correctness: the K claims do not themselves constitute
a separate total-termination theorem.

### Trust and informal boundaries

- **K implementation and logic:** `kompile`, Haskell `kprove`, LLVM `krun`,
  K builtins for integers/booleans/maps/lists, and reachability circularity are
  trusted.
- **Supplied semantics:** the frozen 25-entry trusted tree is the mandated
  operational model. Its used slice was reviewed and concretely exercised;
  equivalence of the entire minimal MPY language to all of CPython is outside
  this theorem.
- **Translator:** the trusted `py2mpy.py` bridge from Python AST to MPY
  constructors is trusted. Byte regeneration and constructor-level claim
  comparison verify that this exact translation, not a hand-substituted body,
  is pinned.
- **Ordinary mathematics:** Euclid’s common-divisor invariance, remainder
  descent, and the convention that gcd is non-negative justify the meaning of
  `gcdEuclid`. They are not separately formalized as a divisibility theorem in
  K.
- **Claim composition:** reachability transitivity is used explicitly. The
  exact constructor/cell unifier is machine-checked by the reviewer script,
  although the candidate packages the result as two claims rather than one
  final entry-to-result claim.
- **Opaque symbols:** the fixed float/sort/MD5 opaque symbols are trusted by
  the supplied model but have no dependency path to these claims.
- **Empirical evidence:** the 11,578-case differential and concrete K runs
  support program/intent and semantics bridges only on tested inputs. They do
  not replace the universal K proof.

### Final judgment

Gate A (real-program soundness) passes: fresh `#Top`, exact body/control
pinning, no execution-bypassing extension, satisfying preconditions, and
successful negative probes. Gate B covers the full stated integer domain and
the standard gcd property, but carries the documented canonical-sign conflict.
Gate C is reproducible and the trust ledger is explicit.

The conflict does not justify `FAIL / NOT_LEGIT`: the proof is sound, pins the
real generated program, and does not narrow the HumanEval source domain.
It does justify retaining a non-fatal concern rather than silently declaring
the canonical and prompt equivalent on negative integers.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
