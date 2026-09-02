# Independent adversarial audit: 120-maximum

The candidate contains a legitimate partial-correctness proof of its submitted
program under the supplied semantics. The result is `CONCERNS / LEGIT`, not an
unqualified pass, because the Haskell proof treats the supplied `sortVS`
operation as an opaque external sorting primitive. K proves that the program
returns the requested suffix of that primitive, but K does not prove that the
primitive is an ascending permutation. That bridge is named, fixed by the
supplied-semantics boundary, mathematically appropriate, and supported by
finite independent tests; it is not a proof-local oracle or execution bypass.
Generation-provenance files are also absent.

All execution and mutation work was performed in
`/tmp/audit-work/120-maximum`. No candidate-provided compiled definition or
cache was used. Reviewer-authored artifacts and bounded logs are under
`/audit-output/evidence/`.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` exists as a real directory. There is no
infrastructure contradiction, so a candidate verdict is appropriate.

The non-following manifest comparison found 25 entries in each semantics tree
and zero missing, extra, changed, mistyped, or symlinked candidate entries.
The candidate `prompt.py` and `py2mpy.py` are regular files and match their
trusted counterparts:

- `prompt.py` SHA-256:
  `360323c0b48ab9ab91ecd91655e881eb66140b4822d73cc5e6e40c9e2ae6ab82`
- `py2mpy.py` SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

Evidence: `evidence/integrity_audit.py` and
`evidence/stage1-integrity.log` (exit 0).

### Artifact and provenance findings

The regular source artifacts needed to reconstruct the proof are present:
`solution.py`, `solution.mpy`, `spec.k`, `verification.k`, the prompt,
translator, and complete `reference-semantics/` tree. No required source is a
symlink.

The following requested provenance artifacts are absent:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`
- any structured generation trace

There is also no candidate `PROOF.md` or `spec-vacuity.k`. The candidate instead
contains `prove.sh`, `prove.log`, concrete smoke files, a Python bytecode cache,
and the proof sources. I inspected these only as untrusted claims. The
candidate log claims `#Top`, but no later conclusion relies on that log or its
build products.

Evidence: `evidence/stage1-untrusted-claims.log`, which records the complete
candidate manifest, file hashes, claimed command script, claimed log, and
provenance search. The missing provenance limits auditability but does not
remove or alter the independently reconstructible proof.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From the trusted prompt and canonical implementation, the intended return-value
contract is:

- `arr` has 1 through 1000 integer elements, each from -1000 through 1000;
- `0 <= k <= len(arr)`;
- return an ascending list of length `k` containing the largest `k` values,
  preserving duplicates;
- when `k == 0`, return `[]`.

The canonical implementation sorts `arr` in place and returns its `-k:`
suffix, with a special `k == 0` branch. The submitted program uses
`sorted(arr)` and the same suffix. Thus it does not mutate its input, unlike
the canonical implementation. The stated task constrains the returned list,
not input mutation, so this is not a contract divergence.

### Trusted translation

I regenerated `solution.mpy` from the scratch-copied `solution.py` with the
trusted mounted translator. `cmp --verbose` found byte identity; both files
are 264 bytes and have SHA-256
`d74f6342b2088b38daf852a3b75cb63a2eda931babf6bf77877779322f964556`.

Evidence: `evidence/stage2-translation.log` (exit 0).

### Independent differential test

`evidence/differential_test.py` independently imports the trusted canonical
entry point and submitted entry point. It also checks a separately stated
return-value oracle and sortedness/length/multiplicity invariants. Its 22,735
cases comprise:

- all three documented examples;
- empty, singleton, extrema, duplicate, `k=0`, `k=1`, `k=n-1`, `k=n`, and
  length-1000 boundaries;
- every array of length 0 through 5 over `{-2,-1,0,1,2}`, with every valid
  `k`;
- 256 deterministic generated arrays of length 1 through 1000 with values in
  the documented range.

The run found zero result mismatches and zero invariant failures. It recorded
17,738 canonical input mutations and zero candidate input mutations, confirming
the known non-contract side-effect difference. All concrete inputs are
preserved in `evidence/stage2-inputs.jsonl` (22,735 lines, SHA-256
`22e836603c9a202e3f744882b06487f2138e7990b312f2735a6239a35e3f14a8`).

