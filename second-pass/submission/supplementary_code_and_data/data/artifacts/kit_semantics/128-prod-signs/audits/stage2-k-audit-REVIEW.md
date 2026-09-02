# Independent adversarial audit: 128-prod-signs

The candidate contains a legitimate partial-correctness proof of the submitted
program. I reconstructed all definitions from source under the supplied
semantics, reran each positive claim, checked the proof-local theory
independently, and obtained a meaningful rejection of a fresh false
postcondition. The candidate's prior `VALIDATED` report and generation traces
were not used as proof authority.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout = pipeline-v3`,
`condition = kit-semantics`, and
`semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so the trusted mounts do not
contradict the rendered mode.

The independent checker
[verify_integrity.py](/audit-output/evidence/verify_integrity.py) and its
[log](/audit-output/evidence/00-integrity.log) establish:

- `/audit-campaign-lock.json` is byte-hashed to the SHA-256 recorded in
  `/audit-input.json`, and its parsed object is exactly the
  `audit_campaign` block.
- All pipeline-v3 records required by the prompt are real regular files:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured
  trace. The trusted canonical, prompt, and translator are also real regular
  files.
- Every launcher-recorded file SHA-256 checked by the script matches. The
  trace file in `generation-result.json` hashes to
  `8b8777e02b6bea0569aa937e2fd4ab981926762ddd60b5e18634d5bfb006d355`.
- An independent implementation of the pipeline tree digest gives
  `34c5ba24b741133bc8c5d44494e4f5c7c7b0b1f5606cd269009bc112e0ad4fcb`
  for `/candidate`, exactly the generation result's workspace digest;
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`
  for the semantics tree, exactly the task input digest; and
  `eb6c9fbd79a07d308d9ee39ce7ac32fc8102b80bb87b810b392c554856bde051`
  for the trace tree, exactly `usage.json`'s source-trace digest.
- The candidate prompt and translator are byte-identical to the trusted
  versions.
- A recursive path/type/content comparison finds exactly 25 entries in each
  semantics tree and no difference. There are no symlinks or unsupported
  entries in the candidate, generation evidence, or semantics mounts.

I streamed and parsed every structured trace line (1,220 valid JSON objects),
read every required JSON/text generation record, and streamed the complete
43,083-line generation output. Counts and the untrusted final generation
claim are preserved in
[01-generation-records.log](/audit-output/evidence/01-generation-records.log).
Those records say that generation succeeded and all claims closed, but this
audit relies only on the fresh results below.

There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for a finite list of integers, return `None` when the
list is empty; otherwise return the sum of the absolute values multiplied by
the product of the element signs, where each sign is `-1`, `0`, or `1`.

The trusted canonical implementation detects zero, counts negative elements,
and multiplies that sign by the magnitude sum. The candidate implementation
uses a single traversal:

- `seen` distinguishes an empty input.
- `total` accumulates `abs(value)`.
- `sign` starts at 1, is negated for a negative value, preserved for a
  positive value, and set to 0 for zero.

This is equivalent on the intended domain. Once `sign` is zero it remains
zero, as required.

Using the trusted translator in source-only scratch regenerated
`solution.mpy` byte-for-byte. Both files have SHA-256
`fee368e5a5a7c3b10944883aa702e60bbafa584ef95949038f3ad8fa662165c7`;
see [10-regeneration.log](/audit-output/evidence/10-regeneration.log).

The independent differential test
[differential_test.py](/audit-output/evidence/differential_test.py) imports
`/reference/canonical.py` and the scratch copy of the generated implementation.
It covers the documented examples; empty, singleton negative, zero, and
positive inputs; zero at different positions; even and odd negative parity;
very large integers; every list of lengths 0 through 6 over
`{-3,-1,0,1,2}`; and 10,000 deterministic random lists of lengths 0 through
30. Its 29,544 cases had zero mismatches and exited 0:
[11-differential.log](/audit-output/evidence/11-differential.log).

No implementation/specification divergence was found.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/128-prod-signs` and used a
fresh copy of the trusted semantics. No candidate `*-kompiled` directory,
cache, binary, or archived backend report was copied or reused. The live
toolchain was K 7.1.293 and Python 3.10.12
([02-toolchain.log](/audit-output/evidence/02-toolchain.log)).

