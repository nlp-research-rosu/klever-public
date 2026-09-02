# Independent adversarial review: 1-separate-paren-groups

## Outcome

The candidate contains a legitimate, non-vacuous partial-correctness proof under
the supplied MPY semantics. A clean Haskell rebuild and proof run closes both
submitted claims with `#Top`; the closure in the entry claim contains the exact
translated function body; the loop claim executes the fixed semantics rather
than replacing the loop with an operational shortcut; and the final heap value
is constrained by terminating, exhaustive equations.

The verdict is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, for two
adequacy limitations:

1. The theorem equates execution with `scanParenGroups`, a faithful recursive
   execution summary. The further assertion that this summary is exactly the
   English notion of the top-level balanced-group partition is justified by
   inspection and finite differential evidence, not by a second formal theorem.
2. The entry claim starts after module loading, with
   `separate_paren_groups` already bound to the exact submitted closure. The
   omitted `typing.List` import and `FuncDef` installation are simple under the
   supplied semantics and the selected binding is pinned, so this is not a
   substitution or soundness failure, but the `<k>` cell does not literally
   start from the submitted `Module(...)` term.

Neither limitation lets a false result be proved on the claimed domain.

## 1. Input and provenance integrity

### Launcher record and mode

`/audit-input.json` declares:

- `record_layout = "pipeline-v3"`;
- `semantics_mode = "SUPPLIED_SEMANTICS"`;
- problem `1-separate-paren-groups`;
- container mounts rooted at `/candidate`, `/reference`, and `/generation`.

The declared mode and mounts are consistent: the trusted
`/reference/reference-semantics` tree is present. There is no infrastructure
breach.

All pipeline-v3 records required by the audit instructions are present and
readable regular files or directories:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation/invocation.json`, `metrics.json`, `runtime-metrics.json`,
  `usage.json`, `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- one 362-line JSONL trace below `/generation/codex-trace`.

Every JSON document and every JSONL event parsed successfully. The generation
log is valid UTF-8, has 34,052 lines and no NUL bytes. These records were treated
only as historical claims. The structured inspection is in
[`stage1-structured-generation.log`](evidence/stage1-structured-generation.log);
the record contents, path types, and mounted tree listings are in
[`stage1-records.log`](evidence/stage1-records.log).

### Independent hashes and source integrity

Independent `sha256sum` results agree with the launcher-recorded hashes for all
single-file provenance records, including:

| Mounted input | Independent SHA-256 |
|---|---|
| `/run.json` | `3b99df09203880c9a59a6dcfed87c41b60e6057ebf8720421e156f1e7517bd73` |
| `/task.json` | `c09efc9b5d768c0b312eb9025eb80abe55c3a8cfcec00c555f5bf9fe3fa7e23e` |
| `/generation-result.json` | `871b18670f98b4220ad90436e9730a874379998bb022aef88e4bdbdc498a8eab` |
| `/generation/invocation.json` | `d05f569d6ae160e3c479a9597f7da2cd218c78d592d412bd4e870e6232b94ec0` |
| `/generation/codex-output.log` | `0d50ff61420b5bce2806a07a220797e12d1b7fdc78243c596e741b5ce3258a32` |
| trace JSONL | `7519ed38f77736960dae4961c14233d6fef280efebc39952ed5daa718b9e4acb` |
| `/reference/canonical.py` | `b74f3a3f40b1416f878efb45645d27f822b9d06b04bcd6191329a2229357b82d` |

Stable per-file manifests independently hash every mounted regular file:
[`candidate-files.sha256`](evidence/candidate-files.sha256),
[`reference-files.sha256`](evidence/reference-files.sha256), and
[`generation-files.sha256`](evidence/generation-files.sha256). The exact
commands and aggregate manifest hashes are in
[`stage1-independent-tree-hashes.log`](evidence/stage1-independent-tree-hashes.log).

No symlink or other mistyped non-file/non-directory entry exists anywhere in
the candidate, reference, or generation trees. Recursive
`diff -r --no-dereference` between the candidate and trusted supplied-semantics
trees exits 0. The candidate prompt and translator are byte-identical to their
trusted copies:

- prompt SHA-256:
  `ba4d0641a184fb3cdd632060a25d6408a7e91fe9d79b5c341407e74b80536327`;
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The recursive comparison, path checks, and individual hashes are recorded in
[`stage1-integrity.log`](evidence/stage1-integrity.log). Thus no candidate
change, addition, deletion, type change, or symlink exists in the supplied
semantics. This integrity result does not bless `verification.k`; that file is
audited independently below.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks for a function that takes a string containing separate
balanced groups of nested parentheses, ignores spaces, and returns the
top-level groups as space-free strings. On the intended domain, every
non-space character is `(` or `)`, no prefix closes below depth zero, and final
depth is zero.

The trusted canonical implementation accumulates parentheses in a list,
increments/decrements depth, emits a group when depth returns to zero, ignores
everything other than parentheses, and returns the emitted groups.

The submitted `solution.py` uses the same depth-and-accumulator algorithm with
strings. For each non-space character it appends the character, increments on
`(` and decrements otherwise, then emits on depth zero. This is equivalent to
the canonical implementation on the intended parentheses-and-spaces domain.
It is not equivalent for arbitrary text: for example, the independent
diagnostics report different results for `")("`, `"(a)"`, and `"()x()"`.
Those inputs are excluded by both the English domain and
`validParenInput`; the difference is therefore an explicit scope limitation,
not a counterexample to the claim.

### Translation identity

In fresh scratch space, the trusted command

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

exits 0. `cmp` exits 0 and both submitted and regenerated files have SHA-256
`1d8ba86f3eaad4413c7c38e0f6630c8cdb532d378f30bf9ebe34f755ae6e22a9`.
See [`stage2-translation.log`](evidence/stage2-translation.log). Therefore the
submitted `solution.mpy` is exactly the trusted translation of `solution.py`.

### Independent differential test

[`differential_test.py`](evidence/differential_test.py) independently imports
the trusted canonical entry point and the generated entry point. It checks:

- the documented example;
- empty and spaces-only inputs;
- a one-group boundary, adjacent groups, separated groups, nesting, and deep
  nesting;
- all valid strings over the alphabet `" ()"` of lengths 0 through 9;
- 500 deterministic larger generated cases with multiple balanced groups and
  varied spaces.

It tests 1,803 distinct valid inputs and reports zero mismatches, exit 0. The
complete bounded result is
[`stage2-differential.log`](evidence/stage2-differential.log). This is finite
evidence about the implementation-to-contract bridge, not a replacement for
the K proof.

## 3. Clean proof reconstruction

### Scratch isolation and toolchain

Only source artifacts were copied to
`/tmp/audit-work/paren-audit`: the candidate solution/specification sources,
the trusted translator, and the trusted supplied semantics. Candidate-provided
`runtime-kompiled`, `verification-kompiled`, caches, and logs were not copied or
used. Both definitions were produced from source in scratch.

The independently available tools report K version `v7.1.293`; see
[`stage3-toolchain.log`](evidence/stage3-toolchain.log).

### Fresh builds

The LLVM concrete definition was built with:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exits 0. The warnings concern unused variables and non-exhaustive
`[total]` functions in unrelated supplied modules; none of the warned
functions is reachable from this program. Full bounded output:
[`stage3-kompile-llvm.log`](evidence/stage3-kompile-llvm.log).

The Haskell proof definition was built with:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exits 0; see
[`stage3-kompile-haskell.log`](evidence/stage3-kompile-haskell.log).

### Positive claims

The required clean proof command is:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

It proves both positive claims together, prints exactly `#Top`, and exits 0.
See [`stage3-kprove-all.log`](evidence/stage3-kprove-all.log).

The loop claim was additionally selected and run independently with
`--claims SPEC.loop-invariant`; it also prints `#Top` and exits 0:
[`stage3-kprove-loop-claim.log`](evidence/stage3-kprove-loop-claim.log).
Selecting only `SPEC.function-correct` removes the loop claim that serves as
its proved circularity, so that filtering experiment is not the target proof
and was manually stopped after it continued unrolling. The valid target run is
the combined proof, in which both the helper claim and dependent entry claim
are obligations and the conjunction closes.

### Concrete execution

[`reviewer-concrete.py`](evidence/reviewer-concrete.py) contains the exact
submitted function body followed by independent assertions for empty,
spaces-only, one-group, documented, adjacent, and nested cases. It was
translated with the trusted translator and executed using the fresh LLVM
definition. Python exits 0; `krun` reaches `.K`, `NoExc`, and exit code 0.
See [`stage3-concrete-krun.log`](evidence/stage3-concrete-krun.log).

## 4. Adequacy and real-program pinning