Evidence: `evidence/stage2-differential.log` (exit 0).

## 3. Clean proof reconstruction

The scratch tree was created from source artifacts only. Candidate bytecode,
compiled definitions, and caches were not copied or reused. The toolchain was
K v7.1.337 (2026-06-18 build) and Python 3.10.12; see
`evidence/stage7-toolchain.log`.

### Concrete definition and execution

I freshly built the concrete definition:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

It exited 0. The submitted `solution.mpy` then loaded under `krun` and ended
with `.K`, `NoExc`, and exit code 0. A reviewer-authored, trusted-translated
boundary harness exercised empty, zero, singleton, examples, extrema,
`k=1`, `k=n-1`, and `k=n`; it also ended with `.K`, `NoExc`, and exit code 0.

Evidence:

- `evidence/stage3-build-llvm.log`
- `evidence/stage3-krun-submitted.log`
- `evidence/stage3-concrete-harness.py`
- `evidence/stage3-artifact-preparation.log`
- `evidence/stage3-krun-harness.log`

All commands exited 0.

### Proof definition and every positive claim

I freshly built the proof definition:

```text
kompile verification.k --backend haskell \
  --main-module MAXIMUM-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

The build exited 0. I ran the original aggregate spec and reviewer-labeled
copies of each claim separately:

| Target | Result |
|---|---|
| original `MAXIMUM-SPEC` | exit 0, `#Top` |
| isolated `k == 0` claim | exit 0, `#Top` |
| isolated `0 < k <= len(arr)` claim | exit 0, `#Top` |

The labeled specs reproduce the original claims without changing their
configurations, guards, or destinations.

Evidence:

- `evidence/stage3-build-haskell.log`
- `evidence/stage3-kprove-original-aggregate.log`
- `evidence/stage3-spec-k0.k`
- `evidence/stage3-kprove-k0.log`
- `evidence/stage3-spec-k-positive.k`
- `evidence/stage3-kprove-k-positive.log`

The compiler's non-exhaustiveness warnings are addressed in Stage 5; they did
not replace a failed proof with `#Top`.

## 4. Adequacy and real-program pinning

### `k == 0` entry claim

Precondition in plain language: the call begins in the pinned module
environment with `maximum` bound to the exact two-parameter closure; `k` is
literally 0; the argument is an arbitrary `list(VS)`; the heap and stack are
empty; allocation begins at 0; no return or exception is pending. There is no
additional `requires` clause.

Postcondition in plain language: the call returns `ref(0)`, heap location 0
holds a newly allocated empty list, the allocation counter becomes 1, and the
environment, scopes, stack, return state, and exception state are restored.
The result is exact, not existential or free.

A satisfying witness is `arr=[7,-2], k=0`. The formal returned heap object,
trusted canonical result, and candidate result are all `[]`.

### Positive entry claim

Precondition in plain language: the same complete pinned call state holds, with
an integer `K` satisfying `0 < K <= vsLen(VS)`.

Postcondition in plain language: `sorted` allocates at heap location 0 the
supplied abstract ascending permutation `list(sortVS(VS))`; slicing allocates
at heap location 1:

```text
list(buildVS(sortVS(VS), vsLen(VS)-K, vsLen(VS), 1))
```

The call returns exactly `ref(1)`, the counter becomes 2, and call-frame state
is restored. This fixes both the returned reference and every element term in
the returned object.

A satisfying witness is `arr=[-3,-4,5], k=2`. The guard is true, heap 0 is
`[-4,-3,5]`, heap 1 is `[-3,5]`, and the canonical, candidate, and substituted
formal return all equal `[-3,5]`.

Evidence: `evidence/stage4-witnesses.py` and
`evidence/stage4-witnesses.log` (exit 0).

### Program identity and control flow

The entry claims start at an invocation rather than replaying module loading,
but they do not substitute a summary for the function. Scope 0 contains a
closure whose parameter list and body are the `maximumBody` macro. That macro
is the same AST emitted in the byte-identical submitted `solution.mpy`.
`stage3-krun-submitted.log` independently shows the module loader creating the
same `closureVal`.

The fixed semantics executes normal callee lookup, left-to-right argument
evaluation, parameter binding, integer comparison, branch selection, builtin
lookup, `sorted` allocation, negative-bound slice evaluation, slice allocation,
return, and frame pop. There is no loop, helper claim, direct result rewrite,
or omitted program-defined operation.

