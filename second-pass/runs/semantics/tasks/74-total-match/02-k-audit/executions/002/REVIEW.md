# Independent adversarial audit: 74-total-match

## Executive conclusion

The submitted Python implementation is correct, its submitted `.mpy` is an
exact fresh translation, its proof claims are domain-adequate and
result-constraining, and all three positive claims reconstruct with `#Top`.
Those facts do not make the proof legitimate. The end-to-end proof imports and
uses a priority-40 operational `For` rule in
`/candidate/verification.k:86`. That rule is false over its declared match
domain and accepts continuation contexts much broader than the loop claim
offered as its justification. Two fresh false-conclusion witnesses close with
`#Top` when the rule is enabled and fail with the expected fixed-semantics
residual when it is removed. The rule therefore makes false claims provable,
and the reconstructed target `#Top` is not usable as a proof of the real
program.

This is a candidate defect, not an infrastructure failure.

## 1. Input and provenance integrity

### Declared layout and required records

`/audit-input.json` declares:

- problem `74-total-match`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance.

I used the mounted paths from `container_paths`, not the host-only provenance
paths. All launcher-required records for this layout are present as real
regular files or real directories:

- `/audit-input.json`, `/audit-campaign-lock.json`;
- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`,
  `/generation-evidence/metrics.json`,
  `/generation-evidence/codex-last.txt`,
  `/generation-evidence/codex-output.log`,
  `/generation-evidence/prompt.txt`;
- the structured trace under `/generation-evidence/codex-trace/`;
- the optional legacy-layout `/generation-evidence/usage.json`, which is
  present and was inspected;
- `/candidate`, `/reference/canonical.py`, `/reference/prompt.py`,
  `/reference/py2mpy.py`, and `/reference/reference-semantics`.

Historical `runtime-metrics.json` is absent, as permitted for
`legacy-selected-stage1`. The campaign-lock JSON is exactly equal to the
`audit_campaign` block, and its SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.

The independent integrity checker is
`evidence/stage1_integrity.py`; its successful command/output record is
`evidence/stage1-integrity.log` (exit 0). It independently verified every
recorded regular-file hash, including the trace JSONL hash recorded in
`generation-result.json`. It also computed pipeline-style tree hashes:

- candidate tree:
  `991f1a0f15e68bb7b2a1c4b196d0492ed27e4492da47094a2899ef6d7e523471`,
  equal to the retained workspace hash in both generation records;
- trusted and candidate semantics trees:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- trace tree:
  `01a9efc64d55824525bae0e3941681af0bb490ba5d729f1337864b26bdfef9b6`,
  equal to `usage.json`'s `source_trace_sha256`.

The earlier `evidence/stage1_integrity.log` is retained for transparency. It
is an obsolete first run of the reviewer script, not a candidate result: that
version incorrectly required `/task.json` to contain the audit input's added
`config` field. The corrected check compares all common fields and checks the
declared config separately.

### Supplied-semantics boundary

The trusted supplied semantics is present, as required by the rendered mode.
The checker recursively compared the 25 entries under the trusted and
candidate semantics directories, including path, entry type, and per-file
SHA-256. There are no missing, additional, changed, mistyped, special, or
symlinked entries. Candidate `prompt.py` and `py2mpy.py` are byte-identical to
the trusted mounts, with recorded hashes
`9662ed6743a83d0c34963151a98c5cdc9d33053cf3b26212adb7ff8abf9e3617`
and
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

### Generation records

`evidence/trace_summary.py` parsed all 303 JSONL records without error and
read the complete 658,413-byte generation log. The bounded summary is
`evidence/generation-trace-summary.log` (exit 0). The records claim prior
successful builds and proofs, but none of those claims or compiled artifacts
was reused.

**Stage 1 result: PASS.** There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt asks `total_match(lst1, lst2)` to accept two lists of
strings, total the number of characters in each list, and return the list with
the smaller total. A tie must return the first list. The trusted canonical
implementation performs exactly those two folds and the `<=` selection.

The candidate implementation uses the same behavior with renamed local
accumulators. It preserves the required signature and returns an original
input list, not a copy.

### Fresh translation

From the scratch tree I ran:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

Both files have SHA-256
`470747b31c31d122130a383ca0b9634c28b09b5d709f3e679033c05f80100d8e`.
The exact command, hashes, `BYTE_IDENTITY_OK`, and exit 0 are in
`evidence/translation-identity.log`.

### Independent differential test

`evidence/differential.py` independently imports the trusted canonical and
candidate entry points and compares them with the direct mathematical choice.
It also checks returned-object identity. Its input scope was:

- all 5 documented examples;
- 14 explicit empty, tie, one-character boundary, empty-string,
  decomposed-Unicode, and emoji cases;
- all 24,336 pairs of lists of length 0 through 3 over
  `["", "a", "bb", "é", "🙂"]`;
- 10,000 deterministic generated pairs (seed 740074), each list and string
  having length at most 8.

The run made 34,355 comparisons with zero value mismatches and zero
object-identity mismatches. Command and exit 0:
`evidence/differential.log`.

**Stage 2 result: PASS.**

## 3. Clean proof reconstruction

All source inputs were copied to `/tmp/audit-work/74-total-match`. Trusted
semantics, not candidate caches, supplied the semantics copy. No
candidate-built definition or cache was copied or used. The observed
toolchain is K v7.1.293 (`evidence/toolchain.log`).

### Concrete definition and execution

Fresh command:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

This exited 0 (`evidence/runtime-build.log`). A freshly translated program
containing all five prompt assertions then ran with:

```text
krun regenerated-concrete-tests.mpy \
  --definition runtime-kompiled \
  --output none