### Plain-language meaning of the claims

`SPEC.loop-invariant` says:

> Starting at the supplied semantics' real `#loop` head with remaining string
> `S`, depth `D`, current string `CUR`, and emitted list `OUT`, executing the
> exact submitted loop body consumes the loop and changes the group heap object
> to `scanParenGroups(S,D,CUR,OUT)`. It preserves environment location,
> allocation counters, stack, normal return/exception state, and exit code.
> Final `current`, `depth`, and `char` are existential because the function
> returns only `groups`.

`SPEC.function-correct` says:

> If scope 0 binds `separate_paren_groups` to the exact submitted closure and
> `S` satisfies `validParenInput`, executing a direct call returns heap
> reference 0. Heap location 0 contains
> `separateParenGroupsSpec(S)`, allocation advances from 0 to 1, the callee
> frame is popped, and execution completes normally with an empty stack.

### Program identity and control flow

The closure body in `spec.k` is syntactically the same AST as
`solution.mpy`, in the same order:

1. allocate `groups = []`;
2. initialize `current`, `depth`, and `char`;
3. iterate `paren_string`;
4. test space, concatenate, test `(`, update depth, test depth zero, append and
   clear;
5. return `groups`.

No helper replaces `Call`, `For`, `#loop`, `append`, or `Return` in
`verification.k`. The fixed supplied rules perform lookup, left-to-right call
evaluation, parameter binding, list allocation, string iteration, target
binding, conditional evaluation, mutation, return, frame pop, and heap escape.
The loop claim begins exactly at the recurring fixed-semantics `#loop` control
point and is itself proved as a reachability claim.

The selected binding is fixed to the exact closure, so an alternate function
cannot satisfy the entry state. The only omitted real-program prefix is loading
the module: under the supplied rules, the `typing.List` import is a no-op and
the exact `FuncDef` installs this closure in scope 0. That static connection is
straightforward but not an explicit auxiliary reachability claim, and is one
reason for the `CONCERNS` verdict.

### Result constraint and satisfiable state

The result is not a free variable or a one-way implication. The returned
`ref(0)` is linked to an explicitly updated heap cell, and that heap cell is
exactly `list(separateParenGroupsSpec(S))`. The summary has exhaustive
constructor equations and therefore cannot be assigned an arbitrary
interpretation.

The entry precondition is satisfiable. For example:

```text
S = iCons(40, iCons(41, .IntSeq))   // "()"
```

reduces through `validParenInput` to true. The fresh ground claim
[`spec-ground-witness.k`](evidence/spec-ground-witness.k) substitutes this
input and replaces the symbolic result by the explicit MPY list `["()"]`. It
prints `#Top` and exits 0. In the same recorded command, both trusted canonical
Python and generated Python return `['()']`. See
[`stage4-ground-witness.log`](evidence/stage4-ground-witness.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`rule-inventory.md`](evidence/rule-inventory.md), generated by the preserved
reviewer script [`rule_inventory.py`](evidence/rule_inventory.py), lists every
top-level source declaration with file, line, attributes, audit disposition,
and compact full text. Its totals are:

| Kind | Count |
|---|---:|
| source `requires` | 25 |
| modules | 27 |
| imports | 88 |
| syntax declarations | 230 |
| configurations | 1 |
| contexts | 5 |
| rules | 705 |
| claims | 2 |

This includes all supplied helper K files, `semantics.k`,
`verification.k`, and `spec.k`. The full source inspections are preserved in
the `stage5-*-semantics.log` files, and declaration/attribute searches are in
[`stage5-declaration-counts.log`](evidence/stage5-declaration-counts.log).
There are no candidate-generated semantics files in this
`SUPPLIED_SEMANTICS` run.

For each supplied rule, the inventory records `ACCEPT FOR TARGET` after
checking whether it is source-faithful on the reachable path or inert for this
entry claim. This is a target-relative soundness decision, not a claim that
the intentionally minimal MPY semantics models every possible CPython
program. Unused rules cannot match a reachable term of this program because
their constructors, operator strings, callable names, or value sorts do not
occur. No unused rule provides a generic rewrite of this program's result.

### Proof-local declarations and rules

`verification.k` has four function symbols in three syntax declarations, all
marked `[function, total]`, and ten equations. It has no ordinary `<k>`
rewrite, priority rule, simplification rule, `functional` declaration, opaque
symbol, or oracle.

