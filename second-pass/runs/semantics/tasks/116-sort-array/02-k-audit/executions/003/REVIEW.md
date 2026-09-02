# Independent adversarial review: 116-sort-array

The reconstructed theorem is legitimate but has a material, non-fatal trust
limitation: it soundly proves that the real translated program returns the
supplied semantics' opaque `sortKeyVS(sortVS(...), keyClosure)` result, but the
mounted K theory contains no universal theorem that those opaque symbols mean
ascending and stable keyed sorting. The boundary is a fixed external Python
builtin in the supplied semantics, not a candidate-authored oracle or an
execution-bypassing local rule. The real program, full stated input domain,
result reference, heap content, and key closure are all constrained and
non-vacuous. Finite CPython and LLVM evidence supports the external sorting
contract but does not prove it.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`semantics_mode = SUPPLIED_SEMANTICS`, problem `116-sort-array`, and condition
`semantics`. I used the container paths in `/audit-input.json`, not its
host-only provenance paths.

All layout-required records are present, readable, regular mounted entries:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured trace;
- optional `usage.json`, which is present and was inspected;
- `/reference/canonical.py`, `/reference/prompt.py`,
  `/reference/py2mpy.py`, and `/reference/reference-semantics`;
- the complete `/candidate` mount.

Historical runtime metrics are absent, as permitted for this legacy layout; I
did not reconstruct them. The campaign lock is normalized-JSON identical to
the `audit_campaign` block and its SHA-256 is the recorded
`ad5dfcc006af...`. Every directly recorded file hash checked in
[integrity-check-rerun.log](evidence/stage1/integrity-check-rerun.log) matches,
including the run/task/result records, generation prompt/log/last/metrics/usage,
canonical, prompt, translator, and campaign lock.

The trace has one regular JSONL file and 163 structured records. Its individual
file digest `5b27883f...` matches the generation result and invocation records.
The independently reproduced pipeline tree digest is `be170771...`, matching
`usage.json`'s `source_trace_sha256`. The fresh candidate pipeline-tree digest
is `53cc1c94...`, exactly the retained workspace digest in
`generation-result.json` and `invocation.json`. The launcher also records
aggregate hashes made under other provenance conventions; I did not equate
those with a plain file or pipeline-tree digest. Direct type inspection and
recursive byte comparison are stronger for the mounted trees here.

The candidate prompt and translator are byte-identical to their trusted mounts.
The candidate `reference-semantics/` contains no symlinks or unsupported entry
types and recursively matches `/reference/reference-semantics` with no missing,
additional, renamed, mistyped, or changed entry. The independently reproduced
manifest digest for each tree is the recorded
`4e06397a1c5a...`. The required trusted semantics mount is present, consistent
with `SUPPLIED_SEMANTICS`. There is no infrastructure breach.

The generation logs and trace were inspected only as untrusted historical
claims. They report an initial parse failure, later builds, finite tests, and a
`#Top`; none was reused as proof evidence. Relevant artifacts:

- [mounted-inventory.log](evidence/stage1/mounted-inventory.log)
- [integrity-check-rerun.log](evidence/stage1/integrity-check-rerun.log)
- [tree-hashes.log](evidence/stage1/tree-hashes.log)
- [records-content.log](evidence/stage1/records-content.log)
- [trace-inspection.log](evidence/stage1/trace-inspection.log)
- [generation-log-inspection.log](evidence/stage1/generation-log-inspection.log)

Stage 1 result: integrity passes.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

`/reference/prompt.py` says `sort_array` accepts an array of non-negative
integers and orders them first by ascending number of `1` bits and, for equal
counts, by ascending decimal value. The domain is arbitrary finite lists and
arbitrary-size non-negative Python integers; it has no list-length or
integer-size bound.

The displayed examples conflict with that prose. In particular, `4` has one
set bit and `3` has two, so the prose requires `4` before `3`, while two
displayed examples use ordinary numeric order. The displayed negative example
is outside the expressly non-negative domain. The trusted canonical resolves
the intended in-domain behavior:

```python
return sorted(sorted(arr), key=lambda x: bin(x)[2:].count('1'))
```

