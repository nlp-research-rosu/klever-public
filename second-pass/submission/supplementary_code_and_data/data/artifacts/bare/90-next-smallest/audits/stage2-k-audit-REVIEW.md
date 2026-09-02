# Independent adversarial review: 90-next-smallest

## Executive assessment

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted generated program over the full intended domain of finite lists
of mathematical integers. I rebuilt both definitions from source, reran the
only positive claim, obtained exit status 0 and `#Top`, mechanically matched the
claim's executed constructor tree to a trusted regeneration of `solution.mpy`,
and made both a body mutation and a false-result mutation fail for the expected
semantic reasons.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, because the
symbolic proof deliberately leaves the result-bearing `uniqueSort`, `lenInt`,
and `itemAt` functions opaque through `[concrete]` rules and uses the same
truthfully defined `uniqueSort` representation in the builtin-operation bridge
and the postcondition. Their connection to Python's `sorted(set(...))` and to
the natural-language “second distinct smallest” property is validated here by
a rule audit, ordinary induction, and finite concrete evidence, not by a
separate bridge-free K theorem. In addition, the generated `IfExp` model eagerly
evaluates both pure branches and totalizes an invalid subscript with
`invalidIndex`; this is result-preserving for this exact guarded program but is
not a faithful general model of Python conditional control and exceptions.
These limitations do not narrow the HumanEval domain or permit a false target
result.

All candidate prose, generation records, traces, and prior `#Top` reports were
treated only as untrusted claims. The decisive evidence is reviewer-generated
under `evidence/`.

## 1. Input and provenance integrity

### Declared layout and required records

`/audit-input.json` declares:

- problem `90-next-smallest`;
- condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- `mount_reference_semantics = false`.

The required regular records exist and are readable:

- `/audit-input.json`, `/audit-campaign-lock.json`;
- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`,
  `/generation-evidence/metrics.json`,
  `/generation-evidence/codex-last.txt`,
  `/generation-evidence/codex-output.log`,
  `/generation-evidence/prompt.txt`;
- the JSONL trace under `/generation-evidence/codex-trace/`.

`usage.json` is present and was inspected. The legacy records
`legacy-metrics.json` and `legacy-run-input.json` are also present and match
their recorded output hashes. A historical `runtime-metrics.json` is absent,
but it is not required for `legacy-selected-stage1`.

Every required mount and every entry below `/candidate`, `/reference`, and
`/generation-evidence` is a real regular file or real directory; no symlink or
special entry was found. `/reference/reference-semantics` is absent, as
required by `GENERATED_SEMANTICS`. There is therefore no supplied or inferred
reference semantics in this review.

### Campaign and hashes

The parsed `/audit-campaign-lock.json` object is exactly equal to the
`audit_campaign` block in `/audit-input.json`. Its independent SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
equal to the recorded hash.

Independent file hashing matched every launcher-recorded hash used here,
including the run/task/result manifests, invocation, metrics, usage, generation
prompt, final message, complete output log, trusted canonical, trusted prompt,
and trusted translator. The candidate prompt is byte-identical to
`/reference/prompt.py`; the candidate translator is byte-identical to
`/reference/py2mpy.py`.

The independently recomputed pipeline-v2 tree digest of `/candidate` is
`69ce4d6d8781a01b697aefa0f90c41c29975b575695531e6b030819a6eb7013f`,
equal to both the retained workspace hash in `invocation.json` and the workspace
hash in `generation-result.json`. The corresponding trace-tree digest is
`9790c22b0393e1464a5013324143063934eaed53fe65518b993e8a84f0fca1ce`,
equal to `usage.json`'s source-trace hash. The audit manifest also records
launcher-specific directory digests under different fields; their serialization
scheme is not specified, so I did not compare unlike directory-digest schemes.
All individual generation output files matched the hashes in both
`invocation.json` and `generation-result.json`.

The structured trace has one JSONL file and 195 valid JSON records. The review
parsed every record, inventoried all 34 recorded tool calls, and read every byte
of the 360,544-byte unstructured generation log. Those records were not used as
proof evidence.

Evidence:

- `evidence/stage1_integrity.py`
- `evidence/stage1_integrity.log` — exact command, all comparisons, trace
  inventory, and exit status 0

No provenance or mount contradiction was found, so the audit proceeds as a
candidate audit rather than an infrastructure error.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From `/reference/prompt.py` and `/reference/canonical.py`, the contract is:
given any finite list of integers, return the second **distinct** smallest
integer; return `None` when the list has fewer than two distinct values. The
`[1, 1] -> None` example resolves the potential ambiguity about whether equal
occurrences count as first and second.

The canonical implementation computes `sorted(set(lst))` and returns element 1
when its length is at least 2. `/candidate/solution.py` computes the same sorted
distinct list and uses the equivalent condition `len(distinct) > 1`. It
preserves the required function name and single parameter.

### Trusted translation fidelity

I copied only source artifacts into
`/tmp/audit-work/90-next-smallest/candidate-src`, ran the trusted mounted
translator from the scratch reference copy, and compared its output to the
submitted `solution.mpy`. Both files have SHA-256
`e63a1fb4ace43a6e28f18d4f978372df2cc093a57b1b01c854ce86266fe0381b`;
`cmp` exited 0. Thus the submitted constructor program is an exact trusted
translation of the submitted Python program.

Evidence: `evidence/translator_fidelity.log`.

### Independent differential testing

`evidence/differential_test.py` independently imports the trusted canonical
entry point and the generated entry point. Its third oracle is a two-minimum
scan that does not use either implementation's `set`/`sorted` construction.
It checks:

- all four documented examples;
- empty, singleton, all-equal, and exactly-two-distinct branch boundaries;
- ascending, descending, duplicate-heavy, negative, and repeated-second cases;
- arbitrary-precision positive and negative Python integers;
- every list of length 0 through 6 over `(-3, -1, 0, 2, 5)`, totaling 19,531
  exhaustive cases;
- 1,000 deterministic generated lists of length up to 60, including injected
  duplicates.

All three implementations agreed on 20,543 cases with zero mismatches. The
complete bounded output and exit status 0 are in
`evidence/differential_test.log`. This supports program-to-canonical fidelity;
it is finite evidence, not a universal proof.

## 3. Clean proof reconstruction

No candidate-provided compiled definition was present or reused. The scratch
copy contained only candidate source files and trusted reference files. K
v7.1.293 was independently observed for `kompile`, `krun`, and `kprove`
(`evidence/toolchain.log`).

### Fresh concrete semantics

The generated semantics was rebuilt with:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/90-next-smallest/semantic-fresh-kompiled
```

