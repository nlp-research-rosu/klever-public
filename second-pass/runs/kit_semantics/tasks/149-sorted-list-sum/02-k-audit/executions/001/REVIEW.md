# Independent adversarial proof audit: 149-sorted-list-sum

## Executive decision

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted program over arbitrary finite K lists whose elements are strings.
Fresh reconstruction closes both the loop-summary claim and the complete entry
claim. The entry claim loads and calls a constructor term mechanically identical
to the freshly parsed submitted `solution.mpy`, and its result is constrained to
the filtered sequence followed by the supplied semantics' two sorting
operations.

The qualification is important: in the supplied proof semantics, `sortVS` and
`sortKeyVS` are opaque total symbols. The K theorem preserves those exact
result-bearing operations but does not itself prove their human-level contracts
of alphabetical ordering and stable length-key ordering. Those contracts are a
fixed-semantics trust boundary, supported here by the concrete rules and finite
differential execution, not a universal K theorem. This is a material but
non-fatal intent bridge, so the result is `CONCERNS / LEGIT`, not `PASS`. It is
not a domain restriction, substituted program, or unsound candidate rule.

Reviewer evidence and command notes are indexed in
[`evidence/README.md`](evidence/README.md).

## 1. Input and provenance integrity

I followed the `using-kit` routing and the `validating-proof` audit procedure.
Because the rendered mode is `SUPPLIED_SEMANTICS`, I did not use the
generated-semantics workflow.

The launcher record declares:

- `record_layout = pipeline-v3`;
- problem `149-sorted-list-sum`;
- generation condition `kit-semantics`; and
- semantics mode `SUPPLIED_SEMANTICS`.

I read `/audit-input.json`, its `record_layout`, `container_paths`, integrity
fields, and hashes before inspecting the candidate. I then read
`/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, and every required pipeline-v3 generation record:
`invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
These records were treated only as untrusted claims.

The campaign block is byte-for-byte equal to the campaign lock and its recorded
SHA-256 matches. Independent hashing matched every recorded regular-file digest
for the trusted prompt, canonical implementation, translator, launcher
manifests, all required generation records, and the sole 529-line trace file.
All 529 trace lines parse as JSON. The launcher-framed trace, supplied-semantics,
and candidate workspace manifest digests also match their corresponding
recorded manifest hashes. Full values and comparison results are in
[`stage1-provenance.log`](evidence/stage1-provenance.log), which ends with
`errors=0` and exit status 0.

The trusted `/reference/reference-semantics` mount exists as required.
Candidate and trusted trees each contain the same 25 entries. Neither tree has
a symlink or mistyped node, and recursive path, type, and byte comparison found
no missing, additional, or changed entry. The candidate `prompt.py` and
`py2mpy.py` are also byte-identical to their trusted mounts. Thus the fixed
semantics is intact; this identity does not confer any authority on
`verification.k` or `spec.k`, which were reviewed separately.

