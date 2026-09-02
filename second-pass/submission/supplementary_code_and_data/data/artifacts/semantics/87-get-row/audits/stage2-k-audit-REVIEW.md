# Independent adversarial audit: HumanEval 87 `get_row`

## Executive finding

The submitted K artifacts reconstruct successfully and appear sound for the
two configurations they actually state. They do **not** prove the HumanEval
contract over arbitrary finite ragged integer lists. The only formal input
shapes are:

1. the empty outer list; and
2. exactly three rows having lengths `0`, `1`, and `3`.

The second claim is symbolic only in the four element values and target value;
it is still a fixed-size unrolling. There is no invariant, induction, list-tail
variable, or auxiliary reachability claim extending the result to other outer
lengths or row lengths. This is a material narrowing of an unrestricted source
contract. Under the benchmark-specific decision rule, the Kit status
`SOUND-BUT-LIMITED` maps to `FAIL / NOT_LEGIT`.

No proof-local unsound rule or result oracle was found. The failure is theorem
adequacy, not a false equation or a failed positive `kprove` run.

## 1. Input and provenance integrity

### Declared layout and required records

`/audit-input.json` declares:

- problem `87-get-row`;
- condition `semantics`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = SUPPLIED_SEMANTICS`;
- `mount_reference_semantics = true`.

The mode and mounts are consistent: `/reference/reference-semantics` exists as
a real directory. The following required launcher records were present,
readable, regular files, and not symlinks:

- `/audit-input.json`, `/audit-campaign-lock.json`;
- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`;
- `/generation-evidence/metrics.json`;
- `/generation-evidence/codex-last.txt`;
- `/generation-evidence/codex-output.log`;
- `/generation-evidence/prompt.txt`.

`usage.json` was present and inspected. Historical `runtime-metrics.json` is
not required for this legacy-selected layout and was not reconstructed. The
trace directory and all candidate/reference directories were real directories,
and a recursive scan found no symlinks under `/candidate`, `/reference`, or
`/generation-evidence`.

The `audit_campaign` object in `/audit-input.json` is structurally equal to
`/audit-campaign-lock.json`. The lock's independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the audit manifest.

### Independent hashes and record inspection

Selected direct hashes all match the corresponding recorded values:

| Artifact | Independently observed SHA-256 |
|---|---|
| `/run.json` | `321818dc4f5c9795e25ea800ab12c1b1e5cf0bcc70b308443b9f08339a122db0` |
| `/task.json` | `ea3b2cb5ae1b013ed78273bf1b53b17eb08d32cd92529a36a4ee99a34befa7e3` |
| `/generation-result.json` | `4b532fe2dd6dfeaa360ec0c9fe21ca96e361b08219bdd31078ad7ae43459f336` |
| `invocation.json` | `6a38ea9b53d805ff31ef2f9774b7006e2cfb9177c4ccd1d8e38fb1c1f7699dae` |
| `metrics.json` | `eb3260a10a90e2fde989d6f8fc5bd3a2d02ff8034fb5de2a4852f25b40d549bc` |
| `usage.json` | `3451219d7e97663d3501cd6c1c22e8b2d723e0d26d18d3715510a1648e642be4` |
| `codex-last.txt` | `ab89c073987a4651e3d50a4df27a5ec63122b892df299dc233b7f4a54dbdaa14` |
| `codex-output.log` | `7a1cdf2c8844f4d19b8323057c839687f4d425b8b0986eaa9c643feb0a61e90f` |
| generation prompt | `3ccfe05a1e1620ec7e34cf354de6eeb973da0fe27a12a04f4ac62b0a78eeec09` |
| trace JSONL file | `cc0dd8d850922b762aaa5ea12c5f59c5e92f68b71d34007f5bec2e3e79f63ba8` |

Using the pipeline's published `sha256_tree` implementation, the mounted
candidate hashes to
`1b8a06d34c6aa16fc3c91d1ccdd21c9151b5ee09633bf808472984ddc70db694`,
which equals the retained/workspace digest in both the invocation and stage-1
result. The trusted and candidate semantics trees both hash to
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
matching the separately recorded manifest-tree field. The trace tree hashes to
`69064f475594879a86afb0f25c8d4817c1e701997ef41cd39bbe96660ce42065`,
matching `usage.json`'s source-trace digest. The launcher also records separate
mount-digest fields distinct from the explicitly named manifest digests; the
audit did not substitute the pipeline algorithm for those fields and instead
checked every mounted file directly.