```

It exited 0 (`evidence/concrete-krun.log`).

### Proof definition and all positive claims

Fresh command:

```text
kompile verification.k \
  --backend haskell \
  --main-module TOTAL-MATCH-VERIFICATION \
  --syntax-module TOTAL-MATCH-VERIFICATION \
  --output-definition verification-kompiled
```

This exited 0 (`evidence/verification-build.log`). The positive proof results
were:

| Claim | Command abbreviation | Result |
|---|---|---|
| loop invariant | `kprove spec.k ... --spec-module TOTAL-MATCH-LOOP-SPEC` | exit 0, `#Top` |
| both entry claims as submitted | `kprove spec.k ... --spec-module TOTAL-MATCH-SPEC` | exit 0, `#Top` |
| left entry in an isolated exact copy | `kprove spec-entry-left.k ... --spec-module TOTAL-MATCH-ENTRY-LEFT-SPEC` | exit 0, `#Top` |
| right entry in an isolated exact copy | `kprove spec-entry-right.k ... --spec-module TOTAL-MATCH-ENTRY-RIGHT-SPEC` | exit 0, `#Top` |

The logs are `evidence/positive-loop.log`,
`evidence/positive-end-to-end-rerun.log`,
`evidence/positive-entry-left.log`, and
`evidence/positive-entry-right.log`. The isolated specs are preserved under
`evidence/artifacts/`.

`evidence/positive-end-to-end.log` records a concurrent first invocation that
failed before claim parsing because K's launcher transiently detected no Java
version (exit 2). It is retained, was not interpreted as a proof result, and
the immediate isolated rerun above succeeded.

**Stage 3 result: PASS for proof reconstruction.** This establishes closure
under the submitted extended theory, not the soundness of that theory.

## 4. Adequacy and real-program pinning

### Claims in plain language

The loop claim has no explicit side condition beyond its sorted variables. For
any finite `StrSeq ITEMS`, integer accumulator `I`, and old loop-variable value
`OLD`, it claims that the supplied `#loop` executing
`acc += len(item)`, followed by the proof-only observer
`readAccAndDrop("acc","item")`, produces
`I + totalChars(ITEMS)`. Its destination updates `acc` to that result and
removes `item`.

The first entry claim says: for all finite sequences of strings `A` and `B`,
if `totalChars(A) <= totalChars(B)`, executing `runTotalMatch(A,B)` returns the
exact K list term constructed from `A`.

The second says: for the same domain, if `totalChars(A) >
totalChars(B)`, it returns the exact list term constructed from `B`.

The two guards are disjoint and exhaustive over K integers, including the
required first-list tie behavior. They are not finite-size or example
restrictions.

### Satisfying states and concrete substitutions

`evidence/claim_witnesses.py` and `evidence/claim-witnesses.log` provide:

- left/tie witness `A=[]`, `B=[]`, totals `(0,0)`, both Python
  implementations return the first object;
- nonempty tie witness `A=["ab"]`, `B=["c","d"]`, totals `(2,2)`, both
  return `A`;
- right witness `A=["ab"]`, `B=[""]`, totals `(2,0)`, both return `B`;
- loop witness `I=7`, `OLD=int(99)`, `ITEMS=["ab",""]`, whose claimed
  accumulator is `7 + 2 + 0 = 9`.

Thus every entry precondition is satisfiable and every claimed result has been
ground-substituted.