The concrete semantics was rebuilt from the trusted source with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

It exited 0
([20-build-runtime.log](/audit-output/evidence/20-build-runtime.log)). A freshly
translated smoke program executed the three documented examples and two
additional negative-parity cases, finishing with `.K`, `NoExc`, exit code 0,
and process status 0
([21-runtime-smoke.log](/audit-output/evidence/21-runtime-smoke.log)).

All proof definitions were then freshly built with the Haskell backend. Every
positive claim was independently executed:

| Definition or claim | Fresh result |
|---|---|
| `CONNECTION` build | exit 0 ([log](/audit-output/evidence/30-build-connection.log)) |
| Both `CONNECTION-SPEC` claims | `#Top`, exit 0 ([log](/audit-output/evidence/31-prove-connection.log)) |
| `LOOP-CONNECTION` build | exit 0 ([log](/audit-output/evidence/32-build-loop-connection.log)) |
| `LOOP-CONNECTION-SPEC.prod-signs-loop` | `#Top`, exit 0 ([log](/audit-output/evidence/33-prove-loop-connection.log)) |
| Both ground iterator witnesses | `#Top`, exit 0 ([log](/audit-output/evidence/34-prove-iterator-witnesses.log)) |
| `VERIFICATION` build | exit 0 ([log](/audit-output/evidence/35-build-verification.log)) |
| Both claims in `SPEC` together | `#Top`, exit 0 ([log](/audit-output/evidence/36-prove-targets.log)) |
| `SPEC.loop-invariant` alone | `#Top`, exit 0 ([log](/audit-output/evidence/37-prove-loop-invariant-only.log)) |
| `SPEC.prod-signs` alone | `#Top`, exit 0 ([log](/audit-output/evidence/38-prove-entry-only.log)) |

The dependency inventory
[70-proof-dependencies.log](/audit-output/evidence/70-proof-dependencies.log)
confirms the intended acyclic structure:

1. `CONNECTION-SPEC` imports `connection.k`, not
   `verification-base.k`.
2. `LOOP-CONNECTION-SPEC` imports `verification-base.k`, not the loop rule in
   `verification.k`.
3. Only the final target definition imports the exact loop-summary rule.

Thus the candidate's positive reconstruction gate passes.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.prod-signs` has no numerical bound. For every finite
`INPUT:IntSeq`, it starts from the supplied semantics' normal initial module
configuration, loads a function named `prod_signs`, and calls that function
with the read-only integer list `list(intVals(INPUT))`. It requires the normal
final module scope, empty stack, `noRet`, `NoExc`, and exit code 0. Its result is:

```text
prodSignsResult([]) = None
prodSignsResult(value :: rest) = foldResult(value :: rest, 0, 1)
```

`foldResult` adds each absolute value and updates the sign exactly as the
program does, then returns `total * sign`.

`SPEC.loop-invariant` says that, after at least one element has set `seen` to
1, executing the exact remaining loop body, post-loop `if`, final return, and
call-frame cleanup reaches `foldResult(REST,TOTAL,SIGN)`, preserving the
arbitrary heap and heap-location cells.

### Mechanical program identity

The entry claim begins with `#loadAll(Module(FuncDef(...)))` and then
`Call(Name("prod_signs"), ...)`; it does not call a summary in place of loading
and entering the submitted function. The claim includes the complete function
constructor tree in both the loaded program and the expected module binding.

[extract_claim_program.py](/audit-output/evidence/extract_claim_program.py)
mechanically extracts the balanced `Module(...)` argument from the claim.
Removing only explicit `.Stmts` associative-unit tokens—tokens accepted in a
K claim but not by the surface-program scanner—the extracted claim program
and the trusted regeneration parse to byte-identical KORE:

```text
db6f3a4683bd1598b19ed89051cf54dc52c6e76dde158f1f2bdb7ec15bcdd60b
```

See
[40-extract-claim-program.log](/audit-output/evidence/40-extract-claim-program.log)
and
[42-constructor-compare-normalized.log](/audit-output/evidence/42-constructor-compare-normalized.log).
This is a constructor-level comparison, not a textual resemblance judgment.