The candidate prompt and translator are byte-identical to their trusted
versions. `diff -qr --no-dereference` between the candidate and trusted
semantics trees exits `0`; the per-file hash lists are identical. Thus there
are no missing, additional, changed, mistyped, unsupported, or symlinked
candidate semantics entries.

The entire 162-line structured trace parsed as JSON, and all 8,069 lines of the
generation output log were read and summarized. They claim successful
generation and `#Top`, but none of those claims was used as proof evidence.
The complete commands and bounded summary are in
[stage1_integrity.sh](/audit-output/evidence/stage1_integrity.sh) and
[stage1_integrity.log](/audit-output/evidence/stage1_integrity.log).

**Stage 1 result: PASS.** No audit-infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt asks `get_row(lst, x)` to search a two-dimensional nested
list whose rows may have different lengths. For integer `x`, it must return all
matching zero-based `(row, column)` coordinates. Rows are ordered ascending;
within each row, columns are ordered descending. The prompt places no bound on
the number of rows or any row length.

The trusted canonical function constructs all coordinates and then applies
stable sorts to obtain that order. The submitted function uses an equivalent
algorithm: it enumerates rows from left to right, iterates every row from
`len(row)-1` down through `0`, and appends a coordinate exactly when the element
equals `x`.

### Translator identity

The exact reconstruction command was:

```text
python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/solution.regenerated.mpy
```

It exited `0`. `cmp -s` against `/candidate/solution.mpy` exited `0`; both files
have SHA-256
`77095066c6cb51ab5f0c562830989906ecdc63f76b1d00d6cc3b74b88f7ac63f`.

### Independent differential testing

The reviewer-authored differential test imports the two functions from
`/reference/canonical.py` and `/candidate/solution.py`; it does not reuse any K
equation. It covers:

- all three documented examples;
- seven explicit empty, singleton, no-match, repeated-match, negative-integer,
  ragged, and large-integer boundaries;
- all 7,140 cases formed by outer lengths `0..3`, row lengths `0..2`, values and
  targets in `{-1,0,1}`;
- 2,000 deterministic random ragged integer cases with up to nine rows and
  twelve columns.

All 9,150 cases matched. The exact script, command wrapper, and output are
[differential_test.py](/audit-output/evidence/differential_test.py),
[stage2_fidelity.sh](/audit-output/evidence/stage2_fidelity.sh), and
[stage2_fidelity.log](/audit-output/evidence/stage2_fidelity.log).
This is finite implementation-fidelity evidence, not a universal proof.

**Stage 2 result: PASS.**

## 3. Clean proof reconstruction

No candidate-built definition or cache was copied or used. The scratch tree at
`/tmp/audit-work/rebuild` was assembled from the candidate source K files and a
fresh copy of the trusted `/reference/reference-semantics`. The scratch
semantics was recursively compared back to the trusted tree before building.
The observed `kompile` and `kprove` version was K `v7.1.293`.

### Concrete definition

The exact build/run commands were:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

krun k-concrete-tests.mpy --definition audit-runtime-kompiled
```

Both exited `0`. The reviewer test program was generated by the trusted
translator and asserted seven normal/boundary results, including the exact
symbolic-claim shape instantiated as `[[], [5], [5,6,5]]`. The final K
configuration had `<exit-code> 0`.

### Proof definition and each positive claim

The fresh proof build was:

```text
kompile verification.k \
  --backend haskell \
  --main-module GET-ROW-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

It exited `0`. I split the two unlabeled candidate claims into otherwise
identical labeled modules so that each could be run independently:

```text
kprove spec-empty.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-EMPTY-SPEC
# output: #Top; exit: 0

kprove spec-shape.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SHAPE-SPEC
# output: #Top; exit: 0
```

The original combined candidate command was also rerun:

```text
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module GET-ROW-SPEC
# output: #Top; exit: 0
```

All commands, statuses, warnings, and bounded output are preserved in
[stage3_rebuild.sh](/audit-output/evidence/stage3_rebuild.sh) and
[stage3_rebuild.log](/audit-output/evidence/stage3_rebuild.log). The split
claims and reviewer concrete program are preserved under
[reviewer-k](/audit-output/evidence/reviewer-k).

**Stage 3 result: PASS.**

## 4. Adequacy and real-program pinning

### Plain-language meaning of each entry claim

