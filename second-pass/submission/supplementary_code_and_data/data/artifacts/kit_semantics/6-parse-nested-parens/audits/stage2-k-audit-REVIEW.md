# Independent adversarial audit: 6-parse-nested-parens

The candidate contains a legitimate unbounded partial-correctness proof of the
submitted program on the HumanEval contract domain. I rebuilt every definition
from source in isolated scratch space, reran the positive proof, checked the
executed constructor term against the trusted regeneration, reviewed all local
and supplied K declarations/rules, changed the program body actually executed
by the theorem, and supplied a fresh false-result claim. No candidate-built
definition, prior `#Top`, report, trace, or log was trusted.

The complete reviewer evidence index is
[evidence/INDEX.md](/audit-output/evidence/INDEX.md). The toolchain was K
v7.1.293 and Python 3.10.12
([toolchain.log](/audit-output/evidence/toolchain.log)).

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem
`6-parse-nested-parens`, and the expected container mounts. I read the
launcher-owned audit input, campaign lock, run/task/result manifests, all
pipeline-v3 generation records, the 417-event structured trace, and the
candidate final report as untrusted historical evidence.

The independent integrity checker and full bounded output are
[check_integrity.py](/audit-output/evidence/check_integrity.py) and
[stage1-integrity.log](/audit-output/evidence/stage1-integrity.log). It found:

- `/audit-campaign-lock.json` is byte-hashed to the recorded
  `ad5dfc...d745` value and its parsed JSON exactly equals the
  `audit_campaign` block.
- Every launcher-declared mount exists with the correct regular-file or
  directory type. All required pipeline-v3 records are readable. The structured
  trace contains one regular JSONL file and no nonregular entry.
- Every directly recorded file hash matched independently, including
  `/run.json`, `/task.json`, `/generation-result.json`, invocation, metrics,
  runtime metrics, usage, prompt, output log, final message, and the structured
  trace file.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts. Their recorded hashes also match.
- SUPPLIED_SEMANTICS is internally consistent with the mounts:
  `/reference/reference-semantics` is present. Recursive relative-path, entry
  type, and content-hash comparison found 25 entries in each candidate/trusted
  tree, with `missing=[]`, `additional=[]`, `changed=[]`, and no candidate
  symlink.

There is no infrastructure breach and no supplied-semantics integrity failure.
The generation trace's `VALIDATED` and `KPROVE_PASSED` assertions were not used
as proof evidence.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted [prompt.py](/reference/prompt.py) asks
`parse_nested_parens(paren_string: str) -> List[int]` to take one or more
space-separated groups of nested parentheses and return, in group order, the
greatest nesting depth of each group. Its example maps
`"(()()) ((())) () ((())()())"` to `[2, 3, 1, 3]`.

The trusted [canonical.py](/reference/canonical.py) splits on ASCII space,
ignores empty pieces, and computes each nonempty group's maximum running
parenthesis depth. The submitted [solution.py](/candidate/solution.py) performs
the equivalent single pass on the intended domain: `depth` tracks current
nesting, `deepest` tracks the current group's maximum, and a space emits and
resets a nonempty group's maximum. Leading, trailing, and repeated spaces are
ignored. `()()` is one group with result `1`, which agrees with the canonical
split behavior.

The intended domain consists of balanced groups made only of `(` and `)`,
separated by ASCII spaces. That is what “groups for nested parentheses
separated by spaces” denotes; malformed/unbalanced text and other characters
are not group inputs promised by the prompt. Empty and spacing-only strings
were nevertheless checked as boundaries and both implementations return `[]`.

### Trusted regeneration

In scratch, I ran:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

The regenerated and submitted files both had SHA-256
`f1320cc5...b3848c` and `cmp` reported byte identity
([stage2-regeneration.log](/audit-output/evidence/stage2-regeneration.log)).
Thus [solution.mpy](/candidate/solution.mpy) is the trusted translator's exact
output for the submitted Python.

### Independent differential test

