# Independent adversarial audit: HumanEval 131 `digits`

This audit reconstructed the candidate from source and did not rely on the
candidate's `kprove.stdout`, compiled artifacts, generation report, or prose.
The reconstructed theorem is a legitimate partial-correctness proof for the
full stated domain of positive Python integers. The proof executes the exact
submitted function body under the supplied semantics, constrains the returned
integer to a truthful base-10 recurrence, and rejects both a material body
mutation and a false result.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = semantics`, and `semantics_mode = SUPPLIED_SEMANTICS`. The trusted
tree `/reference/reference-semantics` is present, so the mounts agree with the
rendered mode. There is no infrastructure breach.

The reviewer script
[`evidence/stage1_integrity.py`](/audit-output/evidence/stage1_integrity.py)
performed `lstat`-based type checks, hashes, JSON checks, recursive tree
comparison, and full JSONL parsing. Its command and complete bounded output are
in
[`evidence/stage1_integrity.log`](/audit-output/evidence/stage1_integrity.log).
It exited 0 and reported `STAGE1_INTEGRITY_OK`.

Specific findings:

- `/audit-input.json` and `/audit-campaign-lock.json` are regular readable
  files. The `audit_campaign` object equals the lock object exactly, and the
  independently calculated lock SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  matching the recorded hash.
- All launcher `container_paths` resolve to the expected regular-file or
  directory type.
- Every record required by `legacy-selected-stage1` is present:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured trace. `usage.json` is
  present and was inspected. `runtime-metrics.json` is absent, which the
  benchmark explicitly permits for this historical layout.
- The independently calculated hashes of the run manifest, task manifest,
  stage-1 result, invocation, generation metrics, prompt, usage, last message,
  output log, and trace JSONL all match their recorded values. The 304-line
  structured trace parses without error.
- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`
  (`4a1c555a...8767c`), and candidate `py2mpy.py` is byte-identical to
  `/reference/py2mpy.py` (`406485ea...db16`).
- The candidate and trusted `reference-semantics/` trees contain the same 24
  regular files with the same bytes and directory layout. Neither tree
  contains symlinks, missing entries, extra entries, or special files. The
  per-file manifest is recorded in the integrity log. The legacy and current
  aggregate semantics hashes in the launcher use different historical tree
  hashing schemes; direct entry/type/byte equality independently establishes
  the required integrity.
- All five required candidate proof artifacts are regular files.

The untrusted generation records were content-inspected, not merely hashed.
[`evidence/stage1_generation_record_summary.py`](/audit-output/evidence/stage1_generation_record_summary.py)
parsed the JSON records and every structured-trace line, and extracted bounded
generation commands/messages and proof claims from the 18,695-line output log.
See
[`evidence/stage1_generation-record-summary.log`](/audit-output/evidence/stage1_generation-record-summary.log).
Those records claim `KPROVE_PASSED`, but that claim was not used as proof
evidence.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted source contract says: for a positive integer `n`, return the
product of its odd decimal digits; return 0 if every digit is even. Its examples
are `digits(1) == 1`, `digits(4) == 0`, and `digits(235) == 15`.

The trusted canonical implementation converts `n` to decimal text, filters odd
digits, and multiplies them. The submitted implementation instead repeatedly
examines the least-significant digit and divides by 10. For nonnegative
integers, `n` and its least-significant decimal digit have the same parity, so
testing `n % 2 == 1` correctly decides whether `n % 10` is odd. The zero
accumulator is a safe "no odd digit yet" sentinel because an odd digit is never
zero.

From the scratch copy, the exact command

```text
python3 /tmp/audit-work/reconstruction/py2mpy.py /tmp/audit-work/reconstruction/solution.py > /tmp/audit-work/reconstruction/solution.mpy
```

exited 0. `cmp` against the submitted `solution.mpy` exited 0; both files have
SHA-256 `bcbb57c135a74bccedb80630923f77d64b987486df74b8b389ce80f84c15d066`.
The commands and statuses are in
[`evidence/stage2_fidelity.log`](/audit-output/evidence/stage2_fidelity.log).

The independent differential
[`evidence/differential.py`](/audit-output/evidence/differential.py) used three
separate computations:

1. the trusted canonical module;
2. the generated candidate module from scratch; and
3. a reviewer-written decimal-digit contract oracle.

It checked the three examples, 21 branch/boundary values, zero as an explicitly
out-of-contract empty-loop extension, every positive integer from 1 through
10,000, 500 seeded values of 1 through 300 decimal digits, and seven structured
500-digit values. All 10,532 inputs are preserved in
[`evidence/differential-inputs.jsonl`](/audit-output/evidence/differential-inputs.jsonl).
The run exited 0 with `mismatch_count=0`. This finite differential supports the
implementation/intent bridge but is not substituted for the universal K proof.