The actual executed body is also proof-sensitive. The auditor-generated
[entry body mutation](/audit-output/evidence/auditor-body-mutation-spec.k)
grounds the entry at `[1]` and changes both occurrences of the loaded/expected
closure body from `seen = 1` to `seen = 0`. Its dry run succeeds
([log](/audit-output/evidence/68-entry-body-mutation-dry-run.log)); proof then
reaches `noneV` rather than 1, emits `WarnStuckClaimState`, and exits 1
([log](/audit-output/evidence/69-entry-body-mutation-proof.log)). This changes
the program term actually executed by `#loadAll`; it is not a mutation of an
external source file ignored by the claim.

### Satisfiable preconditions and ground substitutions

The main entry precondition is satisfiable, for example with
`INPUT=.IntSeq` and exactly the concrete initial cells written in
`SPEC.prod-signs`; the fresh proof reaches `noneV`. It is also satisfiable with
`INPUT=iCons(1,.IntSeq)`, reaching 1. The helper precondition is satisfiable,
for example with `REST=.IntSeq`, `TOTAL=2`, `SIGN=-1`, `seen=1`, a normal
single call frame, empty heap, and the displayed builtins/module/local scopes;
it reaches `-2`.

Five ground formal results—empty, documented nonzero, zero-containing,
negative-parity, and 41-digit-integer inputs—were reduced under the proof
definition and gave `#Top`
([45-prove-ground-results-config.log](/audit-output/evidence/45-prove-ground-results-config.log)).
The same expected values equal both Python implementations
([44-ground-python-compare.log](/audit-output/evidence/44-ground-python-compare.log)).

The formal domain is all finite lists of mathematical integers, with no bound
on list length or integer magnitude. This materially matches the prompt's
array-of-integers domain; it is not a finite-size or example-only theorem.

## 5. Rule-by-rule static soundness review

The exhaustive inventory
[rule-inventory.tsv](/audit-output/evidence/rule-inventory.tsv), generated by
[inventory_k.py](/audit-output/evidence/inventory_k.py), contains 944 items:
231 syntax declarations, 707 rules, five contexts, and one configuration.
Attributes recorded per item include every `function`, `total`, `functional`,
`simplification`, `priority`, `owise`, `concrete`, macro, strictness, symbol,
and `no-evaluators` occurrence.

[rule-review.tsv](/audit-output/evidence/rule-review.tsv) attaches a disposition
to every one of the 944 entries. The disposition counts are:

```text
440 fixed-semantics relevant entries reviewed
412 fixed-semantics entries inert for this program
 51 fixed concrete-only entries
 25 fixed opaque/no-evaluators boundaries, all unused
  8 local mathematical summary entries
  4 local input-representation entries
  2 local connection rules
  2 local operational bridges
```

The inventory and classification commands, counts, and hashes are preserved in
[51-inventory-final.log](/audit-output/evidence/51-inventory-final.log) and
[52-rule-review.log](/audit-output/evidence/52-rule-review.log).

### Proof-local inventory

| Extension | Classification, complete domain, and result |
|---|---|
| `intVals(IntSeq) [functional]` | A proof-only representation of a finite sequence of integer values. The deprecated attribute spelling is harmless. Its observable iteration is fixed by disjoint empty/cons cases; there is no fresh result oracle. |
| Two `#typedNext` rules | Structural empty/cons iterator cases. Empty produces `#iterDone`; cons yields exactly the head integer and represented tail. |
| Four `foldResult` simplifications | Mathematical summary. The negative, zero, and positive guards are pairwise disjoint and exhaustive over K integers. Every recursive RHS strictly descends to `REST`; the base returns `TOTAL *Int SIGN`. |
| Two `prodSignsResult` equations | Empty and cons are disjoint and exhaustive. The nonempty case starts the fold at exactly the program's initial accumulators `(0,1)`. |
| Two rules in `connection.k` | Definitional materialization of the proof-only representation for fixed list iteration. They match only an iterator redex immediately followed by `#loopStep`, preserve arbitrary `CONT`, and are exhaustive over `IntSeq`. |
| Iterator bridge in `verification-base.k`, priority 40 | Operational bridge from `#iterNext(list(intVals(IS)))` to `#typedNext(IS)`, retaining the exact loop step and arbitrary continuation. No other cell is mentioned, so K frames every other cell unchanged. |
| Exact loop rule in `verification.k`, priority 30 | Operational bridge for the exact translated body, exact combined post-loop continuation, exact normal builtins/module/local scopes, `env=1`, `scopeLoc=2`, a single `frame(.K,0,1)`, `noRet`, `NoExc`, and exit 0. Heap and heap location are arbitrary and unchanged. Its RHS includes the correct frame/scope cleanup and exact `foldResult`. |

