# Independent adversarial audit: 8-sum-product

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. I reconstructed both definitions from
source, proved the two positive claims afresh, checked the exact program term and
control state, inventoried all local K declarations/rules, and obtained the
expected failures from independent body- and result-sensitive mutations.

Candidate-produced compiled definitions, `PROOF.md`, logs, traces, and claimed
test results were not used as proof evidence.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present as a regular directory. The trusted
mount therefore agrees with the rendered condition; there is no infrastructure
breach.

The independent `lstat`/byte audit found:

- `run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.py`, `py2mpy.py`, `solution.py`,
  `solution.mpy`, `spec.k`, and `verification.k` are present as regular files.
- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`.
- Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- All 25 entries in the candidate `reference-semantics/` tree have the same
  relative path, type, and bytes as the trusted tree. There are no missing,
  additional, changed, mistyped, or symlinked entries.
- No required source or semantics-tree entry is a symlink.

The command, exit 0, and complete comparison result are in
[`01-provenance-integrity.log`](evidence/logs/01-provenance-integrity.log);
the checker is
[`provenance_check.py`](evidence/provenance_check.py).

I read the four generation records and the structured JSONL trace only as
untrusted claims. They claim an exit-0 generation, `#Top`, 20,611 differential
cases, two negative mutations, and `VALIDATED`. The independent summary records
the files' hashes, 25,807-line generation log, all 335 structured trace
records, record types, and the claimed final report:
[`02-untrusted-generation-records.log`](evidence/logs/02-untrusted-generation-records.log).
None of those claims is used below.

All source needed for execution was copied to `/tmp/audit-work/src`; trusted
prompt, canonical implementation, and translator were copied separately to
`/tmp/audit-work/trusted`. Candidate `runtime-kompiled/`,
`verification-kompiled/`, caches, and bytecode were not copied or read by the
reconstruction. The exact copy manifest and exit 0 are in
[`03-scratch-source-copy.log`](evidence/logs/03-scratch-source-copy.log).

Stage 1 result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For any finite list of integers, `sum_product(numbers)` returns the two-element
tuple consisting of:

1. the sum of every list element; and
2. the product of every list element.

The empty sum is 0 and the empty product is 1. The documented examples are
`[] -> (0,1)` and `[1,2,3,4] -> (10,24)`. This is exactly the contract in
`/reference/prompt.py` and the behavior of `/reference/canonical.py`.

### Submitted implementation

`solution.py` initializes `total=0`, `product=1`, and an otherwise unnecessary
`number=0`; it then performs `total += number` and `product *= number` for each
input element and returns `(total,product)`. The extra initialization makes the
loop target present even on an empty input but does not change the result. The
algorithm is materially the same fold as the canonical implementation.

The trusted translator regenerated the submitted MPY file at
`/tmp/audit-work/regenerated-solution.mpy`. `cmp` succeeded and both files have
SHA-256
`e1499681777c255ef5c9b9991e4247897effaa17718bcd044aaee03c7b3354a2`.
See the reviewer script
[`regenerate_solution_mpy.sh`](evidence/regenerate_solution_mpy.sh) and
[`04-translator-regeneration.log`](evidence/logs/04-translator-regeneration.log)
(exit 0).

### Independent differential test

[`independent_differential.py`](evidence/independent_differential.py) imports the
trusted canonical entry point and the copied generated entry point under
different module names. It does not reuse any K fold or candidate test. It
compared 24,623 inputs:

- both documented examples;
- empty, singleton, and two-element loop boundaries;
- negative, zero, positive, sign-parity, cancellation, and zero-position cases;
- 19,608 exhaustive lists over `[-3,3]` through length 5;
- 5,000 deterministic generated lists of lengths 0 through 20 and values in
  `[-1,000,000,1,000,000]`; and
- 64-bit-like and much larger unbounded Python integers.

The intended/formal domain is finite lists of integers; Python `bool` and
ill-typed elements are excluded. Every generated input is preserved in
[`differential_inputs.jsonl`](evidence/differential_inputs.jsonl), SHA-256
`7bd8769a983ee995984bc0401065b30b399966ae914ca83930d877484f7e6165`.
The exact command exited 0 with `mismatch_count=0`:
[`05-independent-differential.log`](evidence/logs/05-independent-differential.log).
This is finite implementation-to-canonical evidence, not a replacement for the
K proof.

Stage 2 result: **PASS**.

## 3. Clean proof reconstruction