The command exited 0 (`evidence/llvm_build.log`). The reviewer-authored
`evidence/concrete_semantics_test.py` then ran the actual submitted
`solution.mpy` under that definition on 12 normal and boundary inputs. It
included empty, singleton, duplicate-only, two-distinct in both orders,
documented cases, negative/duplicate-heavy cases, all-equal cases, and
arbitrary-precision integers. Every `krun` exited 0, consumed `<k>` to `.K`,
and matched both generated Python and the independent scan oracle. Exact
commands and complete final configurations are in
`evidence/concrete_semantics_test.log`.

### Fresh proof definition and all positive claims

The proof definition was rebuilt with:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition \
  /tmp/audit-work/90-next-smallest/verification-fresh-kompiled
```

It exited 0 (`evidence/haskell_build.log`).

`spec.k` contains exactly one target reachability claim, labeled
`next-smallest-correct`; there are no helper or loop claims. I ran it
independently:

```text
kprove spec.k \
  --definition \
  /tmp/audit-work/90-next-smallest/verification-fresh-kompiled \
  --spec-module SPEC --claims next-smallest-correct --output pretty
```

The actual output was `#Top` and the exit status was 0
(`evidence/positive_kprove.log`). Thus the clean dynamic reconstruction gate
passes.

## 4. Adequacy and real-program pinning

### Claim in plain language

The entry claim at `/candidate/spec.k:8` has no `requires` clause.
Its starting state requires:

- `<k>` to contain the exact translated module with one
  `next_smallest(lst)` function and the submitted assignment/return body;
- `<input>` to contain arbitrary `L:IntList`;
- `<distinct>` to be the initial marker `none`;
- `<result>` to be the initial marker `noResult`.

Its destination requires:

- the computation to be fully consumed to `.K`;
- the input to remain `L`;
- `distinct` to be `pyList(uniqueSort(L))`;
- the result to be `secondSmallest(L)`.

`secondSmallest(L)` is not a free right-hand variable. The total definitional
rule at `/candidate/verification.k:9` rewrites it to:

```text
iteVal(
  lenInt(uniqueSort(L)) >Int 1,
  itemAt(uniqueSort(L), 1),
  none)
```

The result is therefore constrained. There is no one-way `ensures`
implication, existential result, or omitted result cell.

The precondition is satisfiable. Examples include `L = nil`,
`L = cons(1, cons(2, nil))`, and every concrete input in
`evidence/concrete_semantics_test.log`. For the second example, the claimed
result reduces concretely to 2; both trusted canonical and generated Python
also return 2. For `nil`, all three return `None`/`none`. Negative and
duplicate-heavy satisfying instances are also recorded.

### Mechanical program identity

`evidence/pinning_check.py` extracts the `Module(...)` term that the claim
actually executes, normalizes only whitespace, and compares it to the trusted
regeneration. The normalized constructor trees are identical and have SHA-256
`7c800cc508f76b8a38645105c706ed6fbb1d3fc0bc8f47aecdd974296574097e`.
Both texts also parsed during the fresh builds, so this is constructor-level
identity rather than a Python-source filename comparison. See
`evidence/pinning_check.log`.

The claim does not dynamically read `solution.mpy`, so changing only an
external file would not be a valid sensitivity test. I instead changed the
program term actually executed by the claim: the returned subscript index was
changed from 1 to 0 while the original result obligation was retained.
`evidence/spec-body-mutation.k` is the complete mutation. It built far enough
to execute the prover and failed with exit 1 and a
`WarnStuckClaimState` residual requiring:

```text
itemAt(uniqueSort(L), 0) == itemAt(uniqueSort(L), 1)
```

The concrete satisfying witness `[1, 2]` returns 1 in the mutated body but 2
under the original claim. This is direct body sensitivity, not a source-file
proxy. See `evidence/body_mutation_kprove.log`.

There are no helper claims to pin. The semantics' `Module` entry rule directly
invokes the body only when the function and parameter strings are exactly
`"next_smallest"` and `"lst"`. This is a generated invocation harness rather
than a general Python module/call stack, but it selects the submitted binding
unambiguously.

## 5. Rule-by-rule static soundness review

### Complete declaration inventory

`evidence/static_inventory.py` and `evidence/static_inventory.log` inventory
all local declarations. There are 14 syntax declarations, one configuration,
41 local rules, and one reachability claim. There are no local priority
declarations and no local `[simplification]` rules.

The syntax declarations are:

| Location | Declaration and productions | Use |
|---|---|---|
| `semantic.k:7` | `Program ::= Module(Stmts)` | submitted root |
| `semantic.k:8` | empty-separated `Stmts` list | two-statement body |
| `semantic.k:9-11` | `Stmt ::= FuncDef | Assign | Return` | every submitted statement |
| `semantic.k:12` | one-string `Params` | `lst` |
| `semantic.k:13-19` | `Expr ::= Name | Int | NoneVal | Call | Compare | Subscript | IfExp` | every submitted expression |
| `semantic.k:20` | `CmpOp(String, Expr)` | `> 1` |
| `semantic.k:24-25` | `IntList ::= nil | cons(Int, IntList)` | full finite integer-list domain |
| `semantic.k:33-39` | `PyVal ::= Int | Bool | none | pyList | pySet | invalidIndex | iteVal` | modeled values and error marker |
| `semantic.k:40` | `itemAt(IntList, Int)` as `[function,total]` | subscript summary |
| `semantic.k:42` | `Outcome ::= noResult | PyVal` | result cell |
| `semantic.k:44-58` | all `KItem` scheduling frames | explicit evaluation order |
| `semantic.k:124-125` | `uniqueSort` and `insertUnique` as `[function,total]` | `sorted(set(...))` model |
| `semantic.k:136` | `lenInt` as `[function,total]` | length |
| `verification.k:8` | `secondSmallest` as `[function,total]` | declarative postcondition |