On non-negative integers, the candidate's
`bin(value).count("1")` is equal to the canonical
`bin(value)[2:].count("1")`; the `"0b"` prefix contains no `1`. Both perform a
stable numeric pre-sort, so ties in popcount are resolved by decimal value.
The candidate's special negative branch differs from the canonical outside the
stated domain and happens to realize the prompt's negative display. This does
not narrow or alter the source-contract domain.

### Translation and differential reconstruction

Using the trusted `/reference/py2mpy.py` in scratch produced a byte-identical
`solution.mpy`; both files hash to
`9f5d29667fdd1adb62505f439ed2d11bf8db7408b3adeb35eeea3123b760f362`.
See [translation-identity.log](evidence/stage2/translation-identity.log).

The independent differential script imports the trusted canonical and the
candidate entry point by absolute scratch paths. It checks:

- empty, zero, and the `-1/0` implementation branch boundary;
- all prompt inputs, while separately recording the contradictory displays;
- duplicates, equal-popcount ties, powers of two and neighbors;
- integers through 512 bits;
- every list of length 0 through 4 over values `0..8`;
- 2,000 deterministic randomized lists of length up to 79 and values up to
  256 bits;
- input non-mutation.

All 9,390 intended-domain cases match; mismatch count is zero. Out-of-domain
negative divergences are printed rather than hidden. The script and complete
bounded result are
[differential_fidelity.py](evidence/stage2/differential_fidelity.py) and
[differential-results.log](evidence/stage2/differential-results.log).

Stage 2 result: the submitted implementation is faithful on the unrestricted
stated domain, and its submitted translation is authentic.

## 3. Clean proof reconstruction

I copied source artifacts only to `/tmp/audit-work/reconstruction`, using the
trusted semantics tree and translator, and confirmed that no `*-kompiled`
directory was present. No candidate cache or definition was reused. The live
toolchain is K `v7.1.293`.

Fresh commands and outcomes:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
Exit 0

krun concrete_audit.mpy --definition runtime-audit-kompiled
Exit 0; final <k> .K, <exc> NoExc, <exit-code> 0

kompile verification.k --backend haskell \
  --main-module SORT-ARRAY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
Exit 0

kprove spec.k --definition verification-audit-kompiled \
  --spec-module SORT-ARRAY-SPEC
Output #Top; exit 0
```

The independent concrete module covers empty/zero, prompt inputs under the
actual prose rule, duplicates, ties, powers, large integers, and the negative
branch. Its final heap records both inner and outer sort results and confirms
normal termination.

I also placed each submitted claim, unchanged except for its module wrapper,
in a separate scratch spec and reran it independently:

| Claim | Log | Outcome |
|---|---|---|
| Exact module loading | [kprove-claim-load.log](evidence/stage3/kprove-claim-load.log) | `#Top`, exit 0 |
| Universal end-to-end call | [kprove-claim-main.log](evidence/stage3/kprove-claim-main.log) | `#Top`, exit 0 |
| Universal non-negative key | [kprove-claim-key-nonnegative.log](evidence/stage3/kprove-claim-key-nonnegative.log) | `#Top`, exit 0 |
| Negative compatibility key | [kprove-claim-key-negative.log](evidence/stage3/kprove-claim-key-negative.log) | `#Top`, exit 0 |

Build and concrete logs are
[kompile-llvm.log](evidence/stage3/kompile-llvm.log),
[krun-concrete.log](evidence/stage3/krun-concrete.log), and
[kompile-haskell.log](evidence/stage3/kompile-haskell.log). Compiler warnings
are discussed in Stage 5; none is a failed positive claim.

Stage 3 result: every positive target claim closes independently from fresh
source with the required success signal.

## 4. Adequacy and real-program pinning

### Plain-language claims

1. With the standard empty module state, executing
   `#loadAll(sortArrayModule)` consumes the module and binds
   `"sort_array"` to `sortArrayClosure` in scope 0, leaving the other named
   cells unchanged.
