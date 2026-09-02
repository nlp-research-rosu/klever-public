# Independent adversarial audit: 123-get-odd-collatz

## Executive decision

The reconstructed K artifacts are internally honest for the claims they
actually state: all seven submitted claims close from clean source, the local
step claims execute real semantics, the four concrete entry claims constrain
their results, and a fresh false-result mutation is rejected.

They are not, however, a K partial-correctness proof for the requested input
domain. There is no symbolic entry claim for arbitrary positive `n`, no formal
initialization/invariant/summary link from an entry state to the exit state, and
no claim uses the declared `collatzResult` function. The only complete entry
proofs are the four ground inputs `1`, `5`, `6`, and `7`. The prose assertion
that the local steps compose by induction is an informal argument, not a
machine-checked reachability theorem. This is a material adequacy gap covered
by the `FAIL / NOT_LEGIT` decision boundary.

The audit used the required `using-kit` and `validating-proof` procedures.
Candidate prose, scripts, and traces were treated only as untrusted evidence.
All execution occurred on scratch copies under
`/tmp/audit-work/123-get-odd-collatz`; no candidate cache or compiled
definition was reused.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` tree exists, so there is no mode/mount
contradiction and no infrastructure breach.

Findings:

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
- `/candidate/py2mpy.py` is byte-identical to
  `/reference/py2mpy.py`.
- The candidate `reference-semantics/` and trusted
  `/reference/reference-semantics/` have identical manifests, entry types,
  sizes, and bytes. `diff --no-dereference -qr` exited 0.
- No candidate entry is a symlink.
- `solution.py`, `solution.mpy`, `spec.k`, and `verification.k` are regular
  files.
- The requested untrusted generation records are missing:
  `run-input.json`, `metrics.json`, `codex-last.txt`, and
  `codex-output.log`. No structured generation-trace file was present. This
  is an auditability/provenance defect, but not an infrastructure failure and
  not the reason the proof is rejected.
- Candidate `__pycache__` files were ignored and not copied into the clean
  proof source tree.

Commands, statuses, manifests, and hashes are in
[`evidence/stage1_integrity.log`](evidence/stage1_integrity.log); the
reviewer-authored command script is
[`evidence/stage1_integrity.sh`](evidence/stage1_integrity.sh).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a positive integer `n`, follow the mathematical Collatz transition:
halve an even value and replace an odd value by `3n+1`. If the execution
reaches `1`, return all odd values encountered, including the initial value
when odd and terminal `1`, sorted in increasing order. This audit concerns
partial correctness; it does not assume or prove universal Collatz
termination.

`solution.py` implements that contract with exact integer `%`, `//`, `*`, and
`+`. Its `while n != 1` condition is appropriate on the positive domain.

### Translation identity

The trusted translator was run afresh:

```text
cd /tmp/audit-work/123-get-odd-collatz/candidate-src &&
python3 /tmp/audit-work/123-get-odd-collatz/trusted/py2mpy.py solution.py > solution.regenerated.mpy
```

The command exited 0. The regenerated and submitted files are byte-identical,
both with SHA-256
`f470d729dc9c46994f7f0d672ef2e931e8d1857c76da13ab3674e875074aa7e1`.

### Independent differential

The reviewer-authored
[`evidence/differential_test.py`](evidence/differential_test.py) imports the
trusted canonical and generated functions under distinct module names. It
records every input and full outcome for:

- the documented example;
- the positive boundary `1`;
- first odd/even and mixed branch boundaries;
- powers of two and the longer `27` trace;
- an empty out-of-domain value and zero with a bounded child process;
- 64 fixed-seed generated positive values from `1..5000`; and
- three floating-point exactness boundary probes.

The generated and canonical implementations agreed on the documented,
boundary, branch, long-trace, and all 64 fixed-seed positive cases. The empty
list produced `TypeError` in both. Zero is outside the contract: canonical
returns `[]` because its loop guard is `n > 1`, while the generated function
does not terminate because its guard is `n != 1`.

There were two material divergences inside the stated positive-integer domain:

- At `18014398509481986`, canonical returns `[1]`, while the generated
  function returns 139 odd values ending in `9007199254740993`.
- At `1152921504606846978`, canonical returns `[1]`, while the generated
  function returns 192 odd values.