1. `scanParenGroups` base equation returns `OUT` on `.IntSeq`. This is exactly
   the source loop's empty-iterator behavior.
2. Its `iCons` equation first handles code 32 as a no-op. Otherwise it appends
   the character to `CUR`, adds one to depth for code 40 and subtracts one for
   every other code, and emits/resets exactly when the new depth is zero. This
   mirrors the source for every `IntSeq`, including the source's broad
   non-`(` branch. It recurses on strict tail `REST`.
3. `separateParenGroupsSpec(S)` initializes the scanner with zero depth and
   empty current/output accumulators.
4. `validParenInput(S)` starts `validParenSuffix(S,0)`.
5. The six `validParenSuffix` equations cover empty, space, open, close at
   positive depth, close at non-positive depth, and every other character.

Coverage and overlaps are sound:

- `.IntSeq` and `iCons` are disjoint; the scan's nested K conditionals are
  total.
- The close-parenthesis guards `D > 0` and `D <= 0` are disjoint and
  exhaustive.
- The other-character guard excludes exactly codes 32, 40, and 41.
- Every recursive equation consumes one `IntSeq` constructor, so totality is
  justified and terminating.

These equations encode neither a task answer table nor a skipped program
operation. `scanParenGroups` is result-bearing, but its value is fixed by
truthful exhaustive equations and independently connected to execution by the
universal loop claim. There is no circular use of an unconstrained symbol.

### Used syntax-to-rule map

| Submitted construct | Supplied declaration/rules and reviewed behavior |
|---|---|
| `Call`, `Name`, closure | `core.k`, `call.k`, `functions.k`: lexical lookup, callee then argument evaluation, fresh frame, parameter bind, exact body, return and pop |
| `ListExpr`, `groups.append` | `list.k`, `core.k`, `call.k`: fresh heap allocation at location 0 and in-place append at the selected reference |
| `Str`, string iteration and `+` | `str.k`: ASCII literal conversion, one-character iteration, structural concatenation |
| `Int`, `+`, `-`, `==` | `int.k` and `operators.k`: ordinary unbounded integer arithmetic and comparison |
| `Assign`, `AugAssign`, `If` | `controls.k`: RHS strictness, current-scope writes, boolean branch through `truthy` |
| `For` | `controls.k`, `iter.k`, `str.k`, `tuple.k`: evaluate iterable once, `#loop/#loopStep`, bind `char`, execute body, recur through `#loopLbl` |
| expression statement | `controls.k`: evaluate append call for effect and discard `noneV` |
| `Return` | `functions.k`: set return state, restore caller, delete callee scope, preserve escaping heap object |

Evaluation order is left-to-right where observable: call evaluation uses
`#evalArgs`; `BinOp` is sequentially strict; `Assign`, `AugAssign`, `If`, and
`For` use the declared strict positions. The loop input is evaluated once.
There is no exceptional or abrupt construct in the body. With the claim's
typed values, all used operations are defined, so `NoExc` and exit code 0 are
preserved.

State and allocation are fully accounted for. `groups` receives `ref(0)`;
heap location 0 is a list; append mutates that exact location; strings and
integers remain values in the callee scope; `char` is rebound for each yielded
one-character string; and frame pop removes only the callee scope, not the
returned heap allocation. The loop claim frames all unrelated scope/heap
entries and preserves allocation counters and stack.

Relevant priorities are benign and necessary: the list `append` rule at
priority 40 preempts generic bound-method handling for a mutating reference;
reference dereference rules preempt generic value dispatch only on matching
heap references. `verification.k` adds no priority. The generic call rule is
`[owise]`, but no proof-local call interception exists.

### Imported but unreachable boundaries

The supplied semantics contains explicit opaque/trusted primitives for float
operations, sorting, and MD5, including `sortVS`, `sortKeyVS`,
`md5hexCodes`, and the `no-evaluators` float family. It also contains minimal
rules for dictionaries, slicing, comprehensions, ranges, sets, tuples, and
many builtins. None is reachable from this entry claim: the program uses only
strings, integers, one heap list, ordinary control, and `append`. No opaque
term can influence a branch, heap value, exception, or postcondition here.

Compiler exhaustiveness warnings for `mapStrVS`, `floorFI`, `toF`, `ceilF`,
`joinCodes`, and out-of-bounds `valSeqAt` likewise concern unreachable
operations. They are recorded as narrower supplied-language coverage gaps,
not mislabeled as task-rule unsoundness.