2. For every finite `ValSeq` made only of non-negative K integers, calling the
   submitted function closure with `list(VS)` terminates at `ref(1)`. The
   inner numeric sort is allocated at heap 0 as `list(sortVS(VS))`; the
   returned outer result is allocated at heap 1 as
   `list(sortKeyVS(sortVS(VS), popcountKeyClosure))`; heap location advances
   from 0 to 2; stack, return, exception, scope, and exit cells return to their
   normal values.
3. For every `N >= 0`, calling the exact key closure returns the count of code
   49 (`"1"`) in `"0b" ++ binCodes(N)`, with no state or control change.
4. For every `N < 0`, the candidate's out-of-domain key closure returns 0.

These are reachability claims with concrete destination terms. The main result
is neither free nor existential: it must be `ref(1)`, and heap 1 must contain
the keyed-sort term. The claims do not use a one-way implication in place of a
required equality.

Every precondition is satisfiable. Ground witnesses include:

- claim 1's explicitly listed empty state;
- claim 2 with `VS = .ValSeq`, `vCons(0,.ValSeq)`, and
  `[7,3,5,6,9,8]`;
- claim 3 with `N = 0`, `1`, `7`, and a 128-bit integer;
- claim 4 with `N = -1` and `-5`.

For `[7,3,5,6,9,8]`, the formal intended result, trusted canonical, and
candidate all produce `[8,3,5,6,9,7]`. More substitutions are recorded in
[satisfying-witnesses.log](evidence/stage4/satisfying-witnesses.log).

### Mechanical program identity

The candidate does not merely change an external `solution.mpy` file while
proving a fixed unrelated term. A reviewer-authored constructor parser:

1. parses the trusted-regenerated `solution.mpy`;
2. parses and expands `sortArrayLambda`, `sortArrayBody`, and
   `sortArrayModule` from `verification.k`;
3. normalizes only `CellVars()`/`FreeVars()` to K's explicit empty
   `.ParamNames` constructor;
4. compares the complete module and function-body trees.

Both module and body comparisons are `True`; the complete normalized trees are
in [constructor-comparison.log](evidence/stage4/constructor-comparison.log).
The load claim independently proves that fixed semantics installs the same
function binding. The main claim calls that exact closure.

A separate body-sensitivity experiment changes the executed
`sortArrayBody`—and therefore both `sortArrayClosure` and
`sortArrayModule`—to `Return(Int(0))`, recompiles successfully, and reruns the
main claim. It exits 1 with `WarnStuckClaimState` at `<k> 0`, rather than the
required sorted reference. See
[body-mutation-diff.log](evidence/stage4/body-mutation-diff.log),
[body-mutation-kompile.log](evidence/stage4/body-mutation-kompile.log), and
[body-mutation-kprove.log](evidence/stage4/body-mutation-kprove.log).

Stage 4 result: the theorem pins the real translated binding and body over the
entire stated domain, and its result is constrained. Its interpretation as an
ordered list remains conditional on the supplied primitives described below.

## 5. Rule-by-rule static soundness review

The exhaustive source inventory is
[full-rule-inventory.log](evidence/stage5/full-rule-inventory.log). It records
all 1,231 declarations from the assembler, all 23 supplied helper files,
`verification.k`, and `spec.k`, including:

- 704 rules: 238 touching `<k>` and 466 equational;
- 234 syntax records, 153 function declarations, and 114 `total`
  declarations;
- 34 priority, 47 `concrete`, and 29 `owise` rules;
- 25 `symbol` declarations;
- four claims and one configuration;
- zero simplification rules.

[static-assessment.md](evidence/stage5/static-assessment.md) gives a
file-by-file disposition covering every inventory record, then maps every
constructor used by `solution.mpy` to its declaration and operational rules.
The critical path is:

```text
module load -> closure call/frame -> bind arr -> lookup sorted
-> evaluate inner sorted(arr) -> allocate heap 0
-> evaluate exact annotated key lambda
-> outer keyed sorted -> allocate heap 1
-> return ref(1) -> pop frame
```