The live toolchain is K v7.1.293; tool paths and versions are recorded in
[`25-toolchain-version.log`](evidence/logs/25-toolchain-version.log).

From `/tmp/audit-work/src`, with no candidate-built definition present, I ran:

```text
kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled
kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled
```

Both builds exited 0. The complete bounded logs are
[`06-kompile-concrete.log`](evidence/logs/06-kompile-concrete.log) and
[`07-kompile-proof.log`](evidence/logs/07-kompile-proof.log).

`spec.k` contains two positive claims. The loop invariant was run independently:

```text
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.loop-invariant
```

It printed `#Top` and exited 0
([`08-kprove-loop-invariant.log`](evidence/logs/08-kprove-loop-invariant.log)).
The entry claim depends on that invariant as a circularity, so the target proof
must keep both claims available:

```text
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
```

This checked the complete two-claim module, printed `#Top`, and exited 0
([`10-kprove-full-spec.log`](evidence/logs/10-kprove-full-spec.log)). Thus every
positive claim closes in the fresh proof definition.

For transparency, I also tried an entry-only diagnostic with
`--claims SPEC.sum-product`. That filter removes the very loop claim on which
the entry depends, so I interrupted the unproductive unrolling with exit 130.
It is preserved as
[`09-kprove-entry-sum-product.log`](evidence/logs/09-kprove-entry-sum-product.log)
and is not the target proof command or a candidate failure.

Fresh concrete reconstruction supplied two additional checks:

- `krun solution.mpy --definition audit-runtime-kompiled` executed the exact
  submitted module to `.K`, installed the exact function body, left `NoExc`,
  and exited 0
  ([`11-krun-exact-solution-module.log`](evidence/logs/11-krun-exact-solution-module.log)).
- A reviewer harness whose function AST is identical to `solution.py` exercised
  normal, empty, singleton, zero/sign, and large-integer cases. Its corrected
  run reached `.K`, `NoExc`, and exit code 0
  ([`concrete_audit.py`](evidence/concrete_audit.py),
  [`run_concrete_audit.sh`](evidence/run_concrete_audit.sh), and
  [`13-krun-concrete-harness-corrected.log`](evidence/logs/13-krun-concrete-harness-corrected.log)).

The initially recorded harness run failed because my expected sum for
`[2**63-1,-2**63,1]` was mistakenly `-1` instead of `0`; Python rejected the
same bad assertion. That reviewer error and exit 1 remain visible in
[`12-krun-concrete-harness.log`](evidence/logs/12-krun-concrete-harness.log);
the oracle was corrected before using the harness as evidence.

Stage 3 result: **PASS**.

## 4. Adequacy and real-program pinning

### Loop claim

The `loop-invariant` precondition says:

- the active computation is exactly the submitted `for` loop over the remaining
  semantic list `VS`, followed by the submitted `Return(total,product)` and
  `#endcall`;
- every element of `VS` is a K `Int`;
- the current local accumulators are integers `T` and `P`;
- the call frame, closure body, environment/scopes, stack, return state,
  exception state, and exit code have the exact real-call shape; and
- the original `numbers`, prior loop-target value, heap, and heap counter may be
  arbitrary in the types shown because the loop body does not use or change
  them.

The postcondition consumes the loop, return, and `#endcall`; returns
`tuple(sumFrom(T,VS),productFrom(P,VS))`; removes the local scope and call frame;
restores `env=0` and `scopeLoc=1`; and preserves the heap and heap counter.
This is an exact real-control-flow summary, not a rule that bypasses execution.
The claim is itself proved, with recursive use only after one real list
iteration.

### Entry claim

The `sum-product` precondition is the exact initial MPY configuration: empty
module scope, builtin parent, `env=0`, `scopeLoc=1`, empty stack, `noRet`,
`NoExc`, exit code 0, arbitrary preserved heap/counter, and an all-integer
`VS`. Its `<k>` cell loads the exact submitted module and then calls the loaded
`sum_product` binding with `list(VS)`.

The postcondition directly requires:

```text
tuple(vCons(sumFrom(0,VS),vCons(productFrom(1,VS),.ValSeq)))
```

There is no fresh right-only result variable, implication-only weakening,
oracle, or tautology. The final module scope also retains the exact submitted
closure body.

The line-numbered constructor trees are preserved in
[`16-line-numbered-program-claims.log`](evidence/logs/16-line-numbered-program-claims.log).
`solution.mpy:1-10` matches the entry's `Module` at `spec.k:64-74`; the function
body is repeated exactly in the claimed final closure. The loop claim's body and
continuation at `spec.k:8-12` match the real `For` body and subsequent `Return`.