### Mechanical program identity

`evidence/program_term_check.py` extracts the translated
`FuncDef("total_match", Params("lst1","lst2"), BODY)` body and constructs the
corresponding direct `closureVal` call. After only whitespace normalization
and the declared empty-list spelling normalization (`.Stmts` versus an
omitted list unit), that exact call occurs once in `verification.k`.
`evidence/program-term-check.log` records exit 0 and occurrence count 1.

The helper bypasses module load, one `FuncDef` rewrite, and subsequent lookup,
but not the binding or body: under the fresh module configuration, the fixed
`FuncDef` rule binds precisely `closureVal(params, BODY, 0)`, which is the
value the helper calls. This is semantically inert constructor normalization,
not a substituted algorithm.

As an independent body-sensitivity check, I changed the first executable loop
inside that `closureVal` to add `0` while leaving the proof summaries and
right-branch theorem unchanged. The changed definition built successfully
(`evidence/body-mutation-build.log`, exit 0), and the right claim failed with
a meaningful implication residual (`evidence/body-mutation-proof.log`, exit
1). The mutated artifacts are preserved under `evidence/artifacts/`.

### Adequacy limit exposed for Stage 5

Although the helper contains the real body, the submitted proof theory does
not execute each loop through the fixed `For/#loop` rules in the entry proof.
The priority proof-local summary at `verification.k:86-108` preempts that
execution. Whether this is a sound acceleration is therefore decisive.

**Stage 4 result: PASS for domain, result constraint, and constructor-level
pinning; execution fidelity depends on the Stage 5 operational bridge.**

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_inventory.py` inventories every local source record in the
supplied `semantics.k` tree, `verification.k`, and `spec.k`.
`evidence/k-inventory.log` is the complete line-level inventory (exit 0):

- 26 K source files;
- 706 rules;
- 233 syntax declarations;
- 143 separately recorded `requires` guards;
- 47 priority-bearing records;
- 147 function-bearing declarations, 108 marked `total`;
- 36 concrete records, 26 `owise` records, 4 macro records;
- 22 `no-evaluators` opaque declarations;
- 5 contexts, 1 configuration, and all 3 claims;
- no `functional` declaration and no local `simplification` rule.

The supplied opaque symbols are `sortVS`, `sortKeyVS`,
`md5hexCodes`, and the float-only symbols `intFloatDiv`, `divII`,
`floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`,
`powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`,
`truncF`, `roundF`, `roundFN`, and `sqrtF`. None is reachable from
the submitted program or any proof-local rule used by its claims. They are
therefore inert here and cannot supply the result.

The fixed semantics rules used by this program map as follows:

| Program construct | Declaration and material fixed rules |
|---|---|
| `Module`, statement sequencing | `syntax.k:61`; `core.k:124-127` |
| `FuncDef`, parameters, frame creation | `syntax.k:53,57,60`; `functions.k:14-16,63-66`; `call.k:69-74` |
| `Name`, assignment, integer literal | `syntax.k:9-13,41`; `core.k:131-154,194`; `controls.k:9-23` |
| `For` and loop target binding | `syntax.k:45`; `controls.k:65-74`; `tuple.k:31-34` |
| list iteration | `iter.k:8`; `list.k:9-10` |
| `Call(Name("len"),...)` | `syntax.k:28`; `call.k:20-32`; `builtins.k:17-26`; `core.k:223-229` |
| integer `+` | `operators.k:12`; `int.k:9` |
| `Compare(...,"<=",...)` | `syntax.k:30,32`; `operators.k:15-17`; `int.k:23` |
| `If` | `syntax.k:49`; `controls.k:51-54` |
| `Return` and frame pop | `syntax.k:50`; `functions.k:78-90` |

These fixed rules preserve left-to-right strict evaluation, bind the loop
target before the body, evaluate `len` through ordinary lookup/call dispatch,
update the accumulator in the active scope, leave the last loop-target
binding, and pop the callee frame on return. The list/string representation
and `isLen`/`vsLen` definitions structurally count sequence elements. The
remaining inventoried supplied rules are for syntax unreachable from this
program; no such rule can match its execution path. No false conclusion
witness was found for a fixed rule on the used path.

### Proof-local inventory and decisions

| Lines in `verification.k` | Extension | Class and assessment |
|---|---|---|
| 9-15 | `StrSeq`, `strVals` | Sound structural input representation. The empty/cons equations are exhaustive and descending. |
| 17-20 | `totalChars` `[function,total]` | Sound definitional summary. Empty is 0; cons adds fixed-semantics `isLen`; guards do not overlap. |
| 25-38 | `nextStrings` and priority adapter | Operational adapter, but structurally faithful: empty produces `#iterDone`, cons produces the identical value/rest pair as fixed list iteration. It preserves all cells and continuation. |
| 42-74 | `readAccAndDrop` | Explicit proof-only observer. The two disjoint cases return the integer accumulator; the second removes the distinct item binding. It is sound as an observer in the theorem in which it appears, but its state erasure narrows that theorem's justification scope. |
| 86-108 | priority-40 `For` summary | **Materially unsound operational bridge.** It is broader than its cited theorem and makes false conclusions provable. |
| 112-138 | `runTotalMatch` | Exact program-pinning helper. Its RHS is the mechanically matched submitted closure and ordinary fixed-semantics call. |

