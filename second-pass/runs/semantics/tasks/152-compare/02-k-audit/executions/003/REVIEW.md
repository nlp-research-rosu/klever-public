# Adversarial audit: 152-compare

The submitted Python implementation is correct on the tested contract, its
translation is authentic, and every declared positive proof command rebuilds
and prints `#Top`. The candidate nevertheless does **not** contain a legitimate
proof of the real program. Its universal proof depends on a priority-40
operational bridge that erases the entire loop while accepting an arbitrary
continuation and failing to reproduce the loop's `score` and `prediction`
bindings. A fresh machine-checked witness proves a false result with that
bridge, while the trusted fixed semantics rejects the same result and proves
the correct one.

All candidate artifacts, generation records, and prior outputs were treated
only as untrusted evidence. Builds and experiments used the scratch copy under
`/tmp/audit-work/152-compare`; reviewer-authored artifacts and bounded logs are
under `/audit-output/evidence/`.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `152-compare`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`.

This is mode-consistent: `/reference/reference-semantics` exists. The required
legacy-selected-stage1 records were read:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- the present optional `/generation-evidence/usage.json`;
- the one structured trace JSONL below
  `/generation-evidence/codex-trace/`.

Historical `runtime-metrics.json` is absent, which is permitted for this legacy
layout and was not reconstructed. The structured trace contains 262
JSON-decodable records and 45 recorded function calls. Its sole file hash,
`42988acfc746840ea8613564b81975c893e25f93c59835279fa422883f2876a6`,
matches `/generation-result.json`.

The campaign object in `/audit-input.json` exactly equals
`/audit-campaign-lock.json`. The independently computed lock hash is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the launcher record. All directly checkable recorded file hashes
match, including the run/task/result/invocation records, prompt, translator,
canonical solution, usage, generation output, and generation final response.
The independent hash of `/audit-input.json` itself is
`bed4fbde36a832c9dbe4b3a7c359fdc8cb100cb161d3b0a586976ae0fe2dde86`.

The candidate prompt and translator are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. A recursive path/type/content
comparison of `/candidate/reference-semantics` with the trusted supplied tree
found zero differences: no missing, additional, changed, mistyped, or symlinked
entry. No candidate-tree symlink was found. The complete independently hashed
candidate manifest and parsed trace summary are in
`evidence/01_integrity.log`.

Command:

```sh
python3 /audit-output/evidence/01_integrity.py
```

Exit 0; final result: `stage1_integrity_ok=True`. There is no audit
infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires two equal-length arrays of match scores and guesses
and returns an equally long array. Position `i` is `0` for an exact guess and
otherwise the absolute difference, equivalently
`abs(game[i] - guess[i])`. The trusted canonical implementation is the list
comprehension over `zip(game, guess)`.

`/candidate/solution.py` uses a result list, iterates over `zip(game, guess)`,
appends `abs(score - prediction)`, and returns the list. It is a faithful
alternative implementation. Its use of `zip` also truncates unequal lists,
which is outside the stated equal-length precondition and does not weaken the
intended result.

The trusted translator was run in scratch:

```sh
python3 /tmp/audit-work/152-compare/trusted/py2mpy.py \
  /tmp/audit-work/152-compare/candidate/solution.py \
  > /tmp/audit-work/152-compare/candidate/solution.fresh.mpy
cmp /tmp/audit-work/152-compare/candidate/solution.fresh.mpy \
  /tmp/audit-work/152-compare/candidate/solution.mpy
```

Exit 0. Both files have SHA-256
`4b4ee08ff7597115a3cc37699d5bdf9e27497cdaee3314a7d8c4f07f5ced704a`
(`evidence/02_translation.log`).

The independent differential program `evidence/02_differential.py` imports the
trusted canonical and generated entry points separately. It covers both prompt
examples, empty input, zero/positive/negative subtraction branches, negative
operands, arbitrary-precision integers, every pair of length-0-through-4 lists
over `{-5,-1,0,1,5}`, 2,000 deterministic random equal-length pairs of lengths
0 through 40, and four unequal-length diagnostics.

```sh
python3 /audit-output/evidence/02_differential.py
```

Exit 0: 408,913 cases, zero mismatches
(`evidence/02_differential.log`). This is finite evidence of implementation
fidelity, not a universal proof.

The source text is untyped, while the K theorem explicitly ranges over integer
sequences. The examples and benchmark behavior are integer-score cases, so I do
not use possible float generality as the decisive defect. If “scores” were
interpreted as arbitrary Python numeric objects, that would be an additional
domain restriction. The operational-bridge unsoundness below independently
requires failure.

## 3. Clean proof reconstruction

No candidate-compiled definition or cache was copied. The supplied semantics
was copied from the trusted mount, and all definitions were built afresh with K
7.1.293.

Concrete definition and run:

```sh
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