### Satisfiable states and substitutions

An entry witness is `VS=.ValSeq`, empty heap, heap counter 0, and the exact
initial cells above. `intsVS(.ValSeq)=true`, and the direct result is `(0,1)`.

A reachable loop-head witness uses
`VS=INPUT=[2,4]`, `T=0`, `P=1`, `N=0`, empty heap/counter, `env=1`,
`scopeLoc=2`, and `stack=ListItem(frame(.K,0,1))`. The formal folds give `(6,8)`.
The same nonempty substitution in the entry claim gives `(6,8)`. Both trusted
canonical Python and generated Python return the same values for both witnesses.
The executable record is
[`adequacy_witness.py`](evidence/adequacy_witness.py) and
[`15-adequacy-witness.log`](evidence/logs/15-adequacy-witness.log) (exit 0).

Stage 4 result: **PASS**.

## 5. Rule-by-rule static soundness review

[`K-INVENTORY.md`](evidence/K-INVENTORY.md) is the exhaustive inventory over the
assembled semantics, every supplied helper K file, `verification.k`, and
`spec.k`. Its raw-start cross-check passes and accounts for:

- 26 files;
- 230 local syntax declarations;
- 705 ordinary rules;
- five contexts;
- one configuration; and
- two reachability claims.

Every complete rule block includes its line, guards, cells, and detected
attributes. The inventory explicitly records zero `functional` and zero
`simplification` declarations, and enumerates all function/total, concrete,
opaque/no-evaluator, priority, `owise`, macro, strictness, ordinary-rule, and
claim blocks.

The decision for every inventory bucket, a per-module count/disposition table,
the exact used-syntax map, configuration/cell analysis, priority/overlap review,
and ten individual proof-local decisions are in
[`STATIC-REVIEW.md`](evidence/STATIC-REVIEW.md). The essential findings are:

- The used path is ordinary module loading, ignored annotation import, function
  creation/call, left-to-right argument/tuple evaluation, plain local
  assignment, list iteration, integer `AugAssign`, return, and frame pop. All
  cells read or changed by these rules are pinned by the claims.
- The supplied baseline contains no `sum_product`, `sumFrom`, or `productFrom`
  symbol and no task-answer rule
  ([`20-static-searches.log`](evidence/logs/20-static-searches.log)).
- `intsVS` is a total structural all-integers predicate. `sumFrom` and
  `productFrom` are total, structurally descending folds. Their integer and
  non-integer guards are complementary; the non-integer totalization is
  unreachable under `intsVS`.
- The two proof-local `applyBin` equations are guarded by `isInt(V)` and exactly
  agree with the supplied `applyBin("+",Int,Int)` and
  `applyBin("*",Int,Int)` rules on their complete match domain. They are pure
  derived equations: no lookup, evaluation, call, return, exception, state,
  allocation, or continuation is skipped.
- Fixed LLVM semantics and the proof-extended Haskell definition produced
  byte-identical complete configurations on the concrete harness, including
  every cell. Both hashes are
  `e7001675982c33d58a71a55711a67d408aa9bcb1dd9d5c8f9bbfbcaf5c0b7727`
  ([`compare_fixed_extended.sh`](evidence/compare_fixed_extended.sh),
  [`14-fixed-vs-extended.log`](evidence/logs/14-fixed-vs-extended.log), and the
  two preserved configuration outputs).
- Supplied opaque float, sorting, and MD5 symbols are not reachable from the
  submitted program or claims. They remain a named but irrelevant baseline
  trust boundary.