## 3. Clean proof reconstruction

Only source files were copied into `/tmp/audit-work/reconstruction`. No
candidate `*-kompiled` directory, backend cache, or compiled definition was
copied or reused. The installed tools independently reported K version
7.1.293.

The fresh concrete build used:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0. The compiler's non-exhaustiveness warnings concern unused
list/float/method/subscript helpers in the fixed semantics, not any construct
reached by this integer-only program. The exact output is in
[`evidence/stage3_llvm-build.log`](/audit-output/evidence/stage3_llvm-build.log).
Both `krun solution.mpy --output none` and a reviewer harness containing 11 K
assertions exited 0; see
[`evidence/k-concrete-tests.py`](/audit-output/evidence/k-concrete-tests.py)
and
[`evidence/stage3_concrete-runs.log`](/audit-output/evidence/stage3_concrete-runs.log).

The fresh proof build used:

```text
kompile verification.k --backend haskell \
  --main-module DIGITS-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0. The clean target proof then used:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module DIGITS-SPEC
```

It exited 0 and printed `#Top`
([`evidence/stage3_kprove-all.log`](/audit-output/evidence/stage3_kprove-all.log)).
An explicit label list containing both positive claims also exited 0 and
printed `#Top`
([`evidence/stage3_kprove-explicit-both.log`](/audit-output/evidence/stage3_kprove-explicit-both.log)).
The loop claim alone also printed `#Top`.

A diagnostic command retaining only `DIGITS-SPEC.digits-correct` exited 1. This
does not contradict the all-claims success: `--claims` removes the
`digits-loop` circularity that the entry proof is designed to use. The
candidate's positive proof target is the two-claim module, and both the normal
all-claims command and the explicit two-label command check both claims
together. The dependency and residual are preserved rather than hidden in
[`evidence/stage3_kprove-digits-correct.log`](/audit-output/evidence/stage3_kprove-digits-correct.log).

## 4. Adequacy and real-program pinning

The two claims mean:

- `digits-loop`: for any `N >= 0` and `A >= 0`, in the exact function-local
  scope with `n = N` and `product = A`, executing the submitted while loop
  returns to the arbitrary preserved continuation `CONT` with `n = 0` and
  `product = oddDigitProduct(N, A)`.
- `digits-correct`: for any `N > 0`, in a clean module configuration where
  `digits` is bound to the submitted closure, calling `digits(N)` returns
  `oddDigitProduct(N, 0)`. The scope counter, heap, stack, return state,
  exception state, and exit code are pinned to a realizable clean call state.

The entry postcondition is a direct equality target in the `<k>` cell. It is
not a free result variable, tautology, or one-way implication.

[`evidence/stage4_pinning.py`](/audit-output/evidence/stage4_pinning.py)
performed a mechanical constructor comparison after only whitespace and
`.Stmts`-identity normalization:

- `solution.mpy` contains exactly one `FuncDef("digits", Params("n"), BODY)`;
- all three `closureVal` terms in the claims contain that exact `BODY`;
- the auxiliary `#while` guard and body equal the submitted `While` guard and
  body; and
- the entry term is exactly
  `Call(Name("digits"), Int(N:Int)) => oddDigitProduct(N, 0)`.

The script exited 0 and recorded satisfying witnesses. For example, `N=235`
satisfies the entry precondition and yields 15 in the candidate, canonical, and
formal recurrence; `(N,A)=(235,0)` satisfies the loop precondition and yields
15. Other witnesses cover even-only, embedded-zero, existing-accumulator, and
zero-loop cases. See
[`evidence/stage4_pinning.log`](/audit-output/evidence/stage4_pinning.log).

The recurrence has the intended mathematical meaning. For `N > 0`, let
`D = N mod 10` and `Q = (N-D)/10`. Then `N = 10Q+D`, so `N` is odd exactly when
`D` is odd. The definition skips even `D`, installs the first odd `D` when the
accumulator is zero, and otherwise multiplies by `D`; it recurses on the
strictly smaller nonnegative `Q`. The base case returns the accumulator at
`N=0`. Induction on `N` therefore establishes that
`oddDigitProduct(N,0)` is 0 when no decimal digit is odd and otherwise is the
product of all odd decimal digits. Multiplication commutativity makes the
least-significant-first traversal equivalent to the canonical order.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is in
[`evidence/stage5_rule-inventory.log`](/audit-output/evidence/stage5_rule-inventory.log),
and an exact line-numbered snapshot of every audited K source is in
[`evidence/stage5_full-source.txt`](/audit-output/evidence/stage5_full-source.txt).
The inventory contains 228 syntax declarations, 703 rules, five contexts, one
configuration, 45 priority-bearing items, 108 total declarations, 147 function
declarations, 35 concrete attributes, 25 symbol attributes, 22
`no-evaluators` attributes, three simplifiers, and both claims.