There are no proof-local opaque symbols or simplification rules.

### Why the `For` bridge is not justified

The bridge matches:

```text
For(Name(ITEM), list(strVals(ITEMS)),
    AugAssign(Name(ACC), "+", Call(Name("len"), Name(ITEM))))
```

whenever the current `ACC` binding is an integer. It deletes the `For` term
and updates only `ACC` by `totalChars(ITEMS)`. Its complete footprint is:

- reads `<k>`, `<env>`, the active scope map, the old `ACC`, and `ITEMS`;
- writes `<k>` and the `ACC` binding;
- frames heap, allocation counters, stack, return/exception state, and every
  non-`ACC` binding;
- accepts any trailing continuation because of `<k> ... </k>`;
- does not require `ACC =/=String ITEM`;
- never performs the fixed loop-target binding, so it preserves an old
  `ITEM` or leaves it absent instead of binding the last element.

The loop claim at `spec.k:10-36` is not a bridge-free universal connection
theorem for this domain. It starts at `#loop`, not `For`; fixes literal names
`"acc"` and `"item"`; assumes both are initially bound; and proves only the
special suffix `readAccAndDrop`, which deliberately erases `item`. It proves
neither arbitrary continuations nor the alias case. Importing
`verification.k` also means it is not an independent theorem about every
configuration accepted by the bridge, although this particular claim does
not start with a `For` redex.

### False-conclusion witness 1: continuation/state mismatch

The preserved witness is
`evidence/artifacts/bridge-context-witness.k`. It uses an intended-domain
input list `["a"]`, distinct variables `acc` and `item`, initial
`acc = 0`, initial `item = "z"`, the exact summarized loop body, and an
immediate continuation `Name("item")`.

Fixed semantics binds `item = "a"`, increments `acc = 1`, and the continuation
returns `"a"`. The bridge instead skips target binding, leaves
`item = "z"`, and returns `"z"`.

With the bridge:

```text
kprove bridge-context-witness.k \
  --definition verification-kompiled \
  --spec-module BRIDGE-CONTEXT-WITNESS
```

prints `#Top` and exits 0
(`evidence/bridge-context-enabled.log`). With the single bridge removed from a
freshly built definition, the otherwise identical claim exits 1 and the
residual explicitly contains `str(iCons(97,.IntSeq))` and
`item |-> str(iCons(97,.IntSeq))`, i.e. `"a"`, not the demanded old
`"z"` (`evidence/bridge-context-disabled.log`). The bridge-free definition
build is `evidence/no-loop-bridge-build.log` (exit 0), and its source is
preserved under `evidence/artifacts/`.

This is the required concrete false conclusion for the bridge's arbitrary
continuation and omitted state effect.

### False-conclusion witness 2: missing non-alias guard

The preserved witness is
`evidence/artifacts/bridge-alias-witness.k`. It uses the intended-domain list
`["a"]` but sets `ACC == ITEM == "x"`. The bridge guard is satisfied because
`x` is initially integer 0, so the bridge fabricates final `x = 1` and proves
the claim (`evidence/bridge-alias-enabled.log`: exit 0, `#Top`).

Fixed semantics first binds loop target `x = "a"`, then evaluates
`x += len(x)`, leaving the unsupported term
`applyBin("+", str(iCons(97,.IntSeq)), 1)`. The identical bridge-free claim
exits 1 with that exact residual and the failed equality to 1
(`evidence/bridge-alias-disabled.log`).

This is a second concrete false conclusion enabled by the same unsound rule.
It demonstrates that the rule is not merely over-broad-but-sound on its
declared match domain.

The actual candidate happens to use distinct local names and does not observe
`item` after either loop. That makes its Python result correct, but it does
not turn this globally false rule into a valid theorem or supply the missing
complete-domain connection proof. The target entry claims execute both loops
through this priority rule, so the unsound extension contributes directly to
their closure.