The formal domain omits the prompt's length/value bounds and does not constrain
`VS` elements to integers. This is stronger on finite intended integer inputs
and does not exclude any documented case. Behavior of Python-invalid
heterogeneous sequences is not used to claim intent coverage.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/rule_inventory.py` generated a full multiline JSONL inventory and a
line-addressed Markdown index:

- 25 K files;
- 931 top-level K items;
- 697 rules: 695 in the byte-identical supplied definition and 2 proof-local;
- 228 syntax declarations: 227 supplied and 1 proof-local;
- 5 contexts and 1 configuration;
- 145 function-tagged items, 107 total-tagged items, and 0
  functional-tagged items;
- 25 opaque `symbol` items, 22 of them `no-evaluators`;
- 45 priority-tagged, 35 concrete-tagged, 5 macro-tagged, and 1
  simplification-tagged item.

Every item has its source span, attributes, class, decision, and rationale in
`evidence/stage5-rule-inventory.jsonl`. The compact complete list and per-file
hashes/counts are in `evidence/stage5-rule-inventory.md`. The supplied entries
are classified `ACCEPTED_SELECTED_SEMANTICS` because the problem's mode makes
the byte-identical mounted tree the selected fixed semantics, not a
candidate-authored proof extension. This classification does not extend to
`verification.k`.

`evidence/stage5-used-construct-map.md` maps every submitted syntactic
construct to its declaration and records the complete used rule path,
configuration cells, order, binding, allocation, state changes, return
control, overlaps, priorities, guards, totality, and proof-local decisions.

### Proof-local rules

1. `maximumBody` (`verification.k:8-17`) is an exact syntax macro. It reads or
   writes no cell and does not preempt fixed execution. Its expansion matches
   the submitted translated body. It is sound.
2. `vsLen(sortVS(VS)) => vsLen(VS)` (`verification.k:22`,
   `[simplification]`) is a mathematical lemma about the supplied external
   sorting primitive. A sorting permutation preserves length, so the equation
   is true on the intended integer-list domain and for every domain on which
   `sortVS` denotes a permutation. It affects only negative-slice
   normalization; it neither chooses sorted values nor replaces program
   control/state. Its truth is conditional on the supplied `sortVS` contract,
   which is the central documented concern.

There is no proof-local helper function, `total` declaration, opaque symbol,
priority rule, operational bridge, result oracle, loop claim, or auxiliary
claim. Therefore no bridge context or state footprint is hidden.

### Body sensitivity

I rebuilt a separate definition after changing only the positive branch body
to return an empty list. The mutated definition built successfully. The
positive proof then exited 1 with `WarnStuckClaimState`; its residual had
`ref(0)`, heap 0 empty, and allocation counter 1 instead of the required
`ref(1)` and two heap objects. This is a body-sensitive unmet obligation, not a
parser failure.

Evidence:

- `evidence/stage5-verification-body-mutation.k`
- `evidence/stage5-body-mutation-build.log` (exit 0)
- `evidence/stage5-body-mutation-spec.k`
- `evidence/stage5-body-mutation-proof-valid.log` (exit 1, expected residual)

An earlier attempt in `stage5-body-mutation-proof.log` imported both original
and mutated modules and was rejected by the parser. It is retained as a failed
setup attempt and is not counted as body-sensitivity evidence.

### Totality and opaque-value findings

Fresh builds warn about non-exhaustive supplied functions including
`mapStrVS`, several float helpers, `joinCodes`, and `valSeqAt`. The only one on
this program's proof path is `valSeqAt`. It is intentionally total and
abstract when applied to symbolic `sortVS(VS)`. Under
`0 < K <= vsLen(VS)` plus length preservation, all generated indices are in
the intended range. The same exact abstract element terms occur in execution
and the postcondition.

This does not prove those elements are the largest values. That value-level
fact depends on the fixed `sortVS` contract, accounted for in Stage 7. I found
no materially unsound candidate rule and therefore make no unsoundness
allegation requiring a false-conclusion witness.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was available. I created a fresh positive-claim
mutation that changes the result slice start from `len(VS)-K` to
`len(VS)-K+1`, while keeping the actual program, returned reference, and
reachable positive branch unchanged.

The concrete satisfying witness `arr=[-3,-4,5], k=2` has:

- true result `[-3,5]`;
- mutated result `[5]`;
- a satisfied positive precondition.

The mutated spec completed `kprove --dry-run` with exit 0, establishing that it
parses and builds against the original proof definition. Full `kprove` exited
1 and emitted `WarnStuckClaimState`. The residual shows the actual heap object
still begins with
`valSeqAt(sortVS(VS), vsLen(VS)-K)`, while the false destination omits that
element. This is the expected unmet result obligation.

Evidence:

- `evidence/stage6-spec-vacuity.k`
- `evidence/stage6-mutation-witness.py`
- `evidence/stage6-mutation-witness.log` (exit 0)
- `evidence/stage6-mutation-dry-run.log` (exit 0)
- `evidence/stage6-mutation-proof.log` (exit 1, expected stuck implication)

The positive proof is therefore result-constraining and non-vacuous.

## 7. Proven versus assumed accounting

### What the K reachability proof establishes

Under the supplied K definition and the exact entry states:

- when `k=0`, the submitted function body returns a newly allocated empty list;
- when `0<k<=vsLen(VS)`, it calls the supplied `sorted` builtin, then returns a
  new list containing exactly positions `vsLen(VS)-k` through
  `vsLen(VS)-1` of `sortVS(VS)`;
- call binding, branch control, both allocations, returned references, heap
  contents, frame restoration, stack, return state, and exception state have
  the post-state shown in the claims.

This is a partial-correctness result for the real submitted body. It is not a
universal proof of CPython, the frontend translator, or the sorting
implementation.

### Trust and assumption ledger

1. **Supplied semantics.** The 695 rules, 227 syntax declarations, contexts,
   and configuration in the mounted reference tree are the authority-selected
   semantics for this mode. Integrity was checked exactly. The result depends
   on the used call/control/list/slice/sort subset; unused imported rules do
   not contribute to closure.
2. **Used opaque symbol: `sortVS`.** In Haskell proofs it is a total opaque
   symbol. The positive claim and the proof-local length lemma depend on the
   contract “ascending permutation of the input sequence.” The LLVM definition
   has concrete insertion-sort rules for integer lists, but those concrete
   equations are not a universal Haskell proof of the opaque contract.
3. **Other imported opaque symbols.** `sortKeyVS`, `md5hexCodes`,
   `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
   `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
   `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and
   `sqrtF` are present in the selected semantics but unreachable from this
   program and do not affect either claim.