The configuration at `semantic.k:60-66` has exactly the state this program
needs: computation, immutable input, the one local `distinct`, and result.
Every cell is read or written. There is no heap, allocation, output, or
exception cell. That omission is acceptable for ordinary `list[int]` inputs
and this pure function, subject to the conditional-expression caveat below.

### Construct-to-rule map and all 41 rule decisions

The following grouping explicitly accounts for every local rule:

| Rules | Count | Static decision |
|---|---:|---|
| `semantic.k:70-71` module entry | 1 | Valid invocation bridge for the exact submitted name, parameter, and body; it changes only `<k>`. It is not a general Python binding/call semantics. |
| `semantic.k:73-74` empty/nonempty statement execution | 2 | Disjoint list cases and left-to-right statement scheduling. Correct for the assignment followed by final return. |
| `semantic.k:76-80` assignment schedule/commit | 2 | Evaluates RHS before updating `distinct`; exact target binding and cell footprint. |
| `semantic.k:81-83` return schedule/commit | 2 | Evaluates the return expression and sets the initially empty result. Correct because the submitted return is final. The rules do not generally discard a later statement continuation. |
| `semantic.k:85-90` `lst`, `distinct`, integer, and `None` evaluation | 4 | Exact bindings and literal values; patterns are disjoint. |
| `semantic.k:92-93` `set` call schedule/result | 2 | Argument first, then wraps the integer list as `pySet`. Duplicate removal is intentionally delayed to sorting and has no observable intermediate effect here. |
| `semantic.k:94-96` `sorted` call schedule/result | 2 | Argument first; `pySet(L)` becomes `pyList(uniqueSort(L))`. This is the principal builtin bridge, checked below. |
| `semantic.k:97-98` `len` call schedule/result | 2 | Argument first and exact `lenInt` result. |
| `semantic.k:100-104` comparison left/right/application | 3 | Preserves left-to-right evaluation and computes stored left `I1 >Int` right `I2`; operator string must be exactly `">"`. |
| `semantic.k:106-110` subscript base/index/application | 3 | Preserves base-before-index evaluation and uses the exact integer index. |
| `semantic.k:115-121` conditional condition/then/else/assembly | 4 | Deterministic and result-correct for this pure guarded expression, but eagerly evaluates both branches; limitation detailed below. |
| `semantic.k:126-127` `uniqueSort` base/step | 2 | Exhaustive over constructor lists and structurally descending. Ordinary induction reduces correctness to `insertUnique`. |
| `semantic.k:128-134` four `insertUnique` cases | 4 | Nil plus `<`, `==`, and `>` are exhaustive and pairwise disjoint over mathematical integers. `<` prepends, `==` removes the duplicate, and `>` recurses on a shorter tail. On a sorted unique tail this preserves sorting and uniqueness. |
| `semantic.k:137-138` `lenInt` base/step | 2 | Exhaustive constructor-list length, structurally descending, no overlap. |
| `semantic.k:140-143` three `itemAt` cases | 3 | Index 0 and positive recursion are disjoint; nil becomes the explicit `invalidIndex` marker. Exact calls use index 1. Negative indices on nonempty lists have no equation despite `[total]`; this is an unused totality gap. |
| `semantic.k:152-153` concrete `iteVal` true/false | 2 | Pairwise disjoint Boolean selection equations. The enclosing `[concrete]` module excludes their symbolic use in the Haskell proof and supplies concrete LLVM selection. |
| `verification.k:9-12` `secondSmallest` | 1 | Unguarded, exhaustive definitional summary; it names the sorted-distinct index-1 contract and does not replace a program-defined function body. |

Total: 41 rules.

### Mathematical and operational checks

**`uniqueSort` and the builtin bridge.** For every finite constructor list,
ordinary structural induction shows `uniqueSort` returns its values in
ascending order with duplicates removed. The base is `nil`. In the step, the
inductive tail is sorted and unique; the four `insertUnique` equations either
place the head before the first larger element, discard it at equality, or
recurse past a smaller element. Integer trichotomy gives guard coverage and
disjointness. Recursion strictly descends through the finite tail. Therefore
`pyList(uniqueSort(L))` is extensionally Python `sorted(set(L))` for ordinary
mathematical integers. The 12 rebuilt K runs independently exercise all guard
outcomes and boundaries, but those finite runs do not replace this argument.