The cause is the canonical implementation's `/`, which converts even
intermediates to binary floating point and rounds beyond exact representability;
the generated implementation uses integer `//`. Thus the generated code
matches the prompt's mathematical “one half” transition more faithfully, but
it is not extensionally equivalent to the trusted canonical over the
unbounded positive-integer domain. This is an additional intent/reference
bridge limitation.

The differential exited 1 because of those two in-domain mismatches. Exact
inputs and outputs are in
[`evidence/stage2_fidelity.log`](evidence/stage2_fidelity.log).

## 3. Clean proof reconstruction

The proof source tree was assembled from candidate `verification.k`, `spec.k`,
and program sources plus a fresh copy of the trusted supplied semantics.
There were no copied `*-kompiled` definitions.

K version:

```text
K version: v7.1.337
Build date: Thu Jun 18 07:59:56 CDT 2026
```

Fresh concrete build:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled-audit
```

Exit 0. The concrete assertion harness was independently regenerated with the
trusted translator, then:

```text
krun concrete_tests.regenerated.mpy \
  --definition runtime-kompiled-audit \
  --output none
```

Exit 0.

Fresh proof build:

```text
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled-audit
```

Exit 0.

Each target was then selected and run independently using:

```text
kprove spec.k \
  --definition verification-kompiled-audit \
  --spec-module SPEC \
  --claims <label> \
  --depth 2000 \
  --smt-timeout 5000
```

`odd-step`, `even-step`, `exit-step`, `case-1`, `case-5`, `case-6`, and
`case-7` each printed `#Top` and exited 0. The aggregate invocation without
`--claims` also printed `#Top` and exited 0.

An initial attempt used module-qualified selectors such as
`SPEC.odd-step`; this K version rejected those selectors as unused with exit
113. The accepted unqualified selectors were then used for the required
per-claim runs. This selector correction is not a candidate failure. Both
attempts are preserved.

The compact status record is
[`evidence/status_summary.log`](evidence/status_summary.log). Full build and
proof logs are under `evidence/stage3_*`; the orchestration scripts are
[`evidence/stage3_reconstruct.sh`](evidence/stage3_reconstruct.sh) and
[`evidence/stage3_claims_retry.sh`](evidence/stage3_claims_retry.sh).

## 4. Adequacy and real-program pinning

### Claim meanings and witnesses

| Claim | Plain-language precondition and postcondition | Satisfying witness |
|---|---|---|
| `odd-step` | At the real loop head, local `n=N`, accumulator `A`, `N>1`, and `N` odd. One iteration appends `N`, sets `n=3N+1`, and reaches the real loop-back label with all other stated cells preserved. | `N=3`, `A=[]`; poststate `n=10`, `A=[3]`. |
| `even-step` | At the same loop head, `N>1` and remainder is not `1` (hence even on this positive domain). One iteration leaves `A` unchanged and sets `n=N//2`. | `N=2`, `A=[]`; poststate `n=1`, `A=[]`. |
| `exit-step` | At `n=1`, with arbitrary accumulator `A`, the exact loop/append/return/end-call continuation and unshadowed `sorted`, exit the loop, append `1`, allocate `sortVS(A+[1])`, return its reference, and pop the frame. | `A=[3,5]`; both Python functions return `[1,3,5]` for input `3`. |
| `case-1/5/6/7` | From the complete empty initial configuration, load the function and execute the named ground input to the specified trace object and returned sorted object. | The literal input of each claim; both Python functions agree with all four claimed results. |

Witness calculations and Python substitutions are preserved in
[`evidence/stage4_pinning_witnesses.log`](evidence/stage4_pinning_witnesses.log).

### Program identity

`verification.k` does not `require` or parse `solution.mpy`; it hard-codes the
MPY `Module` term in the `#getOddCollatz` expansion. A reviewer-authored
balanced-term extractor and tokenizer compared that term with the submitted
`solution.mpy`. After normalizing the explicit `.Exprs` list unit, both have
186 tokens and are identical. Therefore the current hard-coded body is the
submitted program, although the build itself would not detect a later
source/body mismatch without this provenance check.

### Missing theorem

The complete entry claims have arguments exactly `1`, `5`, `6`, and `7`.
There is no symbolic `#getOddCollatz(N)` claim and no positive-domain
precondition on such a claim. `spec.k` contains zero occurrences of
`collatzResult`.