python3 /tmp/audit-work/152-compare/trusted/py2mpy.py \
  /audit-output/evidence/03_concrete_harness.py \
  > /tmp/audit-work/152-compare/candidate/03_concrete_harness.mpy
krun /tmp/audit-work/152-compare/candidate/03_concrete_harness.mpy \
  --definition audit-runtime-kompiled
```

Both exited 0. The K harness exercises both examples, empty input, each
subtraction-sign boundary, and negative operands. Its final configuration has
`.K`, `NoExc`, and exit code 0 (`evidence/03_build_runtime.log` and
`evidence/03_concrete_run.log`).

Universal/bridge-enabled proof:

```sh
kompile verification.k \
  --backend haskell \
  --main-module COMPARE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled

kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module COMPARE-SPEC
```

Both exited 0; `kprove` printed `#Top`
(`evidence/03_build_verification.log`, `evidence/03_kprove_spec.log`).

Bridge-free finite proof:

```sh
kompile verification.k \
  --backend haskell \
  --main-module COMPARE-COMMON \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-operational-kompiled

kprove operational-spec.k \
  --definition audit-operational-kompiled \
  --spec-module COMPARE-OPERATIONAL-SPEC
```

Both exited 0; `kprove` printed `#Top`
(`evidence/03_build_operational.log`,
`evidence/03_kprove_operational.log`).

The LLVM build emitted non-exhaustiveness warnings for helpers belonging to
unused map/float/string/subscript features. The Haskell builds emitted only
unused-variable warnings in two string-comparison rules. None prevented a build
or matched the submitted program. These clean `#Top` results establish closure
under the compiled theory; Stage 5 shows that the bridge-enabled theory is
unsound.

## 4. Adequacy and real-program pinning

### Entry claims

The three claims in `/candidate/spec.k` share the standard initial state:
module scope 0 is empty with parent builtins scope -1, `scopeLoc=1`, the heap is
empty with `heapLoc=0`, the call stack is empty, and return/exception states are
`noRet`/`NoExc`. They have no unsatisfiable side condition.

1. The universal claim defines `compare`, calls it with
   `list(intVals(GAME))` and `list(intVals(GUESS))` for arbitrary finite
   `IntSeq` values, and requires returned value `ref(0)`. It requires heap
   location 0 to contain
   `list(absDiffs(intVals(GAME), intVals(GUESS)))`, `heapLoc=1`, the exact
   global closure, an empty stack, and no exception.
2. The first example claim requires the exact first prompt output
   `[0,0,0,0,3,3]`.
3. The second example claim requires the exact second prompt output
   `[4,4,1,0,0,6]`.

The universal formal domain includes unequal lengths and gives zip truncation;
therefore it covers, rather than narrows, all equal-length integer-list cases.
The result is not free or tautological: both the returned ref and its exact heap
contents are constrained.

The four entry claims in `/candidate/operational-spec.k` import
`COMPARE-COMMON`, excluding the loop bridge. They prove the two examples,
empty/empty returning empty, and `[-7,9]` versus `[5,-4]` returning `[12,13]`.
They are meaningful finite execution claims, not an arbitrary-length theorem.
There is no helper or loop reachability claim connecting the fixed loop to
`absDiffs`.

### Mechanical program identity

Using the fresh proof definition, `kast --expand-macros` parsed both the trusted
fresh `solution.mpy` and the claim's `compareDef`. The reviewer script unwraps
the sole function statement from the translated `Module` and compares the KAST
JSON recursively:

```sh
kast solution.mpy --definition audit-verification-kompiled \
  --expand-macros --output json --output-file solution.kast.json
kast --expression 'compareDef' --sort Stmt --module COMPARE-COMMON \
  --definition audit-verification-kompiled --expand-macros \
  --output json --output-file compareDef.kast.json
python3 /audit-output/evidence/04_constructor_pinning.py
```

All exited 0; `constructor_terms_equal=True`
(`evidence/04_kast_expansion.log`,
`evidence/04_constructor_pinning.log`). Thus the claim executes the exact
submitted function binding and body, not a substituted program.

A concrete satisfying instance is `GAME=[1,-2,3]` and
`GUESS=[4,-2,-5]`. `absDiffs`, the trusted canonical, and generated Python all
give `[3,0,8]` (`evidence/04_ground_witness.log`).