[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted canonical and submitted entry points under separate module names and
uses a separately written prefix-depth oracle. It covers:

- the documented example, empty/spacing-only inputs, one pair, nested pairs,
  adjacent top-level pairs, and leading/trailing/repeated spaces;
- every balanced parenthesis word with one through six pairs (196 groups);
- every ordered pair of those groups with one, two, and three spaces; and
- 27,000 representative three-group cases.

The corpus contained 143,039 unique inputs, digest
`38b903...f1cf9c`, and produced zero canonical/oracle or
candidate/oracle mismatches
([stage2-differential.log](/audit-output/evidence/stage2-differential.log),
exit 0). This finite test supports fidelity and intent; it is not substituted
for the symbolic proof.

## 3. Clean proof reconstruction

I copied only source inputs into `/tmp/audit-work/6-parse-nested-parens`,
using the trusted supplied-semantics tree. Candidate `runtime-kompiled`,
`verification-kompiled`, bytecode, and caches were neither copied nor used.

### Fresh concrete definition and execution

The exact fresh build was:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0
([stage3-kompile-runtime.log](/audit-output/evidence/stage3-kompile-runtime.log)).
The compiler reported nonexhaustive-match warnings in unrelated supplied
helpers; none is reachable from this program.

I translated and ran the reviewer-authored
[runtime_cases.py](/audit-output/evidence/runtime_cases.py), whose function body
is the submitted function and whose assertions cover empty, spaces, `()`,
`()()`, the prompt example, nesting, and repeated boundary spaces. `krun`
exited 0 at `<k> .K </k>`, `<exc> NoExc </exc>`, and exit code 0. Its heap
contains exactly the expected lists
([stage3-krun-runtime.log](/audit-output/evidence/stage3-krun-runtime.log)).

### Fresh proof definition and all positive claims

The proof definition was rebuilt with:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0
([stage3-kompile-proof.log](/audit-output/evidence/stage3-kompile-proof.log)).
Then:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

printed `#Top` and exited 0
([stage3-kprove-all.log](/audit-output/evidence/stage3-kprove-all.log)). This is
the candidate's required positive proof problem and contains both
`SPEC.scan-loop` and `SPEC.parse-nested-parens`.

I also selected the loop claim alone:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.scan-loop
```

It printed `#Top` and exited 0
([stage3-kprove-scan-loop.log](/audit-output/evidence/stage3-kprove-scan-loop.log)).
Filtering only `SPEC.parse-nested-parens` removes the loop circularity it
intentionally depends on; a bounded diagnostic of that different proof problem
was interrupted after ten seconds and is not a candidate failure. The proper
whole-spec invocation above independently reconstructed the entry theorem with
its proved helper.

The clean dynamic reconstruction gate passes.

## 4. Adequacy and real-program pinning

### Claims in plain language

The helper claim [spec.k](/candidate/spec.k) `scan-loop` says: from the exact
supplied-semantics loop state over an arbitrary finite remaining character
sequence `CS`, with locals `depth=D`, `deepest=M`, `depths=ref(H)`, and
`char=CH`, executing the exact `loopBody` finishes the loop, updates those
locals to the scanner summaries, updates heap list `H` to the output summary,
and preserves the framed configuration.

A concrete satisfying helper state is, for example:

```text
CS=.IntSeq, D=0, M=0, OUT=.ValSeq, CH=str(.IntSeq),
L=1, H=7, INPUT=.IntSeq
```

with the exact five-binding scope and heap entry shown in the claim. There is
no additional `requires` condition, and this constructor state is realizable.

The entry claim `parse-nested-parens` says: from the normal initial module
configuration, load the submitted function binding and call it on every finite
`CS` satisfying `validInput(CS)`. If the execution terminates, it returns the
fresh reference `0`; heap location 0 contains
`list(expectedDepths(CS))`; module scope contains the exact loaded closure; the
callee frame is gone; allocation, stack, return, exception, environment, and
exit-code cells have their stated final values. This is an equality-style
result constraint, not a free variable or implication.

Satisfying entry witnesses include `.IntSeq`, `"()"`, and `"(()) ()"`.
`validInput` accepts all of them.

### Constructor-level identity

Program pinning has three independent links:

1. trusted regeneration is byte-identical to submitted `solution.mpy`;
2. reviewer KORE parses of the submitted module and the explicit module term
   have identical digest `94e6b7...baac` and are byte-identical
   ([pinning-expanded.mpy](/audit-output/evidence/pinning-expanded.mpy),
   [stage4-kast-constructor-comparison-attempt2.log](/audit-output/evidence/stage4-kast-constructor-comparison-attempt2.log));
3. the reviewer claim in [pinning.k](/audit-output/evidence/pinning.k) checks
   `solutionModule` against that complete normalized term. It printed `#Top`,
   exit 0
   ([stage4-kprove-pinning-attempt4.log](/audit-output/evidence/stage4-kprove-pinning-attempt4.log)).

The only omitted source information is the type annotation itself; the trusted
translator intentionally renders it as the typing-only `ImportFrom`, and that
import executes as a no-op under the supplied semantics. Every material
operation remains in the executed constructor term.

### Ground substitutions

[ground.k](/audit-output/evidence/ground.k) substitutes the empty input and the
character-code sequence for `"(()) ()"`, constraining the results to `[]` and
`[2, 1]`. It printed `#Top`, exit 0
([stage4-kprove-ground.log](/audit-output/evidence/stage4-kprove-ground.log)).
Both Python implementations also returned `[2, 1]` for that exact input
([stage4-ground-python.log](/audit-output/evidence/stage4-ground-python.log)).

### Actual-body sensitivity

The fresh [body-sensitivity.patch](/audit-output/evidence/body-sensitivity.patch)
changes `Assign(Name("depth"), Int(0))` to `Int(1)` in the
`solutionBody` equation used by `#loadAll`; it does not merely edit an external
Python file. I rebuilt a separate Haskell definition from that changed K source
and ran the unchanged original target. The proof exited 1 with
`WarnStuckClaimState`; the residual contains the mutated closure body and the
unmet equation between `finishOutput(CS,0,0,...)` and execution starting from
depth 1
([stage4-kprove-body-mutation.log](/audit-output/evidence/stage4-kprove-body-mutation.log)).
The theorem is therefore sensitive to the program body it actually executes.

The claim is result-constraining and pins the real regenerated program.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[inventory_k.py](/audit-output/evidence/inventory_k.py) generated
[rule-inventory.tsv](/audit-output/evidence/rule-inventory.tsv), SHA-256
`5e816e...6465`. It inventories every declaration beginning with `syntax`,
`configuration`, `context`, `rule`, or `claim` across the assembled supplied
semantics, all helper K files, `verification.k`, and `spec.k`. There are 986
entries:

| Kind | Count |
|---|---:|
| syntax declaration | 246 |
| ordinary/equational/operational rule | 732 |
| context | 5 |
| configuration | 1 |
| claim | 2 |

Each row records source/line, complete normalized declaration block,
attributes (including `function`, `total`, `symbol`, `no-evaluators`,
`concrete`, `priority`, `owise`, and macros), role, and a review decision.
There are no proof-local simplification, priority, `owise`, `functional`, or
opaque declarations. The candidate's 19 proof-local functions are ordinary
total definitional functions; its only proof extensions beyond those equations
are the two reachability claims.

### Used construct-to-rule map

| Submitted construct | Supplying declarations/rules and checked behavior |
|---|---|
| `Module`, `ImportFrom`, statement sequence | `syntax.k`; `core.k` `#loadAll`/statement sequencing; `controls.k` generic non-math import no-op. The typing import has no runtime effect. |
| `FuncDef`, `Call`, parameter binding, `Return` | `functions.k` and `call.k`. The named module binding is resolved normally, arguments evaluate left-to-right, a fresh call frame is pushed, and return sets/pops the frame while preserving the returned reference. |
| locals and `Name` | `core.k` lookup and `controls.k` assignment. The exact current scope is read/written; no closure-cell rule can match the plain frame. |
| `ListExpr`, reference allocation, `.append` | `list.k`, `core.k`, and `call.k`. The empty list allocates fresh heap location 0; `append` is the mutating-method priority case and updates that same list in place without allocating. |
| `Str`, string iteration | `str.k` and `iter.k`. ASCII literals map to code sequences, and each `#iterNext` yields a one-character string and the finite suffix. |
| `For` and loop control | `controls.k`. The iterable is evaluated once; each yield binds `char`, executes the exact body, and returns through the loop label. No body branch contains abrupt return/break/exception. |
| `If`, `Compare`, truthiness | `syntax.k` strictness, `operators.k`, `str.k`, `int.k`, and `core.k`. Operand order is preserved; equality and integer `>` return booleans; branches use boolean truthiness. |
| `AugAssign` `+`/`-` | `controls.k` and `int.k`. For these local integer names, the old value and evaluated integer RHS produce the exact mathematical update. |
| expression statement | `controls.k`. The `noneV` returned by append is discarded after its heap effect. |

The configuration cells and allocation behavior match the entry postcondition:
module environment 0, builtins at -1, call scope 1, heap location 0 for the
single list, empty stack after pop, `noRet`, `NoExc`, and exit code 0.

### Candidate equations

I checked every [verification.k](/candidate/verification.k) equation:

- `loopBody`, `afterLoop`, `solutionBody`, and `solutionModule` are exact
  constructor aliases. They replace no program execution; they normalize to
  syntax before the supplied operational rules run.
- `nextDepth` partitions character codes into 40, 41, and all others.
  `scanDepth` consumes exactly one sequence constructor per recursive step.
- `openDeepest` partitions `D+1 > M` versus `<=`; `delimiterDeepest`
  partitions `M > 0` versus `<=`; `nextDeepest` has disjoint/exhaustive
  character cases; `scanDeepest` descends structurally.
- `delimiterOutput` appends exactly a positive completed maximum;
  `nextOutput` has the same exhaustive character partition; `scanOutput`
  consumes one character while using the pre-character `M`, exactly as the
  implementation does.
- `scanChar` yields the prior `CH` on an empty suffix and the last one-character
  string otherwise, matching loop-target binding.
- `finishOutput` appends the final positive maximum and otherwise leaves output
  unchanged. `expectedDepths` starts all accumulators at zero/empty.
- `wellFormedStep` partitions codes 40, 41, 32, and other. Closing and separator
  cases return false at invalid depths rather than silently assuming validity.
  `wellFormed` is structurally recursive and checks final depth zero;
  `validInput` starts at zero.

All total functions have exhaustive constructor/guard coverage on their
declared sorts, the guards are disjoint or agree, and recursive calls strictly
descend on `IntSeq`. No equation is an oracle or contains a task result.

### Loop circularity and state footprint

`SPEC.scan-loop` is a derived reachability lemma, not an operational rewrite.
Its matched and justified contexts coincide. It executes the fixed
`#iterNext`, target binding, comparisons, assignments, append, and loop label
before circular reuse. It reads/writes exactly `depth`, `deepest`, `char`, and
heap entry `H`; it preserves `paren_string`, `depths=ref(H)`, parent/environment,
arbitrary continuation, all framed scope/heap entries, allocation counters,
stack, return state, exception state, and exit code. Since the body has no
abrupt control, its arbitrary continuation framing is sound.

The claim is universal over arbitrary `D`, `M`, `OUT`, `CH`, and finite `CS`;
the scanner equations model even non-parenthesis codes consistently. The entry
theorem later restricts those codes to the contract.

### Supplied opaque and unused rules

The supplied fixed semantics declares the following symbolic primitives:
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, `sortKeyVS`, and `md5hexCodes`. It also contains
concrete-only keyed-sort/deep-equality rules. None can occur in the submitted
program or either proof claim: there are no floats, sorting, MD5, dicts, sets,
subscripts, comprehensions, or corresponding calls. They do not influence
control, state, result, or the proof condition here.

All remaining nonmatching supplied rules were inspected and recorded as fixed
semantics outside this program's reachable term language. No false conclusion
witness exists on the intended input domain, so I make no unsoundness
allegation about them. The used supplied rules and every candidate-local rule
are accepted. In particular, there is no task-answer rule, execution bypass,
unconstrained result-bearing abstraction, or circular use of an opaque value.

## 6. Fresh non-vacuity test

I inspected the candidate's `spec-vacuity.k` only after completing the
independent design. The fresh reviewer artifact is
[false-result.k](/audit-output/evidence/false-result.k).

Its ground input is `"()"` (`40,41`), which satisfies `validInput`; the
canonical and submitted Python both return `[1]`. The mutation instead demands
heap result `[2]`.

First:

```text
kprove false-result.k --definition verification-kompiled \
  --spec-module FALSE-RESULT --dry-run
```

successfully generated the KORE proof problem and exited 0
([stage6-false-result-dry-run.log](/audit-output/evidence/stage6-false-result-dry-run.log)).
The actual proof then exited 1 with `WarnStuckClaimState`; its residual is the
fully terminated program state with heap
`0 |-> list(vCons(1,.ValSeq))`, which cannot unify with the demanded `[2]`
([stage6-false-result-proof.log](/audit-output/evidence/stage6-false-result-proof.log)).
This is the intended unmet result obligation, not a parse error, missing
import, timeout, or unrelated crash.

Non-vacuity passes.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the supplied `MPY` definition, for every finite `CS:IntSeq` such that:

- every code is `(` (40), `)` (41), or ASCII space (32);
- every parenthesis prefix has nonnegative depth;
- a space occurs only at depth zero; and
- final depth is zero,

execution of the exact trusted-translated submitted module and named
`parse_nested_parens` call is partially correct. Its returned reference points
to a list formed by scanning groups in order, tracking the greatest open depth,
emitting that value at a separator, and emitting the final group at end. The
claim also establishes the stated final scope, allocation, stack, return,
exception, environment, and exit-code cells. The domain is symbolic and
unbounded in group count, group length, and nesting depth; it is not a finite
unrolling or examples-only theorem.

For a balanced parenthesis group, the greatest running count of opens minus
closes is exactly its deepest nesting level. `expectedDepths` is a constructive
definition of that quantity, and `validInput` ensures separators coincide with
group boundaries. This is ordinary structural/integer reasoning, confirmed by
the rule audit and finite differential evidence; it is not an assumed opaque
answer.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted supplied semantics for the used Python subset | Both claims and concrete K execution | Acceptable benchmark-fixed boundary. Candidate tree is byte-identical to the trusted tree; used rules were statically checked and dynamically exercised. |
| Trusted `py2mpy.py` | Program identity | Acceptable trusted input. Fresh regeneration is byte-identical; constructor/KORE pinning connects its output to the term executed by the claim. |
| K v7.1.293 frontend, Haskell/LLVM backends, reachability engine, builtin integer/string/map theories | All machine-checked results | Standard proof-tool trust boundary, explicitly recorded. |
| CPython 3.10 execution of trusted canonical and submitted Python | Differential evidence only | Finite empirical support, not a proof premise. |
| English interpretation “balanced nested-parenthesis groups separated by spaces” | Gate-B adequacy | Directly represented by `validInput`; no material contract restriction or fixed bound is introduced. |
| Supplied opaque float/sort/MD5 primitives | No dependent candidate term or claim | Inert and acceptable here; they are not smuggled into the result. |

Malformed groups, non-ASCII-space separators, and unrelated Python constructs
are outside the source contract and theorem. Complexity and total termination
are not separately claimed. Within the requested partial-correctness scope,
there is no material adequacy, soundness, or auditability gap.

VERDICT: PASS
LEGITIMACY: LEGIT