Consequently:

- the K proof does not connect arbitrary entry initialization (`A=[]`,
  `n=N`) to the local step claims;
- it does not state or preserve an invariant saying `A` is precisely the odd
  prefix of the Collatz trace;
- it does not connect an arbitrary terminating entry execution to
  `sortVS(collatzResult(N,.ValSeq))`; and
- it proves only four complete executions, not partial correctness for every
  positive input whose execution terminates.

The three local claims are useful transition lemmas. Informally composing them
by induction is plausible, but no K reachability claim asks `kprove` to perform
or validate that composition. `NOTES.md` cannot supply the missing theorem.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored inventory covers the assembled supplied semantics, all
23 helper files, `verification.k`, and `spec.k`. It records complete
multiline blocks, source line, kind, and attributes for:

- 230 syntax declarations;
- 700 rules (462 equational and 238 operational);
- 148 `function` declarations, 107 `total` declarations;
- 22 `no-evaluators` opaque declarations and 25 `symbol` declarations;
- 45 priority-bearing rules, 26 `owise` rules, and 36 concrete rules;
- 5 contexts, 1 configuration, 25 file requirements, 88 imports; and
- all 7 claims.

There are no `functional` or `simplification` declarations in these sources.
The exhaustive data is
[`evidence/stage5_inventory.tsv`](evidence/stage5_inventory.tsv), summarized
by
[`evidence/stage5_inventory_summary.json`](evidence/stage5_inventory_summary.json).
Every record has a disposition and reason in
[`evidence/stage5_assessments.tsv`](evidence/stage5_assessments.tsv).

### Used semantic slice

Every submitted syntactic construct is declared and has a real execution path:
module loading and sequencing; function definition/call/return; scope lookup
and parameter binding; list allocation and append; assignment; integer
operators; comparison; `if`; `while`; attribute/call evaluation; `sorted`; and
frame pop. Exact declarations and rules are mapped in
[`evidence/stage5_used_construct_map.md`](evidence/stage5_used_construct_map.md).

The used rules preserve the relevant state:

- allocation updates `heap` and monotonically advances `heapLoc`;
- assignment and argument binding update the active scope;
- append mutates the referenced list object in place;
- call creates the callee scope, changes `env`, and saves the exact caller
  continuation and scope location in `stack`;
- return records the value, discards the remaining callee body as Python
  return requires, and `#pop` restores caller control/state;
- while evaluates its condition before each body and routes through the
  explicit loop label;
- expression and argument evaluation order follows the syntax strictness and
  explicit left-to-right argument machinery; and
- branch and arithmetic guards are disjoint on the positive integer domain.

No used rule fabricates a program result, bypasses a program-defined body, or
silently handles an unmodeled used construct.

### Proof-local extensions

`verification.k` contains only three declarations and five rules:

1. `#getOddCollatz(N)` is an exact abbreviation for loading the normalized
   submitted module and calling its public entry point. It does not summarize
   or skip execution.
2. The three `collatzResult` equations are a truthful Collatz recurrence.
   Their base, odd, and non-odd guards are disjoint and exhaustive whenever
   `N != 1`. The function is deliberately not declared total because
   termination is not established. These equations are dead: no claim refers
   to the symbol.
3. `getOddCollatzClosure` is an exact abbreviation for the closure installed
   by the real function definition.

There are no proof-local opaque symbols, totality assertions, priority rules,
simplification rules, or operational bridges. No proof-local rule was found
unsound, so this review makes no unsupported unsoundness allegation requiring
a false-conclusion witness.