4. **K implementation boundary.** K's compiler, parser, Haskell prover, LLVM
   runtime, and builtin integer/Boolean/map/list/string theories are trusted.
5. **Frontend bridge.** The trusted mounted translator is not proved correct
   in K. For this program its output comparison is exact rather than sampled:
   regeneration is byte-identical. The proof macro and loaded closure AST were
   also compared, and body sensitivity was demonstrated.
6. **Intent bridge.** Ordinary mathematics supplies: the final `k` elements of
   an ascending permutation are the maximum `k` elements in ascending order.
   This conclusion is conditional on item 2.
7. **Empirical bridges.** The 22,735-case Python differential and reviewer K
   boundary harness support candidate/canonical result agreement and concrete
   semantics behavior only on their recorded inputs. They do not prove the
   opaque sort contract or replace the reachability proof.
8. **Excluded behavior.** The claims do not model CPython exceptions for
   invalid `k`, non-integer/mutually incomparable elements, alias-sensitive
   input mutation, or resources. These are outside the documented intended
   input/return contract.

### Decision

Gate A (real-program soundness and non-vacuity) passes: source-only claims
close, the actual body executes, state/result are constrained, no unsound
proof-local bridge exists, and both body and postcondition mutations are
rejected for the expected obligations.

The natural-language intent is covered on the documented integer domain
conditional on the supplied `sortVS` contract. The opaque sorting bridge and
finite-only evidence for it are a material limitation in what K itself proves,
and the requested generation-provenance records are missing. They warrant
`CONCERNS`, but not `FAIL`: the abstraction is a fixed external builtin from
the trusted supplied semantics, is explicitly named, does not replace
program-defined code, and cannot be freely chosen by the candidate to force a
false postcondition.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