Every inventoried file was assigned the following disposition:

| Source | Declarations | Rules | Disposition |
|---|---:|---:|---|
| `syntax.k` | 16 | 0 | Constructor declarations; the used subset is mapped below. |
| `core.k` | 37 | 46 | Used configuration, sequencing, lookup, literals, truthiness, and argument evaluation are faithful; unused heap/collection helpers cannot match this program. |
| `operators.k` | 0 | 10 | Used left-to-right dispatch and comparison contexts are faithful; reference-object cases are unreachable. |
| `int.k` | 1 | 16 | Used `*`, `%`, `//`, `>`, and `==` rules are correct for positive divisors 2 and 10 and unbounded integers. |
| `controls.k` | 3 | 34 | Used name assignment, augmented assignment, `If`, and `While` rules preserve evaluation order, scope, continuation, and loop control. Other control forms are unreachable. |
| `functions.k` | 4 | 15 | Used definition, parameter binding, return, frame pop, and result restoration match the exact clean call state. |
| `call.k` | 3 | 21 | Used callee lookup, argument evaluation, and `closureVal` call rule preserve binding, stack, environment, and continuation. |
| `assert.k`, `bool.k`, `builtins.k` | 38 | 153 | Fixed-semantics facilities not reached by the proof term (apart from builtins-scope construction); no task answer occurs in them. |
| `comprehension.k`, `dict.k`, `list.k`, `methods.k`, `range.k`, `set.k`, `str.k`, `subscript.k`, `tuple.k` | 79 | 244 | Collection/string constructs are absent from `solution.mpy`; their rules cannot contribute to claim closure. |
| `float.k`, `sort.k` | 40 | 140 | Their fixed opaque/concrete primitives are unreachable from this all-`Int` term and do not influence control or result. |
| `iter.k` | 1 | 0 | Iterator syntax only; unused. |
| `concrete.k` | 5 | 16 | Imported only by `MPY-KRUN`, never by the proof main module; used only for finite concrete checks. |
| `verification.k` | 1 | 8 | All proof-local declarations and rules are reviewed individually below. |

The used constructor-to-rule map is complete:

- `Module`, `FuncDef`, `Params`, `Assign`, `While`, `If`, `AugAssign`, and
  `Return` are declared in `syntax.k`;
- statement loading/sequencing, `Name`, `Int`, scope lookup, and truthiness are
  handled in `core.k`;
- strictness/contexts and `BinOp`/`Compare` dispatch are in `syntax.k` and
  `operators.k`;
- integer multiplication, modulo, floor division, greater-than, and equality
  are in `int.k`;
- assignment, augmented assignment, branches, and while-loop continuations are
  in `controls.k`; and
- closure construction, call frame allocation, parameter binding, return, and
  frame restoration are in `functions.k` and `call.k`.

All material operations execute through those fixed rules. There is no
proof-local `<k>` rewrite that intercepts a call, loop, return, branch, or
arithmetic operation. There is no proof-local priority rule, opaque symbol,
fresh result, or oracle.

The proof-local inventory is:

1. `oddDigitProduct(Int,Int)` and
   `oddDigitStep(Bool,Int,Int,Int)` are `[function,total]` definitional
   summaries. The `N=0` and `N>0` equations are disjoint. Every value reached
   from the theorem has `N>=0`; totality leaves negative inputs unspecified but
   cannot affect a theorem path or entail a false equality. For `N>0`, the
   recursive quotient is nonnegative and strictly smaller.
2. The three `oddDigitStep` equations are pairwise disjoint and exhaustive:
   false guard; true guard with zero accumulator; and true guard with nonzero
   accumulator. They exactly mirror the program's two nested branches.
3. The three `[simplification]` equality rules are derived lemmas, not
   operational bridges. Under their guards, one unfolding of
   `oddDigitProduct` followed by the corresponding `oddDigitStep` equation
   produces the opposite side. Their modulo-10 expression is syntactically
   the fixed `pyMod` definition.

For an independent machine check of item 3, the reviewer built
[`evidence/verification-base.k`](/audit-output/evidence/verification-base.k),
which contains only the five defining equations and omits all three
simplifiers. All three universal one-step connection claims in
[`evidence/simplifier-connection-spec.k`](/audit-output/evidence/simplifier-connection-spec.k)
then printed `#Top` under that base-only definition. Commands and output are in
[`evidence/stage5_connection-build.log`](/audit-output/evidence/stage5_connection-build.log)
and
[`evidence/stage5_simplifier-connections.log`](/audit-output/evidence/stage5_simplifier-connections.log).

The guards of the proof-local equations are disjoint where right-hand sides
differ, cover every theorem-reachable call, and descend structurally. No
unsound rule was found, so there is no false-conclusion witness to report.

