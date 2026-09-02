# Independent adversarial audit — 37-sort-even

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. I reconstructed every positive proof
from source, verified that the only operational bridge has an independently
proved bridge-free theorem over the identical complete context, mechanically
pinned the claim body to trusted regeneration of `solution.mpy`, and obtained a
meaningful failure from a fresh false-result mutation.

Candidate `PROOF.md`, prebuilt definitions, logs, and generation traces were
treated only as untrusted claims. No candidate cache or compiled definition was
used.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `37-sort-even`;
- condition `kit-semantics`;
- `record_layout: pipeline-v3`;
- `semantics_mode: SUPPLIED_SEMANTICS`;
- the mounted paths under its `container_paths` map.

The mode and mounts are consistent: `/reference/reference-semantics` exists and
is a real directory. There was no infrastructure breach.

I read `/audit-campaign-lock.json` and every pipeline-v3 record required by the
prompt: `/run.json`, `/task.json`, `/generation-result.json`, invocation,
metrics, runtime metrics, usage, last response, complete output log, generation
prompt, and the structured trace. The trace contains one 672-line JSONL file;
all lines parsed. Generation records claim success, but none was accepted as
proof evidence.

Independent checks established:

- the campaign lock JSON is exactly equal to the campaign block in
  `/audit-input.json`, and its SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`;
- all required records are readable regular files/directories of the required
  type, with no required symlink;
- all recorded file hashes for the prompt, translator, canonical solution,
  manifests, metrics, prompt, logs, usage, and trace file match;
- the pipeline-v3 trace-tree digest is
  `fb52df9b62f5e96ddc46f797cb2c8227c30d1301f1d11637c6000a60ad1d13ed`,
  matching `usage.json`;
- the mounted candidate's pipeline tree digest is
  `519eee3351c9ab00c6ccdca001102e514f9774868f55c49349d14183eb9c157c`,
  matching both invocation and stage-result workspace hashes;
- candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounted versions;
- all 25 entries below candidate and trusted `reference-semantics/` match
  recursively in relative path, entry type, and file content; neither tree
  contains symlinks or unsupported entries;
- both semantics trees have pipeline digest
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  matching the task manifest and audit-input manifest hash; and
- all six required candidate proof artifacts are present as regular files.

The launcher also records alternate audit-side aggregate digests. I did not
substitute those opaque serializers for content checks: the review separately
checked every semantics entry, every critical file hash, and the pipeline
workspace digest that binds the candidate mount to the generation result.

Evidence:

- [integrity checker](/audit-output/evidence/integrity_check.py)
- [integrity log](/audit-output/evidence/stage1-integrity.log)
- [generation-record reader](/audit-output/evidence/inspect_generation_records.py)
- [generation-record log](/audit-output/evidence/stage1-generation-records.log)

Stage 1 result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From trusted `prompt.py` and `canonical.py`: for an input list `l`, return a
list of the same length in which every odd-indexed value is unchanged and the
multiset of values originally at even indices appears in ascending order at
those even indices. The documented examples are:

- `[1,2,3] -> [1,2,3]`;
- `[5,6,3,4] -> [3,6,5,4]`.

As with Python's `sorted`, the ordinary defined domain requires the values at
even positions to be mutually sortable. Odd-position values need not be
comparable because neither implementation sorts them.

### Candidate implementation

`solution.py` makes a shallow list copy, computes
`sorted(l[::2])`, and writes those sorted values into indices `2*i` for
`i = 0 .. (len(l)+1)//2-1`. This is a different but equivalent algorithm to the
canonical zip-based implementation. It does not mutate the input list.

Trusted regeneration:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy   exit 0
cmp -s regenerated-solution.mpy solution.mpy               exit 0
```

Both files have SHA-256
`c25e5d64b696017be3aa254ddf81cecdb15f4ddf770c164a9c197e2773535280`.

The independent differential test imports the copied trusted canonical and
candidate entry points. It checks both examples; lengths 0 through 5 as named
boundary cases; empty and singleton inputs; odd/even lengths; duplicates,
negatives, already-sorted and reverse even projections; strings and floats;
and dictionaries confined to odd positions. It then exhaustively checks every
integer list of lengths 0 through 6 over `{-2,-1,0,1,2}` and 5,000 deterministic
generated integer lists of lengths 0 through 40.

Result: **24,543 cases, zero mismatches**, with input preservation, fresh-result,
odd-position, and sorted-even-projection assertions also passing.

Evidence:

- [regeneration log](/audit-output/evidence/stage2-regeneration.log)
- [independent differential script](/audit-output/evidence/differential_test.py)
- [differential log](/audit-output/evidence/stage2-differential.log)

Stage 2 result: **PASS**.

## 3. Clean proof reconstruction

All needed sources were copied to `/tmp/audit-work/37-sort-even`. The supplied
semantics came from the trusted tree; candidate `runtime-kompiled`,
`verification-kompiled`, `verification-no-bridge-kompiled`, and all other
candidate caches were ignored. The live toolchain is K `v7.1.293`.

### Concrete definition

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit 0. A reviewer-authored six-case assertion program then ran with:

```text
krun audit-smoke.mpy --definition runtime-kompiled
```

Exit 0; the final configuration had `<k> .K </k>`, `<exc> NoExc </exc>`,
and `<exit-code> 0 </exit-code>`. The heap explicitly contained the expected
results, including `[3,6,5,4]` and `[3,8,9]`.

### Bridge-free definition and connection claim

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION-NO-BRIDGE --syntax-module MPY-SYNTAX \
  --output-definition verification-no-bridge-kompiled
```