No required launcher-owned mount or record was missing or unreadable. There is
no infrastructure breach. The local K tools are version 7.1.293, recorded with
successful commands in
[`stage1-tool-versions.log`](evidence/stage1-tool-versions.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a finite list of strings, retain precisely the strings whose lengths are
even, then return them ordered first by increasing length and, among equal
lengths, alphabetically. Duplicates are retained. The examples demonstrate that
different input lengths are intended despite a stray prompt sentence saying
that all words may have the same length; the candidate theorem does not rely on
that sentence and accepts arbitrary string lengths.

The trusted canonical implementation first alphabetically sorts the caller's
list in place, filters even-length strings, and applies Python's stable
`sorted(..., key=len)`. The submitted implementation builds a fresh filtered
list and returns `sorted(sorted(result), key=len)`. The returned values are
equivalent on the contract domain. The canonical mutates its input whereas the
submitted function does not; the prompt specifies only the returned list, so
this is an observable implementation difference but not a contract violation.

Running the trusted translator directly on `/candidate/solution.py` produced
bytes identical to `/candidate/solution.mpy`; see
[`stage2-regeneration.log`](evidence/stage2-regeneration.log).

The independent
[`differential_test.py`](evidence/differential_test.py) imports both Python
entry points. It exercises both documented examples, 13 explicit empty,
boundary, duplicate, branch, ordering, and Unicode cases, every list of lengths
0 through 3 over `["", "a", "aa", "bb", "ccc"]`, and 200 deterministic
generated cases (seed 149, maximum list length 12). All 371 returned results
matched. It separately reports 253 canonical input mutations and zero submitted
input mutations. Exact scope and exit status 0 are in
[`stage2-differential.log`](evidence/stage2-differential.log).

## 3. Clean proof reconstruction

I copied source artifacts only to
`/tmp/audit-work/149-sorted-list-sum`. Candidate `*-kompiled` directories,
Python caches, logs, and other candidate-built outputs were neither copied nor
used. From source I created:

- an LLVM concrete definition, `reviewer-runtime-kompiled`;
- a Haskell proof definition, `reviewer-verification-kompiled`; and
- a separate Haskell fixed-semantics-only definition for a Stage 5 check.

The exact build commands, warnings, and status 0 are in
[`stage3-kompile-llvm.log`](evidence/stage3-kompile-llvm.log) and
[`stage3-kompile-haskell.log`](evidence/stage3-kompile-haskell.log). The
compiler's unused-variable and unrelated non-exhaustiveness warnings do not
occur on the submitted program's string/list path.

A reviewer-authored smoke module was translated with the trusted translator and
executed with the fresh LLVM definition on empty input, prompt examples, mixed
even/odd inputs, and an all-odd input. Execution reached `.K`, `NoExc`, and
exit-code 0. Sources and output are in
[`reviewer_smoke.py`](evidence/reviewer_smoke.py),
[`stage3-translate-smoke.log`](evidence/stage3-translate-smoke.log), and
[`stage3-krun-smoke.log`](evidence/stage3-krun-smoke.log).

Both positive target claims were then reconstructed:

- `kprove ... --claims SPEC.filter-loop` exited 0 and printed `#Top`
  ([`stage3-kprove-filter-loop.log`](evidence/stage3-kprove-filter-loop.log)).
- `kprove spec.k --definition reviewer-verification-kompiled --spec-module
  SPEC` proved the complete two-claim specification, exited 0, and printed
  `#Top` ([`stage3-kprove-all.log`](evidence/stage3-kprove-all.log)).

The entry proof is intended to use the labelled loop claim as a circularity.
For diagnosis I also selected only `SPEC.sorted-list-sum`, thereby removing the
loop claim from the circularity set. The backend kept actively unrolling until
manually interrupted; this is not the submitted proof obligation and is not
used as positive or negative evidence. Its exact command and the transcript
qualification are preserved in
[`stage3-kprove-sorted-list-sum.log`](evidence/stage3-kprove-sorted-list-sum.log)
and the evidence index.

## 4. Adequacy and real-program pinning

### Claim meanings

`filter-loop` starts at the real `#loop` control term for the submitted `for`
body. Its precondition permits any finite `INPUT:ValSeq` satisfying
`stringsOnly(INPUT)`, any accumulated sequence, and a heap location containing
that accumulated list. Its postcondition consumes the loop and changes exactly
that heap entry to `scanEven(ACC, INPUT)`, while framing the actual closure,
argument, local variable, and continuation context. In plain language: running
the remaining loop appends exactly the remaining even-length strings in order.

`sorted-list-sum` starts with
`#loadAll(sortedListSumModule) ~> Call(Name("sorted_list_sum"),
list(INPUT))`, again requiring only that every element is a string. It reaches
normal completion and returns `ref(2)`. The heap is constrained to:

1. location 0: `list(scanEven(.ValSeq, INPUT))`;
2. location 1: `list(sortVS(scanEven(.ValSeq, INPUT)))`; and
3. location 2:
   `list(sortKeyVS(sortVS(scanEven(.ValSeq, INPUT)), builtinV("len")))`.

It also constrains allocation from 0 to 3, the installed closure, empty stack,
`noRet`, `NoExc`, and exit-code 0. The result is neither free nor tautological.

### Mechanical pinning

Using the freshly built definition, I parsed `solution.mpy` with
`kast --expand-macros --output json`, separately parsed the
`sortedListSumModule` constructor macro with the same syntax and macro
expansion, and compared the JSON. Both 8,689-byte terms are byte-identical and
all three commands exited 0:
[`stage4-constructor-pinning.log`](evidence/stage4-constructor-pinning.log).
Combined with the trusted-translator byte identity from Stage 2, this pins the
claim to the submitted function binding and complete body rather than a
substitute.

The entry representation passes `list(INPUT)` directly rather than allocating a
caller-owned heap reference. For this function that is a sound read-only
abstraction: the submitted body only iterates over `lst`, never mutates or
aliases it. It is nevertheless an informal Python-to-K input-representation
bridge and is included in the concern accounting below.

Both preconditions are satisfiable. A loop witness uses `ACC=["cc"]`,
`INPUT=["aa","b"]`, and heap location 0, yielding
`scanEven=["cc","aa"]`. An entry witness uses
`["bb","a","aa","cccc"]`, yielding the constrained result
`["aa","bb","cccc"]` in both Python implementations. These substitutions are
recorded by the independent
[`ground_claim_witness.py`](evidence/ground_claim_witness.py) in
[`stage4-ground-witness.log`](evidence/stage4-ground-witness.log).

Finally, a body-sensitivity mutation changed the comparison in the constructor
term actually executed by the entry claim from `== 0` to `!= 0`. The mutated
spec built successfully but proof exited 1 with a reachable final heap
containing the wrong (empty for the witness path) filtered result:
[`stage4-body-mutation-dry-run.log`](evidence/stage4-body-mutation-dry-run.log)
and
[`stage4-body-mutation-proof.log`](evidence/stage4-body-mutation-proof.log).
This is a real theorem-body dependency, not merely an external-source edit.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

I inventoried every statement in the fixed semantics, `verification.k`, and
`spec.k`, including full compact text and source ranges. The reviewer script and
162-KB output are
[`k_rule_inventory.py`](evidence/k_rule_inventory.py) and
[`stage5-k-rule-inventory.log`](evidence/stage5-k-rule-inventory.log).
The inventory covers 26 files and 1,114 statements: 231 syntax declarations,
704 rules, five contexts, one configuration, 28 modules, and two claims, as
well as every import/require/end marker. Attribute counts include 157
`function`, 117 `total`, 35 `concrete`, 26 `owise`, 45 priority, three
`simplification`, seven macro/macro-rec, and 22 `no-evaluators` declarations.
Per-file counts and every individual priority, function, total declaration,
opaque symbol, syntax declaration, and rule appear in that log.

The candidate-owned proof extension is small enough to state completely:

- syntax: total functions `stringsOnly(ValSeq)` and
  `scanEven(ValSeq,ValSeq)`, plus the `sortedListSumBody` and
  `sortedListSumModule` macros;
- `stringsOnly`: empty is true; cons is `isStrV(head) andBool
  stringsOnly(tail)`;
- `scanEven`: empty returns the accumulator; a string of even length is
  appended; a string of nonzero odd parity is skipped; a non-string is skipped;
- one simplification states only that `seqLen(V)` is defined when `isStrV(V)`;
- two constructor macro expansion rules reproduce the submitted body and
  module.

There are nine candidate rules total, three tagged `simplification`, and no
candidate priority rule, operational `<k>` shortcut, opaque symbol, or oracle.

### Used-construct mapping and operational review

The submitted program's constructs map to the fixed syntax and rules as
follows:

- `Module`, `FuncDef`, parameters, `Assign`, `ListExpr`, `Str`, `For`, `If`,
  `Compare`, `BinOp`, `Call`, `Attribute`, `Return`, `Name`, `Int`, and keyword
  arguments are declared in `syntax.k` with their strictness/evaluation
  contexts;
- configuration, module loading, sequencing, name lookup, allocation,
  left-to-right argument evaluation, literals, the builtin scope, `ValSeq`, and
  length helpers are in `core.k`;
- closure creation, parameter binding, frames, calls, returns, stack unwinding,
  and reference dereference are in `functions.k` and `call.k`;
- loop iteration, target binding, and branching are in `controls.k`,
  `iter.k`, and `bool.k`;
- list construction, iteration, and `append`'s heap update are in `list.k` and
  `methods.k`;
- `len`, integer modulo, and equality use `builtins.k`, `int.k`, and
  `operators.k`;
- the two `sorted` calls, including the `key=len` route and fresh-list
  allocations, use `sort.k` (and concrete keyed execution uses `concrete.k`).

Following this path establishes left-to-right evaluation, exactly one mutable
result-list allocation before the loop, append updates to that heap object,
then two non-mutating sorted-list allocations. No exceptional rule is reachable
under `stringsOnly(INPUT)`.

### Candidate-rule judgments

The `stringsOnly` cases are disjoint and structurally descending.
`scanEven`'s empty and cons cases are structurally complete. On strings, its
zero and nonzero `pyMod(length,2)` guards are disjoint and exhaustive; the
non-string totalization is irrelevant under the entry precondition and does
not assert a program result. Appending the current element in the even branch
and preserving the accumulator in the odd branch exactly matches the loop.

The `#Ceil(seqLen(V))` simplification asserts definedness only. In the fixed
semantics `isStrV` recognizes `str(CS)`, `seqLen(str(CS))` reduces to
`isLen(CS)`, and `isLen` is structurally total. A fixed-semantics-only claim
checking the constructor connection closes with `#Top`; see
[`definedness-spec.k`](evidence/definedness-spec.k) and
[`stage5-kprove-definedness-connection.log`](evidence/stage5-kprove-definedness-connection.log).
Two abandoned formulations and why they are not evidence are explicitly
recorded in the evidence index. The macro equations are compile-time exact
constructor expansions, independently confirmed in Stage 4.

The loop claim is a guarded circularity: real operational steps consume a
sequence element before recurrence. It preserves the arbitrary continuation and
frames the relevant environment and heap. Under the string precondition the
body has no `break`, return, exception, or other abrupt effect. I found no
candidate rule that can conclude a false result, encode the benchmark answer,
bypass program execution, or fabricate a used operation. Accordingly there is
no unsound-rule allegation requiring a false-conclusion witness.

### Fixed-semantics trust boundary

The inventory finds 22 opaque `no-evaluators` symbols:
`md5hexCodes`; 19 float-related symbols
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`,
`mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, and `sqrtF`; and `sortVS`, `sortKeyVS`. Only the two sort
symbols are reachable from this theorem. The md5 and float symbols are
constructor- and type-disjoint from the submitted path.

`sort.k` has concrete insertion-sort equations for integer and string
`sortVS`; its concrete keyed implementation calls the key and stably inserts
the associated values. However, the proof imports `MPY`, not the concrete
execution module, and `sortVS`/`sortKeyVS` remain opaque total symbols to the
Haskell prover. This is sound as an abstraction—the theorem cannot invent or
rewrite their values—but it means the universal connection from those names to
Python alphabetical ordering and stable `key=len` sorting is assumed rather
than proved in this reachability claim.

A fresh LLVM differential module mechanically generated from the actual
candidate exercised all 156 lists of lengths 0 through 3 over
`["", "a", "aa", "bb", "cccc"]`. Its Python results all matched, translation
and `krun` exited 0, and execution ended with `.K`, `NoExc`, and exit-code 0:
[`k_differential_test.py`](evidence/k_differential_test.py) and
[`stage5-k-differential.log`](evidence/stage5-k-differential.log). This supports
the concrete bridge for those ASCII cases only; it is not substituted for a
universal K proof.

## 6. Fresh non-vacuity test

I ignored the candidate's vacuity artifact and wrote
[`reviewer-false-spec.k`](evidence/reviewer-false-spec.k) from scratch. Its
ground input is `["aa"]`, which satisfies the real entry precondition. The
mutation keeps real program execution but requires the returned list to contain
two copies of `"aa"`, a demonstrably false result-constraining postcondition.

The mutated specification parsed and dry-ran successfully with status 0:
[`stage6-false-mutation-dry-run.log`](evidence/stage6-false-mutation-dry-run.log).
Proof then reached the normal final program configuration and failed with status
1 because the duplicated list could not equal
`sortKeyVS(vCons("aa"), builtinV("len"))`:
[`stage6-false-mutation-proof.log`](evidence/stage6-false-mutation-proof.log).
This is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash. The positive proof is non-vacuous.

## 7. Proven versus assumed accounting

### What the K proof establishes

For every finite K `ValSeq` consisting only of strings, if the submitted
translated module starts in the claim's initial configuration and reaches a
result, the supplied MPY semantics executes its actual function body, appends
exactly the even-length elements in original order, performs both real
`sorted` calls, allocates their result lists, and returns the reference whose
contents are exactly:

`sortKeyVS(sortVS(scanEven(.ValSeq, INPUT)), builtinV("len"))`.

It also establishes normal control completion and no exception for that
execution. The domain is symbolic and unbounded; it is not a finite-size,
example-only, or bounded-unrolling theorem.

### Assumptions and informal bridges

1. **The supplied MPY semantics.** This trusted, byte-verified tree defines
   Python execution for the modeled language. Treating that supplied language
   definition as the base semantics is required by the benchmark mode and is
   acceptable.
2. **`sortVS`.** The human interpretation “stable ascending alphabetical sort
   on strings” is external to the symbolic proof because this result-bearing
   symbol is opaque there. Concrete rules and testing support it, but do not
   universally prove the bridge. This is concerning but not an unsound proof
   extension.
3. **`sortKeyVS(..., builtinV("len"))`.** Stable ascending sorting by the actual
   `len` key is likewise an opaque fixed-semantics primitive contract in the
   symbolic theorem. This is the principal reason for `CONCERNS`.
4. **Python/K input representation.** A bare K `list(INPUT)` is used as the
   read-only argument rather than a caller heap reference. Because the submitted
   function never mutates or aliases `lst`, this bridge is adequate here but
   informal.
5. **Strings.** The symbolic proof ranges over arbitrary K `IntSeq` strings and
   uses their modeled length and order. Concrete translator tests were limited
   to its accepted literal encoding (primarily ASCII); the finite tests do not
   establish all Python Unicode behavior.
6. **Partial correctness.** Termination, resource bounds, and complexity are
   not claimed. Differential tests, body mutation, and traces are corroborating
   evidence only; none substitutes for the K reachability proof.

Candidate `PROOF.md`, candidate compiled definitions, generation reports, and
generation traces were not trusted as proof evidence. On the independently
rebuilt sources, the proof is result-constraining, non-vacuous, and pinned to
the real program. Its material limitation is the explicitly accounted
fixed-semantics sorting contract, which does not enable a false K conclusion or
narrow the HumanEval domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