**Empty claim.** Starting from the exact clean module configuration shown in
the claim, with the `get_row` closure in scope, an empty outer list, and any
integer target `X`, the call returns reference `0`. Heap location `0` contains
the newly allocated empty result and location `1` contains the empty eager
`enumerate` materialization. The call stack, return state, exception, and exit
code finish normally.

**Fixed-shape claim.** Starting from the exact clean configuration with three
row objects:

```text
row 0 = []
row 1 = [A]
row 2 = [B, C, D]
```

where `A,B,C,D,X` are arbitrary K integers, the call returns new reference `3`.
Its list is:

```text
addMatch(A,X,1,0,
  addMatch(D,X,2,2,
    addMatch(C,X,2,1,
      addMatch(B,X,2,0,[]))))
```

The input rows remain unchanged, heap location `4` is the eager list of
enumeration pairs, the allocation counter becomes `5`, and control terminates
normally. This covers all equality/non-equality choices for those four
positions, but no other position exists in the theorem.

Both preconditions are satisfiable. Ground substitutions were checked against
both Python functions:

```text
empty: lst=[], x=7 -> []
shape: lst=[[],[5],[5,6,5]], x=5
       -> [(1,0),(2,2),(2,0)]
```

The claim-side `addMatch` expression produces the same shape result. Evidence
is in [claim_witnesses.py](/audit-output/evidence/claim_witnesses.py) and
[stage4_witnesses.log](/audit-output/evidence/stage4_witnesses.log).

### Mechanical program pinning

The claim does not load `Module(FuncDef(...))`; it directly installs a closure
whose body is named `getRowBody`. This omission is inert only if that term is
the submitted function body. The following chain establishes it:

1. Trusted translation is byte-identical to submitted `solution.mpy`.
2. `kast` parsed the freshly translated module and an independently transcribed
   `Stmts` term. Extracting the only `FuncDef` body produced equal KAST trees
   with the same SHA-256
   `24e0bd3d67aec6d125b6207f43eb2a767a026382f359cecf674dddbd6f68cffa`.
   Function name and parameters were exactly `get_row(lst,x)`.
3. A separately compiled K definition compared that transcribed term and
   closure with `getRowBody` and `getRowClosure`; `kprove` printed `#Top` and
   exited `0`. The backend reports these as trivial after frontend function
   normalization, which is the desired constructor equality.

See
[constructor_compare.py](/audit-output/evidence/constructor_compare.py),
[stage4_constructor_compare.log](/audit-output/evidence/stage4_constructor_compare.log),
and [stage4_pinning.log](/audit-output/evidence/stage4_pinning.log).
Failed preliminary encodings of the same identity check are preserved as
`stage4_pinning_attempt*.log`; they were parser/proof-module diagnostics and
are not counted as positive target-proof runs.

The closure fixes defining environment `0`, which is the module scope used by
the regenerated one-function module. The claims then execute the actual body
under the supplied operational semantics. No helper or loop claim substitutes
for execution.

### Body sensitivity

As a separate operational-sensitivity test, the reviewer changed the inner
range to ascending `range(0,len(row),1)`, rebuilt a fresh Haskell definition
successfully, and ran the original descending-result shape obligation. The
proof exited `1` with `WarnStuckClaimState`. A reachable residual had
`B = X`, `C = X` and an actual result prefix `[(2,0),(2,1)]`, which cannot match
the descending postcondition. This confirms that the theorem depends on the
executed body and is not closed solely by `addMatch`.

### Fatal adequacy gap

The source contract ranges over arbitrary finite ragged nested lists. The
formal claim set covers only outer length `0` or outer length `3` with row
lengths exactly `0,1,3`. For example, no claim covers:

- `[[1]]`;
- `[[],[]]`;
- the prompt's first `6,6,6` example;
- a fourth row;
- a row of length `2`, `4`, or any unbounded length.

The concrete tests and Python differential sample such inputs, but they do not
extend a reachability theorem. The symbolic values in the fixed-shape claim
quantify over data, not shape. Thus the proof is a finite bounded unrolling,
not an unrestricted proof.

**Stage 4 result: FAIL for intent adequacy.** Real-program pinning and result
constraint pass; domain coverage fails materially.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored inventory scanned all 24 supplied K source files,
candidate `verification.k`, and candidate `spec.k`. It contains 937
line-addressed items:

| Kind | Count |
|---|---:|
| syntax declarations | 230 |
| configuration declarations | 1 |
| contexts | 5 |
| rules | 699 |
| claims | 2 |

Attribute totals include 148 `function`, 108 `total`, zero `functional`, 22
`no-evaluators` opaque declarations, 45 priority-bearing rules, zero
`simplification`, 35 `concrete`, 26 `owise`, four macro-bearing declarations,
and the strictness-bearing syntax blocks. Every item includes its complete
compressed statement, flags, and a per-item disposition. See
[rule_inventory.tsv](/audit-output/evidence/rule_inventory.tsv), generated by
[rule_inventory.py](/audit-output/evidence/rule_inventory.py); the exact run is
in [stage5_static_inventory.log](/audit-output/evidence/stage5_static_inventory.log).

All supplied entries are fixed semantics rather than candidate proof
extensions. They were still inventoried, their module/import structure was
read, and every construct on the submitted execution path was reviewed in
detail. The concrete-only `MPY-CONCRETE` module is included in the inventory
but is not imported by the Haskell proof module.

### Candidate proof-extension inventory

| Extension | Class, domain, and effect | Static decision |
|---|---|---|
| `getRowBody : Stmts [function]` and its equation | Definitional constant; no guard. Expands to the exact submitted statement sequence. It changes no cells itself; fixed semantics executes the expanded statements. | Sound. Constructor equality and body sensitivity are independently evidenced. It is not an operational bridge. |
| `getRowClosure : Val [function]` and its equation | Definitional constant; no guard. Produces `closureVal(("lst","x"), getRowBody, 0)`. | Sound for the directly installed binding. It faithfully represents the sole generated function at module environment `0`. |
| `addMatch(Int,Int,Int,Int,ValSeq) [function,total]` | Mathematical result summary used only in the postcondition. First equation prepends `(R,C)` when `V == X`; second returns `REST` when `V != X`. | Sound. Guards are disjoint and exhaustive over K integers, right-hand sides do not overlap, and there is no recursion or nontermination. It does not replace program execution. |
| two reachability claims | Entry theorems described in Stage 4. | Both reconstruct and are result-constraining, but both are materially domain-limited. |

There are no proof-local priority rules, simplification rules, opaque symbols,
operational bridges, program-call interceptions, or unproved helper claims.
Accordingly there is no circular use of a shared oracle in execution and the
postcondition.

### Used semantics path

The complete constructor-to-rule map is
[used_construct_map.md](/audit-output/evidence/used_construct_map.md). In
summary:

- name lookup selects the scope binding before uniform call routing;
- arguments evaluate left-to-right, bind into a fresh function frame, and the
  body executes before ordinary return/pop;
- list construction allocates the result, while `append` mutates that exact
  heap object and preserves the reference;
- eager `enumerate` preserves row order and materializes `(index,row)` tuples;
- tuple-target unpacking binds both loop variables;
- `len`, integer subtraction/unary minus, and `range` generate precisely
  `n-1,...,0`;
- all generated indices are in bounds, so the semantics' total-but-
  underspecified out-of-bounds `valSeqAt` case is unreachable;
- integer comparison controls the `If`, and tuple construction/append fixes
  coordinate order;
- return restores the caller frame without losing the allocated result.

The semantics models `enumerate` eagerly rather than with a CPython iterator.
For this body, which does not mutate its input during traversal and does not
observe iterator identity, the resulting values, order, and control are
equivalent. K integers are unbounded, matching Python integers for the used
arithmetic. No exceptional index, zero range step, float, string, sort, digest,
dict, set, comprehension, or closure-capture path is reachable.

### Opaque and total symbols

The fixed semantics contains opaque/trusted primitives:

- `md5hexCodes`;
- `sortVS` and `sortKeyVS`;
- float-domain symbols including `intFloatDiv`, `divII`, `floatMod`,
  `floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
  `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
  `sqrtF`;
- concrete-only-equation total symbols `floorFI`, `toF`, and `ceilF`.

None can match a constructor in the submitted program or influence a branch,
result, state cell, exception, or either claim. They remain part of the fixed
semantics trust boundary but are inert here. The proof-local `addMatch` is
total through truthful exhaustive equations and is not opaque.

No candidate/proof-local rule was found unsound, so there is no claimed
unsound rule for which a false-conclusion witness is required. The adverse
finding is narrower: sound rules establish a theorem too small for the source
contract.

**Stage 5 result: PASS for rule soundness; FAIL remains from theorem scope.**