The iterator bridge has a bridge-free universal connection proof over both
`IntSeq` constructors and arbitrary `TARGET`, `BODY`, and `CONT`
([31-prove-connection.log](/audit-output/evidence/31-prove-connection.log)).
Ground values 4 and -2 close, while the opposite interpretation “4 yields 5”
gets stuck at the real value 4 and exits 1
([65-iterator-opposite-value.log](/audit-output/evidence/65-iterator-opposite-value.log)).
An independent transparent function with ordinary empty/cons equations has
the same universal fixed-list iterator behavior
([audit-representation.k](/audit-output/evidence/audit-representation.k),
[59b proof log](/audit-output/evidence/59b-prove-transparent-representation.log)).
The name-to-representation link is a conventional symbolic-input encoding;
order and values are not left unconstrained.

The loop bridge's justification theorem has exactly the same body,
continuation, bindings, stack, control, and cell footprint, and is proved in a
definition that omits the proposed loop rule
([33-prove-loop-connection.log](/audit-output/evidence/33-prove-loop-connection.log)).
It progresses through iterator selection and a complete body execution before
using the circularity on the remaining sequence. A loop-body mutation is
rejected with a concrete `noneV` residual
([66-loop-body-sensitivity.log](/audit-output/evidence/66-loop-body-sensitivity.log)).
The independently generated whole-entry body mutation in Stage 4 provides an
additional source-to-theorem sensitivity check.

There are no overlapping contradictory local equations, unguarded
totalizations, non-descending recursions, proof-local opaque symbols, or rules
that name the benchmark answer. The only two local priority rules preempt
fixed execution solely on the match domains established by their respective
connection proofs.

### Used fixed-semantics path

Every material constructor in `solution.mpy` is covered:

| Program construct | Fixed semantics used |
|---|---|
| `Module`, statement sequence | `core.k`'s `#loadAll` and `Stmts` rules |
| `FuncDef`, `Call`, parameter binding | `functions.k` and `call.k`; module closure binding, callee lookup, left-to-right arguments, fresh local scope, exact call frame |
| `Name`, `Assign` | `core.k` scope-chain lookup and `controls.k` current-scope update |
| `Int`, `NoneVal` | `core.k` literal rules |
| `For` | `controls.k` evaluates the iterable once, then uses `#loop`, `#iterNext`, `#loopStep`, and `#bindTgt`; `tuple.k` supplies the name-target binding |
| `abs` | `builtinsScope` pins the binding to `builtinV("abs")`; `call.k` dispatches it; `builtins.k` returns `absInt(I)` |
| `+`, `-`, `*`, `<`, `>`, `==` | strict/seqstrict evaluation plus `operators.k` dispatch and the corresponding mathematical K-integer rules in `int.k` |
| `If` | strict guard evaluation and the disjoint `truthy` branch rules in `controls.k` |
| `Return` | strict result evaluation followed by `functions.k`'s `retV`, frame pop, environment restoration, and local-scope removal |

The input list is read-only, so the supplied semantics' explicitly supported
unboxed `list(ValSeq)` claim representation preserves all material behavior;
the program never mutates or returns the input object. The exact `abs` binding
prevents a textual-name shortcut.