- The concrete build reports six supplied `[total]` helpers with unmatched
  constructor cases: `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and
  `valSeqAt`. None is reachable here. These are documented coverage/stuckness
  gaps, not false equations or false-conclusion witnesses on the intended
  domain, so I do not label them unsound.

As a separate body-sensitivity check, I changed the real product update from
`*=` to `+=` while leaving the concrete `[2,4] -> (6,8)` obligation. The
mutation parsed and built under `--dry-run` with exit 0
([`21-body-mutation-dry-run.log`](evidence/logs/21-body-mutation-dry-run.log)).
Its proof exited 1 with `WarnStuckClaimState` and the exact residual actual value
`(6,7)` against expected `(6,8)`
([`audit-body-mutation.k`](evidence/audit-body-mutation.k) and
[`22-body-mutation-proof.log`](evidence/logs/22-body-mutation-proof.log)).
This demonstrates sensitivity to the dispatched operator and loaded body.

No inventoried rule is claimed unsound, so no unwitnessed unsoundness allegation
is being made.

Stage 5 result: **PASS**.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh mutation
[`audit-result-mutation.k`](evidence/audit-result-mutation.k) runs the exact
original program on the satisfying empty-list input but changes the required
product from 1 to 2.

First:

```text
kprove audit-result-mutation.k --definition audit-verification-kompiled --spec-module AUDIT-RESULT-MUTATION --dry-run
```

parsed/compiled successfully and exited 0
([`23-result-mutation-dry-run.log`](evidence/logs/23-result-mutation-dry-run.log)).
Then the same command without `--dry-run` exited 1, printed
`WarnStuckClaimState`, and showed the expected semantic residual: actual
`tuple(0,1)` cannot unify with required `tuple(0,2)`. See
[`24-result-mutation-proof.log`](evidence/logs/24-result-mutation-proof.log).
The failure is the intended unmet result obligation, not a parser failure,
missing import, timeout, crash, or unreachable mutation.

Stage 6 result: **PASS**.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the supplied MPY definition, for every finite `ValSeq` consisting only of
K `Int` values, starting in the exact pinned initial configuration, loading the
exact trusted-translator output and calling its loaded `sum_product` binding
reaches normal completion with the tuple:

```text
(left-fold integer addition from 0,
 left-fold integer multiplication from 1)
```

The arbitrary initial heap and heap counter are preserved, the call frame is
removed, the module closure remains exact, the stack is empty, the return state
is cleared, no exception is present, and the exit code remains 0. This is a
partial-correctness theorem. It does not separately claim a termination theorem
or behavior for inputs outside the all-integer finite-list domain.

### Trust ledger

| Boundary | Effect | Evidence and judgment |
|---|---|---|
| K v7.1.293 compiler, LLVM/Haskell backends, and reachability engine | All parsing, rewriting, and proof checking | Unavoidable proof-checker trust; fresh builds and exact success/failure signals are reproducible. Acceptable. |
| Supplied `reference-semantics` | Language values, control, cells, calls, loop, and return | Condition-authorized fixed semantics; candidate tree is recursively byte-identical to trusted mount. Used execution slice was statically reviewed and concretely exercised. Acceptable. |
| K builtins for unbounded `Int`, `Bool`, maps/lists, equality, sort predicate `isInt`, guarded projection `{V}:>Int`, `+Int`, and `*Int` | Input predicate and mathematical result | Ordinary K primitives and mathematics; the projection is used only under its exact sort predicate. Acceptable low-level boundary. |
| Trusted `py2mpy.py` | Python-source to submitted MPY constructor tree | Candidate translator is byte-identical to trusted input, and trusted regeneration is byte-identical to submitted MPY. Acceptable source-to-program bridge. |
| Plain-language/canonical-to-fold interpretation | Human-facing meaning of the returned K tuple | `sumFrom`/`productFrom` equations directly define the requested folds; empty equations are 0/1. Canonical and generated Python agree on 24,623 preserved cases. The finite test supports but does not prove the universal bridge; the mathematical definition supplies the universal intent argument. Acceptable. |
| Supplied opaque float/sort/MD5 symbols | Potential values in unrelated programs | No dependent claim or used term. Explicitly excluded from this theorem; immaterial. |
| Six supplied totality coverage warnings | Potential stuckness in unrelated helpers | No dependent symbol or reachable term. Recorded as evidence gaps, not assumed task results. Immaterial. |
| Candidate `PROOF.md`, logs, compiled definitions, traces, and tests | None | Treated only as untrusted claims and excluded from proof evidence. |

There is no proof-local opaque symbol, empirical oracle, priority shortcut,
program-defined-body summary, or assumed task conclusion. Differential testing
supports only implementation/canonical alignment and concrete semantic behavior;
it is not used in place of either reconstructed `#Top`.

Validating-proof Gate A (real-program soundness and non-vacuity): **PASS**.
Gate B (intent/domain adequacy): **PASS**. Gate C (trust and reproducible
evidence): **PASS**.

The unused supplied-semantics coverage limitations do not affect the submitted
program or theorem and do not create a material adequacy gap. The reconstructed
proof is sound, result-constraining, and pins the real generated program.

VERDICT: PASS
LEGITIMACY: LEGIT