Stage 4 therefore passes program identity, precondition satisfiability, and
result constraint. These facts do not validate a proof-local rule that replaces
the pinned body's execution.

## 5. Rule-by-rule static soundness review

The complete line-addressed inventory is
`evidence/05_inventory.log`; the per-file/per-extension decision ledger is
`evidence/05_rule_assessment.md`. It covers all 232 syntax declarations, 704
rule starts, the configuration, five contexts, imports, claims, attributes,
priority rules, functions, total declarations, macros, and opaque symbols in
the supplied tree plus candidate proof/spec files. There are no
`[functional]` or simplification declarations.

The actual source path is:

```text
Module/load → FuncDef/closure → Call/frame/parameter binding
→ docstring/Expr discard → empty ListExpr/allocation → Assign(result)
→ lookup/call zip → For/#loop → zip #iterNext
→ tuple target binding(score,prediction)
→ integer subtraction → builtin abs → bound append/heap update
→ loop recurrence → Return(result)/frame pop
```

The supplied rules preserve that evaluation order and all relevant cells.
They use mathematical K integers, zip truncation, and fresh heap allocation.
The 25 opaque or concrete-only symbols in the full supplied semantics are
`floorFI`, `toF`, `ceilF`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`,
`absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`,
`divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`,
`md5hexCodes`, `sortVS`, and `sortKeyVS`. None occurs on a target proof path.

Candidate-local extensions:

- `intVals` has disjoint empty/cons equations, justified totality, and
  structural descent.
- `absDiffs` has disjoint empty-left, empty-right, and both-nonempty equations;
  on every claim use it is a terminating definition of zip-truncated
  elementwise `absInt(A-B)`.
- `appendBody`, `compareBody`, and `compareDef` are exact syntax macros, as
  confirmed by the constructor comparison.
- `/candidate/verification.k:50-67` is a priority-40 operational bridge:

  ```k
  #loop(zipObj(GAME, GUESS), TupleExpr(...), appendBody) => .K ...
  ```

  It directly changes the result heap entry to
  `valSeqConcat(ACC, absDiffs(GAME, GUESS))`.

The last rule is materially unsound. It preempts fixed
`controls.k:71` execution and skips iterator steps, tuple assignments,
subtraction, builtin dispatch, append calls, and loop control. Its `...` in the
`<k>` cell admits every trailing continuation, but it neither writes
`score`/`prediction` nor restricts the continuation from observing them. Its
guard checks only that `result` maps to the updated heap reference. No
bridge-free universal connection theorem exists, and the finite claims in
`operational-spec.k` cannot supply one.

### Concrete false-conclusion witness

`evidence/05_bridge_context_spec.k` starts from the same one-pair integer loop:

- `GAME=[1]`, `GUESS=[2]`;
- `result` points to an empty list;
- the pre-loop bindings are `score=99`, `prediction=88`;
- immediately after the loop, the continuation evaluates `Name("score")`.

Fixed execution binds `score=1` and `prediction=2`, appends `1`, and produces
`1`. The bridge appends `1` but skips both bindings, so the continuation
produces stale `99`.

```sh
kprove 05_bridge_context_spec.k \
  --definition audit-verification-kompiled \
  --spec-module BRIDGE-CONTEXT-FALSE
```

Exit 0, `#Top`: the bridge-enabled theory proves the false `99` conclusion
(`evidence/05_bridge_false_proves.log`).

```sh
kprove 05_bridge_context_spec.k \
  --definition audit-operational-kompiled \
  --spec-module FIXED-CONTEXT-REJECT-FALSE
```

Exit 1 with `WarnStuckClaimState`. The residual explicitly contains `<k> 1`,
`score |-> 1`, `prediction |-> 2`, and result list `[1]`
(`evidence/05_fixed_false_rejected.log`).

```sh
kprove 05_bridge_context_spec.k \
  --definition audit-operational-kompiled \
  --spec-module FIXED-CONTEXT-CORRECT
```

Exit 0, `#Top` (`evidence/05_fixed_correct_proves.log`).

This is a satisfiable false-conclusion witness over integer lists inside the
bridge's complete declared match domain. It specifically demonstrates the
context/state mismatch rather than merely asserting a missing proof.

Finally, the universal claim was copied unchanged except for importing
`COMPARE-COMMON`, removing the bridge:

```sh
kprove 05_universal_without_bridge.k \
  --definition audit-operational-kompiled \
  --spec-module UNIVERSAL-WITHOUT-BRIDGE \
  --depth 100
```