No rule was classified as materially unsound for this target. Consequently
there is no purported unsound rule for which a false-conclusion witness is
owed. The observed Python divergences on invalid text are domain exclusions,
not conclusions enabled under `validParenInput`.

## 6. Fresh non-vacuity test

The candidate's own `spec-vacuity.k` was not reused. The reviewer-authored
[`spec-fresh-mutation.k`](evidence/spec-fresh-mutation.k) uses the satisfiable
valid input `"()"`, executes the exact closure body, but changes the required
single output string from `"()"` to `"(())"`.

Command:

```text
kprove spec-fresh-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-FRESH-MUTATION
```

The mutation parses and builds, executes to the actual terminal state, prints
`WarnStuckClaimState`, and exits 1. Its residual heap is:

```text
0 |-> list(vCons(str(iCons(40, iCons(41, .IntSeq))), .ValSeq))
```

That is the actual `["()"]` result, which does not unify with the mutated
`["(())"]` destination. This is the expected unmet result obligation, not a
parser error, missing import, timeout, or unrelated crash. Full output:
[`stage6-fresh-mutation.log`](evidence/stage6-fresh-mutation.log).

## 7. Proven versus assumed accounting

### Formally established

Conditional on the K toolchain and supplied semantics, the successful
reachability proof establishes:

- for every finite `IntSeq S` satisfying `validParenInput(S)`;
- from the exact entry configuration in `SPEC.function-correct`, including the
  exact closure binding and normal initial control/state cells;
- if the call terminates, it returns `ref(0)`;
- heap location 0 contains
  `list(scanParenGroups(S,0,.IntSeq,.ValSeq))`;
- stack, return, exception, and exit cells end in the specified normal state;
- the loop summary is universally connected to fixed-semantics execution for
  all string tails, integer depths, current strings, and output sequences
  matching the loop claim.

The proof does not rely on a candidate compiled definition, prior `#Top`,
candidate trace, candidate report, or differential test.

### Trust and limitation ledger

| Boundary | Influence | Assessment and evidence |
|---|---|---|
| K v7.1.293 compiler, Haskell backend, and reachability logic | All formal closure results | Necessary low-level proof-checker trust; fresh source rebuild and reruns succeeded |
| Supplied MPY semantics | Evaluation, control, scopes, heap, calls, and return | Authorized fixed semantics; candidate tree is recursively identical to trusted tree; used rules were statically reviewed and concretely exercised |
| Trusted `py2mpy.py` | Connection from `solution.py` to `solution.mpy` | Translator implementation is not formally verified, but trusted input regenerates the submitted MPY byte-for-byte |
| Entry-state module-load bridge | Connection from submitted `Module` to preinstalled exact closure | Informal/static: supplied import rule ignores `typing.List`, and `FuncDef` installs the displayed exact closure; not an explicit candidate claim |
| `scanParenGroups` to English top-level-group meaning | Natural-language adequacy | Equations visibly implement depth partitioning and space erasure, and 1,803 independent canonical comparisons agree; no separate universal K theorem states balancedness/partition properties |
| Trusted canonical Python | Differential oracle | Trusted input and independent of proof equations; finite tests support, but do not prove, the universal intent bridge |
| ASCII/unbounded-int MPY model | Character and depth representation | Adequate for codes 32, 40, and 41 and arbitrary nesting depth; Unicode and resource limits are outside the theorem |
| Imported opaque float/sort/digest symbols | None for this claim | Unreachable by syntax, value sorts, and callable names; no dependent claim |

### Gate assessment

- Real-program soundness: **pass**. The exact body executes; no operational
  bridge or unconstrained result-bearing abstraction exists; state/control are
  preserved; a satisfying witness exists; and the fresh false result is
  rejected.
- Intent adequacy: **limited but legitimate**. The formal domain matches the
  prompt's balanced parentheses and ASCII spaces, but the recursive
  summary-to-English partition theorem and module-load prefix remain informal.
- Evidence auditability: **pass**. Reviewer-authored scripts, exact commands,
  exit statuses, bounded outputs, ground witness, fresh mutation, source
  inventory, and independent hashes are preserved below `evidence/`.

The limitations warrant `CONCERNS`, not `FAIL`: the proof is sound,
result-constraining, and pinned to the exact generated function, and no
intended-domain witness makes any contributing rule yield a false conclusion.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