Exit 0.

```text
kprove spec-connection.k \
  --definition verification-no-bridge-kompiled \
  --spec-module SPEC-CONNECTION
```

Output `#Top`; exit 0.

### Target proof definition and claims

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Exit 0.

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Output `#Top`; exit 0. This invocation loads and proves both claims in
`SPEC`, which is required because the entry proof uses the loop claim as a
circularity. Selecting `SPEC.loop-inv` separately also printed `#Top` and
exited 0.

Compiler warnings concern known non-exhaustive fixed-semantics functions and
unused pattern variables; none is a build or proof error. Relevant
`valSeqAt` totalization is discussed in Stages 5 and 7.

Evidence:

- [command manifest](/audit-output/evidence/command-manifest.md)
- [LLVM build](/audit-output/evidence/stage3-kompile-llvm.log)
- [concrete execution](/audit-output/evidence/stage3-krun-smoke.log)
- [bridge-free build](/audit-output/evidence/stage3-kompile-no-bridge.log)
- [connection proof](/audit-output/evidence/stage3-kprove-connection.log)
- [target build](/audit-output/evidence/stage3-kompile-verification.log)
- [all target claims](/audit-output/evidence/stage3-kprove-target-all.log)
- [selected loop claim](/audit-output/evidence/stage3-kprove-loop-inv.log)

Stage 3 result: **PASS**.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC-CONNECTION.loop-connection` starts at the exact remaining fixed-semantics
loop configuration. It quantifies over current result sequence `CUR`, sorted
sequence `SORTED`, slice `SLICE`, original input `VS`, remaining range
`rangeObj(I,C,1)`, old local `i`, and builtin scope `B`, with `I >= 0`. It
executes the exact loop body, the sole remaining `Return(result)` statement,
`#endcall`, environment/scope restoration, and frame pop. It returns `ref(0)`
and changes heap location 0 to `fillEven(CUR,SORTED,I,C)` while preserving
locations 1 and 2 and all explicitly framed observable cells.

`SPEC.loop-inv` is the same operational statement specialized to the real
entry values: heap location 1 is the even-index projection of `VS`, location 2
is `sortVS` of that projection, and the builtin scope is fixed.

`SPEC.sort-even` has no strengthening `requires` clause. From the complete
initial MPY configuration and an arbitrary `ValSeq VS`, it loads the function
binding and calls `sort_even(list(VS))`. On termination it returns `ref(0)`,
whose heap value is:

```text
sortEvenResult(VS)
 = fillEven(
     VS,
     sortVS(buildVS(VS, 0, vsLen(VS), 2)),
     0,
     evenCount(vsLen(VS)))
```

The post-state also fixes the exact two intermediate allocations, module
binding, scope counter, stack, return state, exception state, and exit code.
The returned result is not free, existential, tautological, or constrained by
only a one-way implication.

### Satisfiability and concrete substitution

The entry precondition is realized by the standard initial configuration with
`VS = [5,6,3,4]`. A corresponding loop/connection pre-state is realized with
`I=0`, `C=2`, `CUR=[5,6,3,4]`, `SLICE=[5,3]`, `SORTED=[3,5]`, old `i=0`,
and `B=builtinsScope`.

Both trusted canonical Python and candidate Python return `[3,6,5,4]`. A fresh
ground K claim replaces all result summaries with explicit `ValSeq`
constructors and proves:

```text
[5,6,3,4] -> [3,6,5,4]
```

It printed `#Top` and exited 0.

### Mechanical program identity

The entry `<k>` term loads:

```text
Module(FuncDef("sort_even", Params("l"), sortEvenBody))
```