The operational `sorted` rule and the postcondition both mention
`uniqueSort`. That would be circular if `uniqueSort` were a fresh oracle. It is
not: its ground value is fixed by the exhaustive terminating equations above.
Nevertheless, the target reachability proof itself does not prove the
sorted/unique invariant, because the equations are `[concrete]`; the bridge is
part of the generated-semantics trust boundary.

**Length, indexing, and the result.** `lenInt` is the usual list length.
Whenever `lenInt(uniqueSort(L)) > 1`, `itemAt(uniqueSort(L), 1)` reaches the
second constructor and cannot reach `invalidIndex`. Otherwise
`secondSmallest` selects `none`. Thus the definitional postcondition is
equivalent to the natural-language contract over every finite integer list.

The `[total]` declaration on `itemAt` is broader than its equations:
`itemAt(cons(I, IS), N)` has no reducing rule for `N < 0`. This does not affect
the submitted program, whose only index is positive 1, nor does it create a
false target result. I classify it as a totality-evidence gap rather than an
unsoundness claim; no false conclusion witness on the intended theorem domain
exists.

**Evaluation order and control.** Calls, comparisons, and subscripts use
explicit continuation frames and preserve the source operand order. There are
no overlaps or priorities that can preempt these transitions. Assignment
updates only `distinct`, and return updates only `result`.

The conditional is intentionally eager. For `L = nil`,
`evidence/ifexp_control_probe.log` shows the fresh semantics at depth 20
evaluating the `Subscript` despite a false condition, at depth 24 reaching
`subscriptRight(nil)`, and at depth 28 forming
`iteVal(false, invalidIndex(1), none)`. It then selects `none`. Python instead
skips the subscript branch. This is semantically inert for this exact program:
the branches are otherwise pure, and the same length guard makes the
index-1 value valid exactly when selected. It would not be a sound reusable
Python rule for effectful or exception-observable branch expressions.

Similarly, the return rules do not generally unwind an arbitrary later
statement continuation. The submitted return is syntactically last, so the
only continuation is `exec(.Stmts)` and the real control flow is preserved.
These two facts are over-broad generated-language limitations, not false-rule
findings for the immutable target. I therefore do not label them unsound and
do not use off-target programs as false-conclusion witnesses.

**Bindings and Python domain.** Literal name patterns bind the exact builtin
calls `set`, `sorted`, and `len`; the submitted module defines no shadowing
binding. `IntList` covers arbitrary finite length and K mathematical `Int`
covers arbitrary precision, negatives, and zero. The theorem does not restrict
sizes, values, order, or duplicates. Non-integer objects, integer subclasses
with overloaded operations, unhashable elements, and general Python runtime
exceptions are outside the documented `list[int]` contract.

**No proof-rule answer smuggling.** No semantic rule rewrites the whole module
to the desired result, no program-defined helper is replaced by an opaque
oracle, and there are no proof-local lemmas, priorities, or simplifications.
Every constructor in `solution.mpy` passes through its matching operational
rules. The only proof-local rule defines the postcondition function itself.

The freshly compiled KORE confirms that `uniqueSort`, `lenInt`, and `itemAt`
are `function,total` symbols with concrete equations, while
`secondSmallest` is a symbolic total function and `iteVal` remains a
constructor in the Haskell proof. The bounded inspection command is recorded
in `evidence/fresh_kore_attributes.log`.

No inventoried rule was found to enable a false result on the intended input
domain. Consequently, this review makes no unsupported “unsound rule” finding
that would require a false-conclusion witness.

## 6. Fresh non-vacuity test

I did not rely on any candidate-supplied vacuity artifact. The fresh mutation
`evidence/spec-vacuity-fresh.k` leaves the exact program term and precondition
unchanged but changes the result obligation to `none` for every `L`. This is
demonstrably false for the satisfying input `L = cons(1, cons(2, nil))`, for
which rebuilt K, trusted canonical, and generated Python all return 2.

First, `kprove --dry-run` compiled the mutation and exited 0, excluding a
parser/import/build failure (`evidence/vacuity_build.log`). The real proof run
then exited 1 with `WarnStuckClaimState`. Its residual final result was:

```text
iteVal(
  lenInt(uniqueSort(L)) >Int 1,
  itemAt(uniqueSort(L), 1),
  none)
```

which could not unify with the mutated `none` destination. This is precisely
the expected unmet result constraint, not a timeout or unrelated crash. Exact
command and output: `evidence/vacuity_kprove.log`.

The independent body-sensitivity failure from stage 4 is separate and tests
source execution rather than only result constraint.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the freshly compiled submitted K definition, for every `L:IntList`, the
exact trusted translation of the submitted `next_smallest` body reaches:

```text
<k> .K </k>
<input> L </input>
<distinct> pyList(uniqueSort(L)) </distinct>
<result>
  iteVal(
    lenInt(uniqueSort(L)) >Int 1,
    itemAt(uniqueSort(L), 1),
    none)
</result>
```

This is a universal, unbounded reachability result under the generated
semantics. It is not a finite-size unrolling. The theorem is discriminating
with respect to both the executed body and result.

Together with the audited ground equations and ordinary mathematical argument,
that configuration returns the second distinct smallest mathematical integer,
or `none` when fewer than two distinct values exist. Trusted regeneration and
the source differential evidence connect the exact constructor body to the
generated Python body and trusted canonical.

### Trust ledger and exclusions

| Boundary | Status and dependents |
|---|---|
| K v7.1.293 compiler, Haskell/LLVM backends, K integer/Boolean primitives, constructor axioms | Trusted toolchain/math boundary. Every build, concrete run, and proof depends on it. Versions and fresh commands are recorded. |
| Trusted `/reference/py2mpy.py` transliteration | Trusted input boundary. Exact byte regeneration proves the claim term corresponds to `solution.py`; translator correctness as a general compiler is outside this theorem. |
| `Module` direct-entry harness | Informal generated-semantics bridge from “call the HumanEval entry point” to body execution. Exact literal function/parameter matching and body sensitivity support it. No general Python call stack is claimed. |
| `set`/`sorted` to `uniqueSort` | Result-bearing builtin bridge. Ground values are fixed by exhaustive recursive equations and audited by induction; 12 K cases add finite evidence. There is no separate bridge-free K connection theorem to CPython builtins. |
| `[concrete]` `uniqueSort`, `insertUnique`, `lenInt`, `itemAt` equations | Concrete ground semantics and static mathematics fix their intended values. They remain opaque during symbolic closure, so the target `#Top` alone does not validate their meaning. |
| `iteVal` and `invalidIndex` | `iteVal` selects concrete Boolean branches. `invalidIndex` is an opaque error marker that appears only in the unselected branch for intended invalid index-1 cases; it cannot affect the selected target result. Python exception traces are not modeled. |
| `secondSmallest` | Definitional specification, not an external oracle: it expands unconditionally to sorted-distinct length/index selection. The human-facing interpretation relies on the audited helper equations. |
| Python/canonical equivalence | The implementations are directly mathematically equivalent and agreed with an independent oracle on 20,543 recorded cases. Testing is finite support, not the K proof. |

Excluded behavior includes non-integer inputs, overloaded integer subclasses,
hash/comparison side effects, memory exhaustion, general function/module
binding, post-return statements, effectful conditional branches, and Python
exception objects/traces. None is part of the documented HumanEval
`list[int]` contract or occurs in the submitted body.

### Gate and verdict reasoning

- Clean verification gate: pass. Fresh builds succeeded and every positive
  target claim printed `#Top` with exit 0.
- Real-program pinning/result constraint: pass. Trusted regeneration matches
  the executed term; body and result mutations fail meaningfully.
- Domain adequacy: pass. All finite mathematical integer lists are covered
  without a size/value restriction.
- Static target soundness: pass with limitations. The recursive helper rules
  are mathematically valid and no false intended result is enabled, but their
  relation to Python builtins is an audited generated-semantics boundary rather
  than an independently proved K connection theorem.
- Auditability/non-vacuity: pass. Reviewer scripts, inputs, exact commands,
  bounded outputs, and exit statuses are preserved under `evidence/`.

The limitations are material enough to disclose but do not substitute a
different program, narrow the source-contract domain, make the theorem
vacuous, or enable a false result. The proper benchmark classification is
therefore legitimate with concerns, not `FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