Exit 1 with `WarnStuckClaimState` and two unexplored symbolic branches
(`evidence/05_universal_without_bridge_depth100.log`). This bounded diagnostic
does not show that the desired theorem is false; it confirms that the delivered
universal `#Top` depends on the rejected extension and that no legitimate
universal proof remains after its removal.

## 6. Fresh non-vacuity test

I did not rely on `/candidate/mutation-spec.k`. The fresh
`evidence/06_false_result_spec.k` executes the exact `compareDef` on satisfying
input `([1],[2])` but changes only the result-bearing heap postcondition from
the true `[1]` to false `[2]`.

The mutation first built successfully:

```sh
kprove 06_false_result_spec.k \
  --definition audit-verification-kompiled \
  --spec-module AUDITOR-FALSE-RESULT-SPEC \
  --dry-run
```

Exit 0 (`evidence/06_false_result_dry_run.log`).

The actual proof command was:

```sh
kprove 06_false_result_spec.k \
  --definition audit-verification-kompiled \
  --spec-module AUDITOR-FALSE-RESULT-SPEC
```

Exit 1 with `WarnStuckClaimState`. The residual is the expected normal return
`ref(0)` with heap location 0 containing `[1]`, directly exposing the unmet
`[2]` result obligation (`evidence/06_false_result_rejected.log`). This is a
valid non-vacuity result. It shows that the final claim constrains its answer;
it does not cure the independent operational-rule unsoundness.

## 7. Proven versus assumed accounting

### What the successful K runs establish

Under the **extended candidate theory**, the universal `#Top` establishes
partial correctness of the formal entry claim for arbitrary finite integer
sequences: the exact translated binding/body reaches a returned fresh list
whose symbolic contents are `absDiffs`, with the specified final scope, heap,
stack, return, and exception cells. The two examples close in that same theory.

Under the **fixed supplied theory without the bridge**, four concrete entry
claims close: the two examples, empty input, and one additional two-element
case. Those are legitimate finite reachability facts only.

Because the extended theory contains the demonstrated false transition, its
universal `#Top` proves closure under an unsound rewrite system, not the
requested theorem about fixed execution of the real program.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Trusted supplied semantics, byte-identical candidate copy | Defines all source execution, state, calls, and control | Accepted as the selected semantics boundary; relevant rules were also statically reviewed and concretely exercised. |
| K 7.1.293 compiler/prover and Haskell/LLVM backends | Builds and checks all K artifacts | Ordinary toolchain trust. Fresh builds avoid candidate binaries/caches. |
| K integer/Boolean/string/map/list hooks, especially `-Int` and `absInt` | Directly determines numeric results and state representation | Accepted low-level mathematical/runtime primitive boundary. |
| The 25 supplied opaque/concrete-only symbols listed in Stage 5 | Potentially affect floats, sorting, MD5, and conversions | Accepted but irrelevant here: none appears on a target path or in a postcondition. |
| `intVals` and `absDiffs` equations | Encode formal inputs and mathematical expected result | Equations themselves are truthful and terminating on every use. |
| Priority-40 candidate loop bridge | Determines universal loop result and control/state transition | Illegitimate. It is program-derived, lacks a bridge-free universal connection theorem, admits a broader continuation than any justification, and enables the concrete false conclusion in Stage 5. |
| Mechanical KAST comparison | Connects trusted translation to claim macro | Strong identity evidence; it does not establish semantic correctness of the bridge. |
| Python differential test | Connects generated Python behavior to trusted canonical behavior on 408,913 inputs | Finite empirical support only; not a K proof or a universal connection theorem. |
| LLVM concrete harness and bridge-free finite K claims | Exercise fixed execution on normal/boundary cases | Finite operational evidence only. |
| Informal observation that the submitted suffix returns only `result` | Suggests skipped loop-variable bindings are unobserved in this one body | Insufficient: the actual bridge rule accepts arbitrary suffixes and is globally false on its match domain. Priority does not narrow that domain. |

### Decision

Stages 1-4 reconstruct authentic inputs, a correct implementation, clean
positive `#Top` runs, a pinned program term, satisfiable preconditions, and a
result-constraining postcondition. Stage 6 confirms non-vacuity. Stage 5 is
fatal: the universal proof relies on a materially unsound operational bridge,
and a machine-checked witness shows the exact false conclusion it enables. The
bridge-free finite claims and differential tests cannot substitute for the
missing universal fixed-semantics connection proof.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