`program_identity.py` first requires byte identity with trusted regeneration,
then expands `sortEvenBody` and `sortEvenLoopBody` and compares the normalized
constructor term to the third argument of the regenerated `FuncDef`. Function
name, parameter constructor, and all 386 normalized body characters match.
This is semantically inert macro normalization, not a substituted program.

### Body sensitivity

I changed the loop's actual executed target constructor from `2*i` to
`2*i+1`, rebuilt a distinct bridge-free definition, and reran the connection
claim. The mutation built successfully, but `kprove` exited 1 with
`WarnStuckClaimState`. Its residual requires the false equality between:

```text
setVSAt(CUR, 2*I+1, valSeqAt(SORTED,I))
setVSAt(CUR, 2*I,   valSeqAt(SORTED,I))
```

Thus the connection proof is sensitive to the displaced program body itself,
not merely to an external `solution.py` file.

Evidence:

- [constructor identity checker](/audit-output/evidence/program_identity.py)
- [identity log](/audit-output/evidence/stage4-program-identity.log)
- [ground witness claim](/audit-output/evidence/audit-witness.k)
- [ground witness proof](/audit-output/evidence/stage4-kprove-witness.log)
- [body mutation diff](/audit-output/evidence/stage4-body-mutation.diff)
- [mutated verification](/audit-output/evidence/verification-body-mutated.k)
- [body-sensitivity residual](/audit-output/evidence/stage4-kprove-body-mutation.log)

Stage 4 result: **PASS**.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The machine-generated inventory contains the complete source text, location,
attributes, and role for every declaration and rule in the supplied semantics,
`verification.k`, `spec.k`, and `spec-connection.k`:

- 232 `syntax` declarations;
- 702 rules;
- 5 contexts;
- 1 configuration;
- 3 claims;
- all module, import, and require structure.

No `functional`, `simplification`, `concrete`, `symbol`, `no-evaluators`, or
`owise` attribute occurs in proof-local `verification.k`. It has exactly one
priority rule: the loop bridge at priority 40.

[The complete 153 KB rule inventory](/audit-output/evidence/rule-inventory.md)
is the authoritative per-rule enumeration. Per-file rule counts and decisions
are:

| Supplied file | Rules | Decision |
|---|---:|---|
| `assert.k` | 3 | Accepted fixed assertion/exception rules; only reviewer smoke uses them. |
| `bool.k` | 13 | Accepted fixed Boolean/short-circuit rules; no result-bearing proof shortcut. |
| `builtins.k` | 137 | Accepted fixed builtin subset. Used `len`, `list`, and `range` rules match their Python behavior on the claimed path. |
| `call.k` | 21 | Accepted. Used rules preserve callee lookup, left-to-right argument evaluation, builtin dispatch, and user-frame creation. |
| `comprehension.k` | 7 | Accepted fixed unused macro rules; no used constructor matches them. |
| `concrete.k` | 16 | Accepted concrete-only rules; unused by Haskell proof and no target-answer rule. |
| `controls.k` | 34 | Accepted. Used assignment and `for` rules preserve evaluation order, binding, loop continuation, and state changes. |
| `core.k` | 46 | Accepted configuration, allocation, load, lookup, and sequence-helper rules. Used `setVSAt` equations preserve non-target positions. |
| `dict.k` | 28 | Accepted fixed subset. Its generic subscript-target rules correctly perform the used heap-list update. |
| `float.k` | 121 | Accepted supplied opaque/concrete float boundaries; unused by the target proof. Duplicate mixed-operation equations have identical right sides. |
| `functions.k` | 15 | Accepted. Used definition, parameter binding, return, and pop rules explicitly preserve/restore every relevant cell. |
| `int.k` | 16 | Accepted on the path. `+`, `*`, and floor `//` are exact; divisor is fixed at nonzero 2. |
| `iter.k` | 0 | Declaration-only iterator protocol. |
| `list.k` | 27 | Accepted fixed list constructors/operations; no overlapping list operation changes the target path. |
| `methods.k` | 75 | Accepted fixed unused method subset; no used constructor matches it. |
| `operators.k` | 10 | Accepted dispatch and dereference rules; relevant priorities correctly precede generic dispatch. |
| `range.k` | 6 | Accepted. Step 1 yields exactly `0 <= i < C` and terminates at the boundary. |
| `set.k` | 12 | Accepted fixed unused set subset. |
| `sort.k` | 19 | Accepted supplied external sort boundary and concrete insertion-sort equations; discussed below. |
| `str.k` | 28 | Accepted fixed unused runtime-string operations; string tokens used as names do not invoke these rules. |
| `subscript.k` | 40 | Accepted on the path. Step-2 slicing and in-bounds indexing match the program; evaluation contexts enforce order. |
| `syntax.k` | 0 | All submitted constructors are declared with the expected strictness/context behavior. |
| `tuple.k` | 21 | Accepted fixed target-binding rule used for loop variable `i`; other tuple rules are inert. |
| `verification.k` | 7 | All seven proof-local rules accepted individually below. |