The fixed semantics contains 25 opaque `no-evaluators` declarations for
floats, sorting, and MD5-related operations. None is reachable from this
integer/list program or influences any branch, state cell, summary, or
postcondition. LLVM emitted five non-exhaustive-total warnings for unrelated
value constructors (`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and
`valSeqAt` categories); none occurs on the symbolic or concrete execution path
audited here. No supplied rule contains a `prod_signs`, `foldResult`, or other
task-specific conclusion.

I found no unsound inventoried rule. Consequently there is no claimed
unsoundness requiring a false-conclusion witness; the rejected opposite-value,
body, and postcondition cases above instead confirm the relevant theory is
discriminating.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`.
[make_false_mutation.py](/audit-output/evidence/make_false_mutation.py)
created the preserved fresh mutation
[auditor-false-spec.k](/audit-output/evidence/auditor-false-spec.k). It changes
the main entry postcondition from `prodSignsResult(INPUT)` to integer zero.
This is false for the satisfiable empty input (`noneV`, not 0) and for the
documented `[1,2,2,-4]` input (-9, not 0).

The exact mutation dry run:

```text
kprove auditor-false-spec.k \
  --definition verification-audit-kompiled \
  --spec-module AUDITOR-FALSE-SPEC --dry-run
```

parsed and compiled the claims, printed the backend command, and exited 0
([63-false-mutation-dry-run.log](/audit-output/evidence/63-false-mutation-dry-run.log)).
The same command without `--dry-run` exited 1 with
`WarnStuckClaimState`. Its residual is the normal final configuration with
`noneV` in `<k>` and path condition `INPUT #Equals .IntSeq`, exactly the
expected unmet result obligation
([64-false-mutation-proof.log](/audit-output/evidence/64-false-mutation-proof.log)).
This is neither a parser failure, missing import, timeout, nor unreachable
mutation.

The fresh non-vacuity gate passes.

## 7. Proven versus assumed accounting

### Formally established

Conditional on the supplied MPY definition and the audited proof-local rules,
the reconstructed reachability proof establishes:

- For every finite K `IntSeq`, the exact constructor tree regenerated from
  `solution.py` loads, binds, and executes normally on the represented
  read-only integer list.
- Empty input returns `noneV`.
- Nonempty input returns the recurrence that sums all absolute values and
  multiplies by the accumulated product of signs.
- The proof reaches the required final module scope with empty call stack,
  `noRet`, `NoExc`, and exit code 0.
- The exact remaining-loop transition preserves arbitrary heap and heap
  location while restoring the caller environment, removing the local scope,
  and popping the exact call frame.

The ordinary mathematical induction from `foldResult` to “sum of magnitudes
times product of signs” is transparent: the three sign cases are precisely the
integer trichotomy, and structural descent covers every finite sequence.

### Trust and assumptions

| Boundary | Influence | Audit judgment and evidence |
|---|---|---|
| Supplied MPY semantics | Defines all execution, binding, calls, arithmetic, lists, and control | Required trusted boundary for `SUPPLIED_SEMANTICS`; candidate tree is byte-identical to the trusted tree. Used rules were statically audited and concrete examples freshly executed. Acceptable. |
| Trusted `py2mpy.py` | Connects Python source to MPY constructors | Required trusted mount; candidate copy matches. Regeneration is byte-identical and the claim's constructor tree is KORE-identical after removing only the `Stmts` unit. Acceptable. |
| `intVals` input representation convention | Connects finite mathematical integer sequences to read-only MPY list values | Structurally exhaustive iteration connection, arbitrary continuation preservation, ground opposite-value rejection, and independent transparent-model proof. It does not summarize program-defined computation. Acceptable. |
| K integer/Boolean/map/list hooks and `absInt` | Supplies ordinary mathematical primitives used by the fixed semantics and summary | Low-level K trust boundary; operations have their standard mathematical meaning and no opaque result oracle is involved. Acceptable. |
| K compiler, parser, Haskell/LLVM backends, and host execution | Underlies `kompile`, `krun`, and `kprove` results | Standard toolchain trust boundary. Positive and deliberately false claims have the expected opposite outcomes. Acceptable. |
| Informal reading of the prompt | Identifies “array of integers” with finite integer lists and relates the recurrence to the English formula | Matches all examples, the canonical implementation, unrestricted formal domain, and 29,544 differential cases. The induction is elementary and not used to make K close. Acceptable. |

Differential tests and concrete smoke runs support only the source/translator/
semantics adequacy bridges; they are not substitutes for the universal K
claims. The candidate `PROOF.md` and generation records are likewise not proof
premises.

Excluded behavior is non-integer elements, non-list or infinite iterables,
rebinding the pinned builtin `abs`, exceptional initial machine states, and
alternate call frames. These exclusions do not narrow the prompt's material
HumanEval domain. The theorem is partial correctness; it does not separately
prove a resource bound, the K implementation, or the supplied semantics
itself.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C (trust
and reproducible evidence) all pass. There is no material adequacy gap or
unsound proof extension.

VERDICT: PASS
LEGITIMACY: LEGIT