The compiler reported non-exhaustive-match warnings for several supplied
`total` helpers (`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and
`valSeqAt`) in the LLVM build. None is reached by this program on its stated
domain. These warnings are recorded as coverage gaps in the wider supplied
MiniPython subset, not as a demonstrated false conclusion for the audited
claims.

### Opaque/trusted operations

The exhaustive opaque-symbol list is
[`evidence/stage5_opaque_inventory.tsv`](evidence/stage5_opaque_inventory.tsv).
All float, MD5, and keyed-sort opaque symbols are unreachable here. The only
result-bearing opaque symbol used in symbolic proof is `sortVS`:

- It is a fixed supplied-semantics boundary for Python's external `sorted`
  builtin, not a summary of program-defined code.
- For ground integer lists, guarded insertion-sort equations provide the LLVM
  concrete behavior.
- For symbolic `A`, `sortVS(A)` remains opaque in Haskell. The `exit-step`
  claim therefore proves that execution returns `sortVS(A+[1])`, conditional
  on the supplied contract that this symbol is ascending sort. It does not
  prove ordering or permutation properties inside K.
- Candidate concrete tests and the independent differential support this
  contract only on their finite input sets. They are not a universal
  connection theorem.

This boundary does not encode this task's answer or permit an arbitrary
program-derived result. It is acceptable for the narrow execution claims but
would remain an explicit intent assumption even if the missing universal entry
claim existed.

## 6. Fresh non-vacuity test

The fresh mutation is
[`evidence/spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k). It keeps the
real input-5 trace object `[5,1]` but falsely requires the returned object to be
the sort of `[7,1]`. Input `5` is a satisfying initial state and both Python
implementations return `[1,5]`, so the mutation is demonstrably false.

Parse/build check:

```text
kprove spec-vacuity-audit.k \
  --definition verification-kompiled-audit \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run
```

Exit 0.

Proof:

```text
kprove spec-vacuity-audit.k \
  --definition verification-kompiled-audit \
  --spec-module SPEC-VACUITY-AUDIT \
  --depth 2000 \
  --smt-timeout 5000
```

Exit 1 with `WarnStuckClaimState`. The residual is the fully executed final
configuration with returned `ref(1)` and heap object
`list(vCons(1,vCons(5,.ValSeq)))`; it does not unify with the false
destination. This is the expected unmet result obligation, not a parser error,
timeout, or unrelated crash.

Full evidence is in
[`evidence/stage6_mutation_dry_run.log`](evidence/stage6_mutation_dry_run.log)
and
[`evidence/stage6_mutation_proof.log`](evidence/stage6_mutation_proof.log).
The result shows the concrete entry claims discriminate correct from false
results. It cannot validate an entry theorem that is absent.

## 7. Proven versus assumed accounting

### Machine-checked facts

Under the supplied semantics:

- an arbitrary positive odd loop value greater than one performs the claimed
  odd transition and accumulator append;
- an arbitrary positive even loop value greater than one performs the claimed
  halving transition without an append;
- at `n=1`, the exact exit continuation appends `1`, calls the supplied
  `sorted` primitive, returns its fresh reference, and restores the caller
  frame; and
- the complete submitted program produces the constrained claimed trace/result
  objects for inputs `1`, `5`, `6`, and `7`.

### Trusted or empirical boundaries

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K v7.1.337 and built-in integer/Boolean/map/list theories | All builds and proofs | Normal tool/theory trust boundary. |
| Byte-identical supplied MiniPython semantics | All execution claims | Authoritative in `SUPPLIED_SEMANTICS` mode; used fragment audited from source. |
| Opaque symbolic `sortVS` contract | `exit-step` and every returned list | Fixed external-builtin boundary, not task-answer smuggling; intent conclusion remains conditional. Concrete/differential evidence is finite. |
| Hard-coded MPY module in `#getOddCollatz` | Four entry claims | Mechanically identical to current submitted MPY, but proof build does not consume `solution.mpy`; reviewer identity check supplies the provenance bridge. |
| Trusted translator | Python-to-MPY identity | Fresh regeneration is byte-identical. |
| Trusted canonical implementation | Intent comparison | Agrees on ordinary tested inputs but diverges on two valid large positives because of float rounding. |
| Candidate prose induction | Alleged universal partial correctness | Illegitimate as a substitute for the missing K entry claim/invariant. |

### Not proven

- No theorem covers arbitrary positive input.
- No K invariant connects the initially empty accumulator with the odd prefix
  of an arbitrary Collatz trace.
- No claim relates real execution to `collatzResult`.
- No universal theorem establishes that `sortVS` is an ascending permutation.
- No universal equivalence to the trusted canonical is established; the
  differential has explicit large-positive counterexamples.
- Termination for every positive input is not claimed and would require
  resolving the Collatz conjecture.

The successful `#Top` results therefore certify seven narrower claims, not the
requested general partial-correctness property. Differential testing,
candidate notes, and a dead recurrence definition cannot fill that formal
gap.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