The supplied semantics is intentionally a Python subset. Unused rules were
checked for pattern overlap with the submitted constructor path; none can
preempt or fabricate the target result. Known out-of-subset behavior such as
zero slice steps, out-of-bounds exceptions, floats, closures escaping their
frame, and unsupported methods is not reached by the submitted program on its
intended inputs. I found no rule warranting an “unsound” label, so there is no
false-conclusion witness to report.

The exact used-path mapping, including declaration and rule locations, is
[used-construct-map.md](/audit-output/evidence/used-construct-map.md).

### Proof-local rules

1. `sortEvenLoopBody` macro equation exactly expands to the translated indexed
   assignment. Accepted as a syntax alias.
2. `sortEvenBody` macro equation, after recursive loop-macro expansion, exactly
   matches regenerated `solution.mpy`. Accepted as a syntax alias.
3. `evenCount(N)` has one unconditional equation. It is algebraically the fixed
   Python floor-division rule for `(N+1)//2`; entry use has `N=vsLen(VS)>=0`.
4. `fillEven` base equation applies when `I>=STOP`.
5. `fillEven` step equation applies when `I<STOP`, performs the exact `2*I`
   write from sorted index `I`, and advances `I`. The two guards are disjoint
   and exhaustive; recursion descends toward the base case.
6. `sortEvenResult` has one unconditional equation composing the original
   sequence, exact even projection, supplied sort primitive, even count, and
   `fillEven`. It replaces no program term.
7. The priority-40 loop rule is an operational bridge. Its complete normalized
   operational region—`<k>` continuation, binding scopes, heap, counters,
   stack/frame, return, exception, exit cells, and guard—is character-for-
   character identical to `SPEC-CONNECTION.loop-connection`. The connection
   module imports `VERIFICATION-NO-BRIDGE`, which imports only
   `VERIFICATION-BASE`; it cannot use the bridge. The independent connection
   proof printed `#Top`, and the body mutation invalidated it.

The bridge introduces no fresh or opaque value. It changes exactly what its
connection theorem changes: result heap location 0, environment, scopes,
scope counter, stack, and returned reference. It admits no arbitrary
continuation or extra frame and preserves heap locations 1/2, heap counter,
return, exception, and exit state exactly.

### `sortVS` boundary

`sortVS(ValSeq)` is the only result-bearing supplied opaque primitive reached by
this proof. It is not program-defined code: it is the fixed semantics'
representation of external Python `sorted`. The actual submitted call executes
through fixed lookup, argument evaluation, builtin dispatch, and allocation to
produce `sortVS(even-projection)`; no proof-local bridge replaces that call.

The K theorem is interpretation-parametric in this returned sequence and states
the final wrapper result explicitly in terms of `sortVS`. The human statement
that this term is the ascending, length-preserving permutation of sortable
inputs is a named supplied-semantics contract, not something the loop theorem
proves. This is an acceptable external primitive boundary under the Kit
contract, not a circular summary of program-defined code.

Finite evidence does not replace that contract:

- the reviewer LLVM smoke has six explicit expected results;
- a second generated K program ran 26 explicit-oracle integer cases with zero
  failed assertions;
- the 24,543-case Python differential validates candidate versus canonical
  Python, not universal K `sortVS` meaning.

An initial optional 134-assertion K program was killed during parsing by the
8 GB limit (exit 137), before execution. It is retained as infrastructure
evidence and was superseded by the bounded 26-case run; it is not proof evidence
or a candidate defect.

Evidence:

- [extension attribute log](/audit-output/evidence/stage5-extension-flags.log)
- [bridge context checker](/audit-output/evidence/bridge_context_check.py)
- [bridge context result](/audit-output/evidence/stage5-bridge-context.log)
- [bounded K differential generator](/audit-output/evidence/generate_k_differential.py)
- [bounded K differential source](/audit-output/evidence/audit-k-differential.py)
- [bounded K differential log](/audit-output/evidence/stage5-k-differential.log)
- [superseded oversized log](/audit-output/evidence/stage5-k-differential-oversized.log)

Stage 5 result: **PASS**.

## 6. Fresh non-vacuity test

Candidate `spec-vacuity.k` was inspected only as untrusted prior evidence. I
created a different reviewer-authored mutation for the satisfiable input
`[9,8,3]`.

