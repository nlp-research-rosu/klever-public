# Independent adversarial audit: 37-sort-even

This audit used the required `using-kit` and `validating-proof` procedures.  The
candidate was treated as untrusted and read-only.  Every executed source was
copied to `/tmp/audit-work/37-sort-even-audit`; candidate caches and compiled
artifacts were not reused.  Reviewer scripts and bounded logs are under
[`evidence/`](evidence/).

The final assessment is **CONCERNS / LEGIT**.  Both proof claims reconstruct and
close, the theorem executes an exact transcription of the submitted program,
the result is constrained, and fresh body/postcondition mutations are rejected.
The concerns are evidence/trust limitations rather than witnessed unsoundness:
the supplied semantics makes `sortVS` an opaque trusted primitive, a small
administrative binding specialization lacks a closing bridge-free Haskell
connection proof, and the candidate omitted the requested generation/provenance
records.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and the trusted mount
`/reference/reference-semantics` is present.  There is therefore no
mode/mount contradiction and no infrastructure breach.

The recursive, no-symlink comparison found:

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (`sha256 82b621b23095040636b376f49469c4fc1d951c6563fed5aae1f5460f60ba7696`).
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (`sha256 406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- `diff -qr --no-dereference` over the trusted and candidate
  `reference-semantics/` trees exits 0.  Every entry is a regular file or
  directory of the same type; there are no candidate semantics symlinks,
  additions, removals, or byte changes.
- `solution.py`, `solution.mpy`, `spec.k`, and `verification.k` are regular
  files, not symlinks.

The candidate does **not** contain `run-input.json`, `metrics.json`,
`codex-last.txt`, or `codex-output.log`, and no structured generation trace was
present.  These are provenance/integrity omissions.  No candidate `PROOF.md`
was present either, so no prose proof claim was relied on.  The candidate
`__pycache__` was identified and ignored.

Commands, entry types, individual missing-file statuses, hashes, and the full
semantics-tree comparison are recorded in
[`stage1-integrity.sh`](evidence/stage1-integrity.sh) and
[`stage1-integrity.log`](evidence/stage1-integrity.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt requires `sort_even(l)` to return a list of the same
structure such that:

1. values at odd indices are unchanged; and
2. values originally at even indices are placed back at the even indices in
   ascending order.

The canonical implementation takes `l[::2]`, sorts that copy, takes `l[1::2]`,
alternates the two subsequences, and appends the unmatched final even element
for odd-length inputs.

The submitted implementation uses `sorted(l[::2])`, iterates over the odd
subsequence while appending one sorted-even and one unchanged-odd value, then
concatenates `evens[len(odds):]`.  This is a different but equivalent algorithm
for lists whose elements are mutually sortable.  Neither implementation
mutates the input list.

### Trusted translation

From the scratch copy, the command

```text
python3 ../trusted/py2mpy.py solution.py > ../regenerated-solution.mpy
```

exited 0.  `cmp -s solution.mpy ../regenerated-solution.mpy` exited 0; both
files have SHA-256
`fd4ff5d27b4f28364c69a9794290cfa53b00c3040f3fc10c09c26daeac68659c`.
See [`stage2-program.log`](evidence/stage2-program.log).

### Independent differential

[`differential_test.py`](evidence/differential_test.py) loads the trusted
canonical and scratch candidate as separate modules and compares both return or
exception outcomes and post-call input state.  Its complete deterministic
corpus is preserved in
[`differential-inputs.json`](evidence/differential-inputs.json):

- both documented examples;
- nine explicit empty, length-parity, duplicate, negative, and large-integer
  boundary cases;
- all 19,531 lists of lengths 0 through 6 over
  `[-2, -1, 0, 1, 2]`; and
- 512 generated lists using seed `370037`, lengths 0 through 40, values
  `[-1000, 1000]`.

The run executed 20,054 inputs per implementation and reported zero result,
exception, or mutation mismatches (exit 0).  This is strong finite evidence for
the intended integer-list domain, not a substitute for the K proof.

## 3. Clean proof reconstruction

K version `v7.1.337` and Python `3.10.12` were used; see
[`environment.log`](evidence/environment.log).

A fresh reconstruction directory was populated only with candidate source
artifacts and the independently copied trusted semantics.  No precompiled
candidate definition existed or was used.

The following fresh commands all succeeded:

| Operation | Result | Evidence |
|---|---|---|
| LLVM `kompile reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX` | exit 0 | [`stage3-kompile-llvm.log`](evidence/stage3-kompile-llvm.log) |
| `krun solution.mpy` | exit 0; module loaded to the expected `sort_even` closure | [`stage3-krun-solution.log`](evidence/stage3-krun-solution.log) |
| `krun concrete-tests.mpy` | exit 0; all five assertions passed | [`stage3-krun-tests.log`](evidence/stage3-krun-tests.log) |
| Haskell `kompile verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX -I .` | exit 0 | [`stage3-kompile-haskell.log`](evidence/stage3-kompile-haskell.log) |
| `kprove` selecting only `SPEC.loop-correct` | exit 0 and `#Top` | [`stage3-kprove-loop.log`](evidence/stage3-kprove-loop.log) |
| `kprove` selecting the loop and entry claims, with the separately proved loop claim supplied as the loop lemma | exit 0 and `#Top` | [`stage3-kprove-entry.log`](evidence/stage3-kprove-entry.log) |

The entry command's `--trusted SPEC.loop-correct` is proof composition, not an
unproved assumption in this audit: the exact same claim closed independently,
under the exact same fresh definition, immediately beforehand.

The build emitted reference-semantics warnings about deliberately total,
non-exhaustive functions such as `valSeqAt`; these are accounted for below.
They did not prevent either build or either target claim from closing.

## 4. Adequacy and real-program pinning

### `loop-correct`

The loop claim's precondition says: execution is at the iterator step for an
unconsumed list suffix `OVS`, followed by the real loop-step marker and an
arbitrary continuation `K`; the current scope has the real locals `l`, `evens`,
`odds`, `result`, `i`, and `odd`; and the three referenced heap objects contain
`EVS`, `OALL`, and accumulated result `ACC`.

Its postcondition says: the loop has completed and continuation `K` remains;
`i` is increased by the length of `OVS`; `odd` may contain the last bound value;
the result list is `ACC` followed by the pair sequence formed from
`EVS[I], OVS[0], EVS[I+1], OVS[1], ...`; and the even list, odd list, unrelated
scope entries, and unrelated heap entries are preserved.  No relationship
between `OVS` and `OALL` is needed for this local execution theorem.

A concrete satisfying loop state exists, for example `OVS = .ValSeq`,
`I = 0`, empty `EVS`/`OALL`/`ACC`, distinct heap locations for the three lists,
and `K = .K`.  It takes the supplied `#iterDone` rule and satisfies the
unchanged post-state.

### `sort-even-correct`

The entry precondition has no explicit `requires`.  It universally quantifies
`VS:ValSeq` and starts from:

- `Call(Name("sort_even"), list(VS)) ~> #observeResult`;
- module environment 0 with `sort_even |-> sortEvenClosure`;
- the exact supplied builtins scope at `-1`;
- fresh scope/heap counters, empty heap and stack, `noRet`, `NoExc`, and exit 0.

The postcondition forces the `<k>` result to the structural value

```text
list(assembledEvenSort(sortVS(evenIndices(VS)), oddIndices(VS)))
```

It is not a free result variable, tautology, or one-way implication.  Heap
addresses and the final heap counter are existential because list construction
allocates, but `#observeResult` dereferences the returned list, so those fresh
addresses cannot satisfy an incorrect result.

### Pinning to the submitted body

The spec does not load `solution.mpy` by filename.  Instead it invokes
`sortEvenClosure`, whose `sortEvenBody` is an exact constructor-for-constructor
transcription of the function body in the byte-verified `solution.mpy`.
Fresh concrete module loading independently produced the same closure body in
[`stage3-krun-solution.log`](evidence/stage3-krun-solution.log).

This manual transcription was also tested for body sensitivity.  In a separate
fresh definition, the reviewer changed the real loop body's second append from
`odd` to `999`.  The mutated definition built, but the original loop claim
failed with a residual containing `vCons(999, ...)` where `pairedVS` required
the actual odd value.  See
[`verification-body-mutation.k`](evidence/verification-body-mutation.k),
[`stage4-body-sensitivity.log`](evidence/stage4-body-sensitivity.log), and
[`stage4-body-mutation-proof.log`](evidence/stage4-body-mutation-proof.log).
Thus claim closure is sensitive to the property-bearing program body.

### Satisfying entry witnesses

[`ground_witness.py`](evidence/ground_witness.py) substituted `[]`, `[7]`,
`[5, 6, 3, 4]`, and `[9, -1, 3, -2, 3, -3, 0]` into the claimed assembly
formula and both Python implementations; all four agreed.  The reviewer-authored
ground K claim for `[5, 6, 3, 4] => [3, 6, 5, 4]` also exited 0 with `#Top`.
See [`spec-ground.k`](evidence/spec-ground.k) and
[`stage4-ground.log`](evidence/stage4-ground.log).

The formal domain is broader than the well-supported Python intent: it admits
arbitrary `ValSeq`, while the supplied concrete `sortVS` supports integer and
string lists and actual Python sorting may reject heterogeneous values.  The
proof is soundly parametric in its opaque sort term, but the natural-language
adequacy evidence is strongest for integer lists.  This is a concern, not a
false theorem on the intended integer domain.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[`k-rule-inventory.txt`](evidence/k-rule-inventory.txt), with full source blocks
and metadata in
[`k-rule-inventory.json`](evidence/k-rule-inventory.json).  The generating
script found 956 records across all 26 K files:

```text
236 syntax declarations
712 rules
5 contexts
1 configuration
2 claims
154 function-tagged records
116 total-tagged records
22 no-evaluators records
47 priority-tagged records
3 simplification rules
0 functional declarations
```

Every record is dispositioned by source module, and every one of the 26
`verification.k` records is assessed individually, in
[`static-rule-assessment.md`](evidence/static-rule-assessment.md).

### Used-construct map

| Submitted construct | Declaration and operative rules |
|---|---|
| `Module`, statement sequence, `FuncDef` | `syntax.k`; `core.k` load/sequence; `functions.k` closure creation |
| `Call`, `Name`, parameter binding, return | `call.k`, `core.k`, `functions.k`, plus the exact singleton bind specialization |
| assignments and `i += 1` | strict syntax, `controls.k`, `int.k` |
| `l[::2]`, `l[1::2]`, `evens[i]`, `evens[len(odds):]` | `subscript.k` contexts, dereference, slice normalization/build, positional read |
| `sorted(...)` and `len(...)` | `sort.k`; `builtins.k` |
| `ListExpr`, `append`, final list `+` | `list.k`, `call.k`, `operators.k`, heap allocation in `core.k` |
| `For odd in odds` | strict syntax, list iterator rules, `controls.k`, `tuple.k` name-target binding |

These paths preserve evaluation order, scope/heap state, frame control, list
allocation, and return behavior.  The loop claim contains an arbitrary
continuation and the real loop body; it does not introduce an abrupt return or
discard that continuation.

### Candidate-local extensions

The local body/closure, slice, pair, index, suffix, and assembly symbols are
transparent definitional summaries with constructor-disjoint, descending, or
single equations.  They do not replace the property-bearing execution.

The two `valSeqConcat` simplifications are ordinary right identity and
associativity.  They agree with the fixed recursive concat equations on every
overlap and orient toward a simpler/right-associated form.  The `"$cells"`
membership simplification removes five concrete keys, each provably distinct
from `"$cells"`, then checks only the framed remainder.

`#observeResult` is a specification-only observer after real execution.  Its
reference rule reads the value at the returned heap address without changing
the heap or continuation; its complementary non-reference rule is identity.
The total `isRefV` split covers all `Val`.

The priority-30 singleton `#bindP` rule is an administrative operational
specialization.  Its complete match domain requires the newly allocated
current scope to be exactly `.Map`.  Instantiating the fixed generic bind rule
at parameter `"l"` and then the fixed empty-bind rule produces exactly the same
`"l" |-> V` map, `.K`, continuation, environment, heap, stack, return, and
exception state.  The higher-priority cell-binding rule cannot apply because
`"$cells" in_keys(.Map)` is false.

A separate definition importing only fixed semantics compiled successfully,
but bridge-free universal and ground Haskell connection claims remained stuck
at the initial `#bindP`; see
[`stage5-bind-connection-build.log`](evidence/stage5-bind-connection-build.log),
[`stage5-bind-connection-proof.log`](evidence/stage5-bind-connection-proof.log),
and [`stage5-bind-connection-ground-proof.log`](evidence/stage5-bind-connection-ground-proof.log).
This reproduces the backend narrowing ambiguity the specialization is intended
to avoid.  It is a missing machine-checked connection artifact and therefore a
validation concern.  It is not labeled unsound: the exact fixed two-step
derivation is valid over the complete match domain, concrete fixed-semantics
function calls succeed, and no false value/control/state conclusion witness
exists.

### Opaque and total symbols

The candidate adds no opaque/no-evaluator symbol.  Of the 22 fixed opaque
symbols, only `sortVS` is reachable here; the md5, keyed-sort, and 19 float
symbols are inert.  `sortVS` is explicitly the supplied semantics' external
trusted primitive.  The K proof is interpretation-parametric: both execution
and postcondition contain the same `sortVS`, so the proof establishes the
wrapper logic but does not establish that `sortVS` is an ascending,
length-preserving permutation.

`valSeqAt` is fixed, total, and intentionally underspecified for opaque or
out-of-bounds sequences.  Assuming the named `sortVS` permutation/length
contract, all loop accesses are in bounds because
`len(evens) = ceil(len(VS)/2) >= floor(len(VS)/2) = len(odds)`.  Without that
external contract, the K theorem remains a structural theorem over opaque
values, not a proof of Python exception behavior.

No candidate-local rule was found that encodes the task answer, uses an
unconstrained oracle, bypasses the body, fabricates a used construct, or
supports a concrete false conclusion on the intended integer-list domain.
Accordingly, no rule is called unsound without the required witness.

## 6. Fresh non-vacuity test

The reviewer created a distinct mutation,
[`spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k), using the exact entry
state at `VS = .ValSeq` but changing the required result from `[]` to `[0]`.
This is demonstrably false for a satisfying input and changes only the
result-constraining obligation.

The dry run compiled the mutation successfully (exit 0).  The real proof exited
1 with `WarnStuckClaimState`; its final configuration contains
`list(.ValSeq)`, and the backend reports that it cannot unify with the mutated
destination.  This is the expected unmet result, not a parser/import error,
timeout, or unrelated crash.  See
[`stage6-mutation-dry-run.log`](evidence/stage6-mutation-dry-run.log) and
[`stage6-mutation-proof.log`](evidence/stage6-mutation-proof.log).

An earlier universal extra-element mutation built but was manually stopped
after unbounded proof search; its logs are preserved as
`stage6-universal-mutation-*` and are not used as non-vacuity evidence.

The separate loop-body mutation in Stage 4 also failed for the expected value
residual, independently establishing program-body sensitivity.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the fresh Haskell definition consisting of the supplied semantics and
the statically reviewed `verification.k`, for every `VS:ValSeq` in the exact
entry configuration, partial correctness establishes that the submitted
function-body execution reaches the structural result

```text
assembledEvenSort(sortVS(evenIndices(VS)), oddIndices(VS))
```

with the loop performing the stated pairwise appends and index increments.  It
also establishes the independently checked loop claim used for proof
composition.  This is an execution theorem, not merely a differential test.

### Trust ledger

| Boundary | Influence and assessment |
|---|---|
| K v7.1.337 parser, compiler, Haskell/LLVM backends, and K builtins | Standard machine-checking trust base; affects all proof/build results. Acceptable. |
| Byte-identical supplied MPY semantics | Defines the language, configuration, evaluation, allocation, calls, loops, and results. Required by `SUPPLIED_SEMANTICS`; accepted at that selected semantics level. |
| `sortVS` | Directly affects every sorted-even value and the final postcondition. It is intentionally external to the proof and fixed by the supplied semantics, but ascending/permutation/length are a named contract rather than a K theorem here. Acceptable for legitimacy, concerning for complete intent validation. |
| Total opaque `valSeqAt(sortVS(...), i)` | Can influence each even output. It is valid on the intended path conditional on the `sortVS` length contract; otherwise the K term is merely opaque. Same concern as `sortVS`. |
| Exact manual body transcription in `sortEvenBody` | Determines which program is proved. Translator byte identity, concrete loader output, line-by-line AST review, and the rejected body mutation support the bridge. Legitimate, with the ordinary residual risk of manual duplication. |
| Singleton bind specialization | Affects initial parameter binding/control. Exact fixed-rule instantiation shows identical behavior; no value oracle is introduced. The failed bridge-free Haskell check is an auditability concern, not a false-rule witness. |
| `#observeResult` | Converts the returned heap reference to its structural list after execution. Fully defined, state-preserving, and does not influence program control. Acceptable specification instrumentation. |
| `SPEC.loop-correct` supplied with `--trusted` during entry proof | Affects loop summarization, but the identical claim independently closed with `#Top` first. Acceptable proof composition, not an outstanding assumption. |
| Termination | Excluded by partial correctness in principle. For finite input lists this implementation's `For` loop consumes one list constructor per step, and all used helper recursions descend, so termination is also informally evident. |

### Independent evidence for intent bridges

The 20,054-case Python differential in Stage 2 connects the submitted Python
algorithm to the trusted canonical over the recorded integer corpus.

The reviewer also generated 100 canonical-answer assertions, translated them
with the trusted translator, and ran the actual submitted program through the
fresh LLVM semantics.  The corpus includes explicit parity/boundary cases, all
lists of lengths 0 through 2 over `[-2,-1,0,1,2]`, and deterministic generated
lists up to length 15.  Python and K both exited 0.  See
[`generate_k_differential.py`](evidence/generate_k_differential.py),
[`k-differential-inputs.json`](evidence/k-differential-inputs.json), and
[`stage7-k-differential.log`](evidence/stage7-k-differential.log).

An attempted 1,000-case single `.mpy` concrete corpus exhausted the Java
parser's memory (exit 137); its source and log are preserved with `-1000`/`oom`
suffixes.  It is excluded from candidate judgment and was replaced by the
successful bounded 100-case run.

These tests support only the tested Python/translation/concrete-semantics
bridges.  They do not universally prove the opaque `sortVS` contract or replace
the successful K reachability proofs.

### Decision

The proof is legitimate: it reconstructs from source, both positive claims
close with `#Top`, the exact generated program body is executed, the output is
fully constrained, all candidate-local rules are sound on the intended domain,
and meaningful result/body mutations fail for the expected obligations.

`PASS` is withheld because (1) the four requested provenance records and trace
are absent, (2) the natural-language meaning of the supplied opaque `sortVS`
remains a trusted/empirically supported bridge rather than a theorem in this
proof, (3) the formal `ValSeq` domain is broader than the well-supported
integer-list intent, and (4) the administrative bind bridge has an exact static
derivation but no closing bridge-free Haskell connection artifact.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