The helper key path additionally follows integer comparison, complementary
`IfExp` guards, `bin`, string construction, attribute/method binding, and the
terminating `cntSub` scan. Relevant call/return rules preserve environment,
stack, scope, heap allocation, return, exception, and exit cells. Evaluation is
left-to-right. Priority rules used on this path only dereference heap objects
or select the LLVM concrete keyed sorter; their guards and state footprints are
consistent with the operations they preempt.

### Candidate-authored theory

All nine candidate equations are truthful definitions:

- four exact constructor names for the lambda, function body, closure, and
  module;
- one exact constructor for the evaluated key closure;
- one postcondition abbreviation,
  `sortArraySpec(VS) = sortKeyVS(sortVS(VS), popcountKeyClosure)`;
- three complete, disjoint, structurally recursive equations for
  `allNonNegativeInts`.

They do not match or replace an executing `Call`, have no priority or
simplification attribute, introduce no fresh/opaque value, and do not encode a
different program. Totality is complete over every actual use. The module-load
and key reachability claims supply independent fixed-semantics connections for
the two manually named closures. No candidate rule can enable a concrete false
conclusion on an intended input.

### Supplied opaque sorting boundary

The proof definition intentionally leaves these fixed-semantics symbols
opaque:

```k
sortVS(ValSeq)
sortKeyVS(ValSeq, Val)
```

They are total, result-bearing, `no-evaluators` symbols. The ordinary and keyed
`sorted` rules allocate lists containing them. This is an external primitive
boundary for Python's builtin `sorted`, not a candidate extension and not a
program-defined helper. The theorem is sound under every interpretation: it
claims exactly that execution returns those primitive applications.

The semantic comments say they mean ascending and stable keyed sorting, and
`MPY-CONCRETE` supplies a separate LLVM-only insertion-sort implementation
that calls the real key closure. The ascending insertion rule places a new
element after equal keys, so it is stable. Fresh K execution agrees with
CPython on 85 cases: nine named boundary/large/tie cases, all length-two lists
over `0..5`, and 40 deterministic randomized lists. See
[k-differential-generate-bounded.log](evidence/stage5/k-differential-generate-bounded.log)
and
[k-differential-bounded-krun.log](evidence/stage5/k-differential-bounded-krun.log).
A first 400-case K parse exceeded the 8 GiB container limit before execution
(exit 137), recorded in
[k-differential-krun.log](evidence/stage5/k-differential-krun.log); this
resource failure is not treated as a proof defect or success.

There is no mounted, bridge-free universal K connection theorem equating the
opaque Haskell symbols with the concrete twin or proving ordering, permutation,
stability, and exact key invocation. The separate key claim proves what the
closure computes when called; it does not prove `sortKeyVS` calls it. Finite
tests cannot close that universal gap. Accordingly, the natural-language
ordering conclusion is conditional on the named supplied primitive contract.
This is the reason for `CONCERNS`, rather than `PASS`.

The LLVM compiler reports non-exhaustive total-function patterns for
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. None occurs
on the submitted proof path. The Haskell proof build reports only unused
variables in disjoint `strLt` branches. An inactive reverse-sort branch reverses
the complete concrete sequence and therefore is not a full CPython model of
stability among equal keys under `reverse=True`; the submitted program never
constructs a `reverse` keyword, so no intended-domain input can expose that
branch. I record it as an unused minimal-semantics limitation, not an
unsoundness witness for this theorem.

Stage 5 result: no candidate-authored unsoundness, answer rule, unconstrained
local oracle, or execution bypass exists. The fixed external sorting opacity
is sound as a conditional boundary but lacks universal validation of its
human-facing meaning.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was relied on. I created two fresh mutations in
scratch and preserved them under `evidence/stage6/`.

The primary, content-level mutation keeps the actual return `ref(1)` but
changes heap 1 from

```k
list(sortKeyVS(sortVS(VS), popcountKeyClosure))
```

to the false alternative:

```k
list(sortVS(VS))
```