## 6. Fresh non-vacuity test

The fresh reviewer mutation keeps the satisfiable empty-list precondition but
changes the returned heap object from `[]` to the fabricated coordinate list
`[(0,0)]`. Ground witness `lst=[]`, `x=7` returns `[]` in both trusted canonical
Python and generated Python, so the mutation is demonstrably false.

The mutation first built successfully:

```text
kprove spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY \
  --dry-run
# exit: 0
```

The actual proof run was:

```text
kprove spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY
# exit: 1
```

It failed for the expected semantic reason with `WarnStuckClaimState`. The
residual is a completed call returning `ref(0)` with:

```text
0 |-> list(.ValSeq)
1 |-> list(.ValSeq)
```

which does not unify with the mutated nonempty destination. This is not a
parser error, missing import, timeout, or unrelated crash. The exact mutation,
dry run, proof command, exit statuses, and residual are in
[spec-vacuity.k](/audit-output/evidence/reviewer-k/spec-vacuity.k),
[stage6_nonvacuity.sh](/audit-output/evidence/stage6_nonvacuity.sh),
[stage6_nonvacuity.log](/audit-output/evidence/stage6_nonvacuity.log), and
[stage6_nonvacuity_proof_output.log](/audit-output/evidence/stage6_nonvacuity_proof_output.log).

**Stage 6 result: PASS.** The submitted claims discriminate their stated
results.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Conditional on the supplied semantics and K backend, the proof establishes
partial correctness of the actual submitted function body for:

- every integer target on the empty list; and
- every choice of integer `A,B,C,D,X` on `[[],[A],[B,C,D]]`.

For those inputs, it establishes the exact returned reference, exact result
sequence, preservation of the input rows, the eager-enumeration allocation,
allocation counters, empty stack, normal return state, no exception, and exit
code `0`. The postconditions are not free variables or tautologies. The proof
also concretely reaches termination for those finite configurations.

It does **not** establish anything about other list shapes. In particular, it
does not establish the universal source property “for every finite ragged
integer list.”

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K `v7.1.293`, Haskell/LLVM backend correctness, and built-in Int/Bool/Map/List theories | All `kompile`, `krun`, and `kprove` results | Ordinary formal-tool trust boundary; acceptable and version-recorded. |
| Byte-identical supplied reference semantics | All K execution/proofs | Required fixed semantics boundary. Candidate has no modifications. Used operations were audited; unused opaque operations are inert. |
| Trusted `py2mpy.py` translation relation | Source-to-`solution.mpy` bridge | Launcher-designated trusted input. Fresh byte regeneration plus KAST constructor comparison establishes artifact identity; translator semantic correctness remains an external trust boundary. |
| `getRowBody`/`getRowClosure` equations | Program term executed by both claims | Not assumed: constructor equality is mechanically checked, and a material body mutation invalidates the theorem. |
| `addMatch` | Fixed-shape postcondition | Not assumed: exhaustive, disjoint integer equations define it. |
| Canonical Python implementation | Differential oracle and ground witnesses | Launcher-designated trusted oracle. Supports implementation fidelity only; not part of the K proof. |
| 9,150-case Python differential and seven-case concrete K run | Source/candidate agreement and finite semantics adequacy | Reproducible empirical evidence only. It cannot generalize the K theorem to unproved list sizes. |
| Natural-language reading that list sizes are unrestricted | Gate B comparison | Directly supported by the prompt: rows may differ in length and no bound is stated. The fixed-shape restriction is therefore material. |

### Kit gates and benchmark mapping

- **Gate A — real-program soundness: PASS.** The reconstructed claims execute
  the pinned body under unchanged fixed semantics; proof-local equations are
  truthful; ground states satisfy both preconditions; body and false-result
  mutations are rejected.
- **Gate B — intent adequacy: FAIL.** Two finite shapes do not cover the
  unrestricted HumanEval domain. Generic Kit terminology is
  `SOUND-BUT-LIMITED`.
- **Gate C — trust/evidence auditability: PASS.** Relevant artifacts, exact
  commands, statuses, finite-test scope, and trust boundaries are preserved.

The generation record's `KPROVE_PASSED` marker is accurate only in its narrow
sense that the submitted positive claims closed. It is not evidence that those
claims state the required universal theorem. The benchmark prompt explicitly
maps this material domain narrowing to `FAIL / NOT_LEGIT`, not
`CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