Trusted canonical Python and candidate Python both return `[3,8,9]`; the
concrete reviewer K smoke asserts the same. The fresh mutation executes the
exact submitted function but demands that heap location 0 remain the false
unchanged list `[9,8,3]`. Intermediate slice `[9,3]` and sorted value `[3,9]`
are constrained correctly, isolating the mutation to the returned result.

First:

```text
kprove audit-false-result.k --definition verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT --dry-run
```

Exit 0, proving the mutation parses and builds.

Then:

```text
kprove audit-false-result.k --definition verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT
```

Exit 1 with `WarnStuckClaimState`. The residual is a normal final
configuration whose heap location 0 explicitly contains `[3,8,9]`; it cannot
unify with the false demanded `[9,8,3]`. This is an expected unmet result
obligation, not a parser error, timeout, missing import, crash, or unreachable
claim.

Evidence:

- [fresh false mutation](/audit-output/evidence/audit-false-result.k)
- [mutation build log](/audit-output/evidence/stage6-false-mutation-build.log)
- [mutation proof residual](/audit-output/evidence/stage6-false-mutation-proof.log)

Stage 6 result: **PASS**.

## 7. Proven versus assumed accounting

### What is machine-checked

Under the exact supplied MPY definition plus the audited proof-local
definitions, for every symbolic `ValSeq VS`, executing the exact regenerated
`sort_even` binding from the stated initial configuration reaches, on
termination, `ref(0)` with:

- heap 0 equal to `sortEvenResult(VS)`;
- heap 1 equal to the even-index projection of `VS`;
- heap 2 equal to `sortVS` of that projection;
- exactly three allocations;
- module binding and builtin scope as stated;
- the local call scope removed and caller environment restored;
- empty call stack, `noRet`, `NoExc`, and exit code 0.

The bridge-free universal theorem separately establishes that the exact
remaining loop, return, and frame cleanup computes `fillEven` over its complete
bridge domain. Fixed `setVSAt` equations and the validated recurrence imply
that only even indices are changed and odd indices are preserved.

This is a partial-correctness theorem in the Kit sense. It is not merely a
test result, candidate log claim, or acceptance of a prior `#Top`.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, compiler, Haskell/LLVM backends, and reachability logic | All builds, execution, and proofs | Necessary proof-checker trust; acceptable. Fresh reconstruction and expected-failure discrimination reduce operational uncertainty but do not prove the toolchain. |
| Trusted supplied MPY semantics | All modeled binding, control, heap, calls, lists, slicing, arithmetic, and sorting | Required foundation selected by `SUPPLIED_SEMANTICS`; acceptable. The exact tree was integrity-checked and the used subset was statically reviewed. |
| Trusted `py2mpy.py` | Python-to-constructor translation and program identity | Acceptable fixed frontend trust. Byte regeneration plus constructor-level macro comparison independently pins this artifact. |
| External bare `list(VS)` input representation | Relates the claim's unboxed read-only input value to an external Python list argument | Acceptable supplied-semantics convention. The function copies it before writes; the output contract does not depend on input alias mutation. |
| `sortVS` ascending, length-preserving permutation contract | Determines every value written at an even result index and therefore the human-facing “sorted” conclusion | Acceptable fixed external builtin boundary. The formal theorem remains explicit/parametric; concrete K and Python testing are finite support only. |
| Mathematical integer model and supported list subset | Index/count arithmetic, no integer overflow | Adequate for HumanEval integer-list behavior; Python integers are unbounded. Unsupported CPython effects such as custom comparison side effects and concurrency are outside the supplied model, not silently proved. |
| Manual body macros and manually duplicated bridge theorem/rule | Artifact maintenance | No defect for this immutable candidate: trusted regeneration, mechanical expansion, exact context comparison, and body-sensitivity testing pin the submitted artifact. |

No proof-local primitive, lemma, totality annotation, or priority rule smuggles
the task answer. No program-defined helper is treated as external. Differential
testing supports only program equivalence and finite concrete behavior; it is
not used as a substitute for either positive K proof.

Stage 7 result: **PASS**.

## Decision

All seven required stages pass. The proof closes from a clean build, constrains
the actual returned list, executes the exact regenerated program up to one
universally justified exact-context loop acceleration, covers the unrestricted
symbolic `ValSeq` formal domain without a finite-size restriction, and has no
material source-contract adequacy gap. The supplied `sortVS` meaning remains an
explicit external semantics boundary, which is legitimate for this
`SUPPLIED_SEMANTICS` condition.

VERDICT: PASS
LEGITIMACY: LEGIT