It is demonstrably false for the satisfying input `VS = [3,4]`: decimal
pre-sort is `[3,4]`, while the prose rule, canonical, and candidate produce
`[4,3]`. The mutated spec dry run exits 0, establishing successful parsing and
build. Its proof exits 1 with `WarnStuckClaimState`; the residual is precisely
the unmet equality between `sortKeyVS(sortVS(VS), keyClosure)` and
`sortVS(VS)`. It is not a parse error, missing import, timeout, unrelated
crash, or unreachable mutation.

Evidence:

- [spec-vacuity-content.k](evidence/stage6/spec-vacuity-content.k)
- [content-mutation-diff.log](evidence/stage6/content-mutation-diff.log)
- [content-mutation-dry-run.log](evidence/stage6/content-mutation-dry-run.log)
- [content-mutation-kprove.log](evidence/stage6/content-mutation-kprove.log)
- [mutation-witness.txt](evidence/stage6/mutation-witness.txt)

An independent allocation-result mutation from `ref(1)` to `ref(0)` also
builds and fails with the expected `<k> ref(1)` residual; it is secondary
corroboration in [mutation-kprove.log](evidence/stage6/mutation-kprove.log).

Stage 6 result: the proof discriminates both returned object identity and
result content.

## 7. Proven versus assumed accounting

### Machine-proven under the supplied theory

- The trusted-regenerated submitted module loads and installs the exact
  `sort_array` closure.
- For every finite list of arbitrary-size non-negative integers, fixed
  symbolic execution of the exact submitted body consumes the call, restores
  normal control/state cells, allocates exactly two result objects, and returns
  the outer object.
- That object's formal content is exactly
  `sortKeyVS(sortVS(VS), popcountKeyClosure)`.
- Executing the exact key closure on every non-negative integer returns the
  count of `"1"` in its fixed-semantics binary representation.
- The candidate's extra negative branch returns key 0 for every negative
  integer.
- The result and body are non-vacuous under both body and postcondition
  mutations.

### Trusted or informal boundaries

| Boundary | Influence | Status and evidence |
|---|---|---|
| `sortVS` supplied primitive | Intermediate decimal ordering and therefore final tie order | External fixed builtin contract; opaque in Haskell. Concrete twin and finite K/Python tests support it, but no universal K connection theorem is mounted. Concerning but not illegitimate. |
| `sortKeyVS` supplied primitive | Entire returned permutation, ordering, stability, and whether/how the key is called | External fixed builtin contract; opaque in Haskell. This is the principal concern. The formal theorem stays conditional and cannot prove an unrelated concrete result. |
| `MPY-CONCRETE` keyed-sort twin | Empirical bridge from executable K behavior to CPython | Real key calls and stable ascending insertion; 85 fresh cases pass. It is a different imported module from the proof definition, so finite agreement is evidence only. |
| Trusted translator | Source-to-constructor identity | Trusted regeneration is byte-identical; independent constructor comparison pins the proof term. Acceptable. |
| Supplied operational subset | Calls, lookup, allocation, closure/frame, integer/string/bin/count behavior | Fixed trusted semantics, reviewed rule-by-rule on the actual path and exercised concretely. No material path discrepancy found. |
| Prose/canonical intent choice | Resolves contradictory displayed examples | The prose domain/order and trusted canonical agree on all in-domain tests; contradictory displays are documented. No domain restriction was introduced. |
| K toolchain/backend | Compiler and prover correctness | Standard trusted verification tool boundary, version recorded, with fresh builds and mutations. |

The candidate's historical prose, traces, previous `#Top`, and differential
tests are not used as substitutes for the reachability proof. The independent
differentials support only source fidelity and the finite concrete bridge.

### Decision

This is not `FAIL`: the proof reconstructs, is non-vacuous and
result-constraining, mechanically pins the real program, and universally
covers the full non-negative-integer-list source domain. It does not prove a
substituted program, bounded sizes, or examples only. No candidate rule enables
a false conclusion.

This is not `PASS`: the central human-facing meaning of the returned opaque
sorting terms has no universal connection theorem in the mounted theory. The
limitation is precisely the kind of fixed external trust/evidence boundary
allowed by `CONCERNS / LEGIT`: the theorem remains sound and conditional and
does not fabricate a concrete answer under an arbitrary interpretation.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