**Stage 5 result: FAIL.** Gate A real-program soundness fails.

## 6. Fresh non-vacuity test

I created a new mutation, preserved as
`evidence/artifacts/spec-vacuity.k`. It retains the satisfiable
`totalChars(A) <= totalChars(B)` guard but changes the required result from
`A` to `B`. The concrete witness `A=[]`, `B=["a"]` satisfies `0 <= 1`; both
Python programs return `[]`, not `["a"]`.

First:

```text
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run --output none
```

compiled the mutation to KORE and exited 0
(`evidence/vacuity-build.log`). Then the same command without `--dry-run`
exited 1 with `WarnStuckClaimState`; the residual shows the reached
`list(strVals(A))` and unmet `A == B` implication
(`evidence/vacuity-proof.log`). This is a reachable result obligation, not a
parse error, missing import, timeout, or unrelated crash.

**Stage 6 result: PASS.** The entry claim is result-constraining and
non-vacuous. This does not repair the unsound execution rule.

## 7. Proven-versus-assumed accounting

### What the successful K runs establish

Under the submitted extended rewrite theory, the successful runs establish:

1. For every `StrSeq ITEMS`, integer `I`, and `Val OLD`, the submitted
   `#loop` claim composed with `readAccAndDrop` reaches
   `I + totalChars(ITEMS)` and the stated scope update.
2. For every `StrSeq A,B` satisfying `totalChars(A) <= totalChars(B)`,
   `runTotalMatch(A,B)` reaches `list(strVals(A))`.
3. For every `StrSeq A,B` satisfying `totalChars(A) > totalChars(B)`,
   it reaches `list(strVals(B))`.

The false mutation confirms items 2 and 3 are discriminating statements.
They are nevertheless conditional on every imported rewrite rule, including
the false `For` rule. Because that rule can prove both documented false
conclusions above and is used by the entry executions, the conditional
theorems are not a sound partial-correctness proof of the real program.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Trusted supplied MPY semantics | Defines all execution, control, cells, and values | Acceptable selected semantics boundary. Candidate copy is exact. Material rules were reviewed; partiality outside the used subset is irrelevant here. |
| K integer/Boolean/map/list builtins | Arithmetic, comparisons, sequence/map operations | Ordinary low-level trusted mathematical/runtime primitives; acceptable. |
| `StrSeq`/`IntSeq` to Python `list[str]` interpretation | Input-domain and character length bridge | Formal representation is at least as broad as finite Python lists of strings; `isLen` counts code-sequence elements. Mechanical translation and finite Unicode differential tests support, but do not universally prove, the Python/K interpretation bridge. No domain narrowing results. |
| `strVals`, `totalChars`, `nextStrings` | Input construction, result-bearing length summary, symbolic iterator | Exhaustive descending definitions/adapter; acceptable. No unconstrained oracle. |
| `readAccAndDrop` | Auxiliary claim result and item-state erasure | Acceptable only as an explicit observer in that exact auxiliary theorem. It cannot justify the broader `For` bridge. |
| `runTotalMatch` | Selects the executed program body | Acceptable exact constructor pin, mechanically checked and body-sensitive. |
| supplied float/sort/MD5 opaque symbols | Potential value or control only if invoked | Unreachable and non-dependent; inert for all three claims. |
| proof-local priority `For` rule | Replaces both material loops, controls accumulators and therefore branch/result | **Illegitimate.** No complete-domain bridge-free connection theorem; false on two satisfying intended-data witnesses; directly used by target claims. |
| Python differential suite | Candidate/canonical result and identity on 34,355 cases | Strong finite evidence only. It cannot validate the K operational bridge or replace a universal connection theorem. |
| LLVM example run | Five concrete submitted examples | Finite execution smoke evidence only. |

### Gate accounting and decision

- Gate A — real-program soundness: **FAIL** because an imported,
  result-contributing operational bridge makes false conclusions provable.
- Gate B — intent adequacy: the claim domain and two postconditions do cover
  the unrestricted finite list-of-strings contract and the tie rule; no
  material narrowing was found.
- Gate C — evidence auditability: fresh commands, source mutations, witnesses,
  bounded logs, and scripts are preserved. This cannot cure Gate A.

The correct implementation, clean `#Top` reconstruction, real-body pinning,
and successful non-vacuity probe are all genuine but insufficient. The
decision boundary requires failure when a target proof relies on materially
unsound proof rules.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