The body-sensitivity mutation changed `% 2` to `% 3` in the program terms
actually executed by both claims, while leaving the claimed summary unchanged.
The mutated K parsed and ran, then exited 1 with `WarnStuckClaimState`; its
residual explicitly contains the mutated `%Int 3` branch and the unmet
`oddDigitProduct` equality. See
[`evidence/body-sensitivity-spec.k`](/audit-output/evidence/body-sensitivity-spec.k)
and
[`evidence/stage5_body-sensitivity.log`](/audit-output/evidence/stage5_body-sensitivity.log).

## 6. Fresh non-vacuity test

The reviewer-created
[`evidence/false-result-spec.k`](/audit-output/evidence/false-result-spec.k)
keeps the exact program, loop claim, precondition, and state but changes the
entry result to:

```text
oddDigitProduct(N, 0) +Int 1
```

This is demonstrably false for the satisfying input `N=1`: both Python
implementations and the formal summary return 1, while the mutated target
requires 2.

First,

```text
kprove false-result-spec.k --definition verification-kompiled \
  --spec-module FALSE-RESULT-SPEC --dry-run
```

exited 0, establishing that the mutation builds and parses
([`evidence/stage6_false-result-dry-run.log`](/audit-output/evidence/stage6_false-result-dry-run.log)).
The actual proof command exited 1 with `WarnStuckClaimState`, not a parser
error, timeout, crash, or missing import. Its residual contains the expected
unmet condition `oddDigitStep(...) +Int 1 #Equals oddDigitStep(...)`. See
[`evidence/stage6_false-result-kprove.log`](/audit-output/evidence/stage6_false-result-kprove.log).
The proof is therefore result-discriminating and non-vacuous.

## 7. Proven versus assumed accounting

### What the K proof establishes

Conditional on the K toolchain and supplied semantics, the successful
all-path reachability proof establishes:

- for every mathematical integer `N > 0`, starting from the exact clean
  configuration in `digits-correct`, execution of the exact submitted
  `digits(N)` body has partial-correctness result
  `oddDigitProduct(N,0)`; and
- for every `N >= 0` and `A >= 0`, the exact loop body transforms its local
  state according to the stated recurrence and preserves its arbitrary
  continuation.

Together with the elementary base-10 induction in Stage 4, that result is
exactly the contract's product of odd digits, including 0 when none exist. The
formal domain is the full unbounded positive-integer domain; there is no fixed
size, bounded unrolling, finite example restriction, or strengthened source
precondition.

This is partial correctness. The audit does not recast the circular
reachability proof as a separate machine-checked termination theorem, although
the concrete algorithm plainly decreases a positive integer by floor division
by 10.

### Trust and assumption ledger

- **K parser, kompilers, Haskell prover, LLVM backend, SMT reasoning, and K
  built-ins (`Int`, `Bool`, `Map`, `List`, strictness, and reachability
  circularity):** foundational toolchain trust. Both clean backends rebuilt
  successfully with the campaign-pinned K 7.1.293.
- **Supplied MPY semantics:** fixed benchmark trust boundary. Its candidate
  copy is recursively byte-identical to the trusted mount. The entire source
  was inventoried, and the operational fragment used by this term was
  reviewed for binding, order, control, state, and arithmetic fidelity.
- **Opaque fixed-semantics primitives:** float operations
  (`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`,
  `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`,
  `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`), `md5hexCodes`,
  `sortVS`, and `sortKeyVS`. None is reachable from the submitted constructor
  term or appears in a proof-local postcondition, so none affects this result.
- **Trusted translator:** independently pinned by byte identity. Fresh
  translation reproduced the submitted constructor term byte-for-byte.
- **Proof-local functions and lemmas:** not assumed. Their equations were
  audited for truth, disjointness, coverage on the theorem domain, and descent;
  the three simplifier connections were additionally checked under a
  base-only definition.
- **Summary-to-English-contract bridge:** ordinary base-10 induction stated
  explicitly in Stage 4. It introduces no empirical or opaque value oracle.
- **Finite empirical evidence:** the 10,532-case three-way Python differential
  and 11-assertion K concrete harness support program/semantics fidelity only;
  neither is counted as the universal proof.

### Gate results and decision

- Gate A, real-program soundness: **PASS**. The body executes under fixed
  semantics, all local lemmas are sound, exact constructor pinning holds, a
  material body mutation fails, a satisfying state exists, and the false
  result is rejected.
- Gate B, intent adequacy: **PASS**. The theorem covers every positive integer
  and its recurrence is exactly the requested odd-decimal-digit product.
- Gate C, trust and auditability: **PASS**. Sources, scripts, exact inputs,
  commands, statuses, and bounded outputs are preserved under
  `/audit-output/evidence`.

VERDICT: PASS
LEGITIMACY: LEGIT
