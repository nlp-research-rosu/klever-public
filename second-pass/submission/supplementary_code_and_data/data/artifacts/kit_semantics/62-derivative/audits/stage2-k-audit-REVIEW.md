# Independent adversarial review: 62-derivative

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. I did not rely on the candidate's
compiled definitions, `#Top` transcript, `PROOF.md`, mutation logs, or generation
report. I rebuilt both definitions from the mounted source tree, ran the positive
claims, compared parsed program terms, audited the proof-local theory, and made a
fresh false-result mutation.

## 1. Input and provenance integrity

The launcher record declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, and problem `62-derivative`. The trusted
`/reference/reference-semantics` mount is present, as this mode requires.

`evidence/integrity_check.py` independently walked and hashed the mounted
inputs. Its exact invocation and output are in
`evidence/stage1-integrity.log`; it exited 0. Findings:

- `/audit-input.json` and `/audit-campaign-lock.json` are readable regular
  files. The lock is byte-hash consistent with the recorded
  `ad5dfcc...d745`, and its JSON object exactly equals the
  `audit_campaign` block.
- Every `pipeline-v3` record is present and regular:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured
  trace. Each recorded ordinary-file SHA-256 matches. The
  `generation-result.json` hash for the sole JSONL trace file also matches.
- The structured trace contains one regular JSONL file, 406 events, and no
  parse errors. `evidence/stage1-trace-inventory.log` records all event-type
  counts. The generation records and trace were treated only as untrusted
  historical claims.
- The candidate tree has 780 walked entries and no symlink or special-file
  entries. The independently defined reviewer tree digest is recorded in the
  log. This digest uses an explicitly documented serialization in
  `integrity_check.py`; it is separate from the launcher's opaque aggregate
  tree-hash serialization.
- The candidate prompt and translator are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.
- The candidate and trusted supplied-semantics trees each contain exactly 25
  entries. Relative names, entry types, and every file hash agree. There are
  no missing, additional, changed, mistyped, or symlinked entries.
- All six required candidate proof deliverables are regular readable files.

There is no semantics-mode contradiction, missing provenance mount, or
unreadable required record. Thus no audit-infrastructure stop condition applies.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt says that `xs` contains the coefficients
`xs[0] + xs[1]x + xs[2]x^2 + ...` and asks for the derivative in the same
coefficient-list form. In plain language, the result is:

```text
[x0, x1, x2, ...] -> [1*x1, 2*x2, 3*x3, ...]
```

Empty and singleton lists therefore return `[]`. The trusted canonical
implementation is the list comprehension
`[(i * x) for i, x in enumerate(xs)][1:]`.

The candidate uses a different but equivalent loop. It starts `i = 0`, skips
the first iteration, appends `i * x` thereafter, and increments `i` once per
element. The false branch is exercised exactly at `i = 0`; the true branch is
first exercised at `i = 1`.

### Trusted translation

The exact command in `evidence/stage2-translator.log` ran the trusted translator
on `/candidate/solution.py`, wrote only to scratch, and compared the result with
the submitted `solution.mpy`. It exited 0, establishing byte identity.

### Independent differential

`evidence/differential_test.py` independently imports
`/reference/canonical.py` and `/candidate/solution.py`; it does not use the
proof equations. The recorded command in
`evidence/stage2-differential.log` exited 0:

```text
documented examples:       2
named boundary cases:      9
exhaustive small cases: 3906
seeded generated cases:  600  (lengths 0..80)
total:                  4517
mismatches:                0
```

The named cases include empty, singleton, the first true-branch boundary,
zeros, negatives, very large integers, floats, booleans, and Python sequence
coefficients. The script also checks exception behavior, result type, and input
mutation. This finite test supports implementation fidelity; it is not used as
a universal proof.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/62-derivative`. Candidate
`runtime-kompiled`, `verification-kompiled`, bytecode, caches, and transcripts
were neither copied nor used. Tool versions and locations are recorded in
`evidence/tool-versions.log`: K v7.1.293 at `/usr/bin`.

### Fresh concrete definition

The command in `evidence/stage3-kompile-llvm.log` was:

```text
kompile --backend llvm reference-semantics/semantics.k
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX
  --output-definition runtime-kompiled
```

It exited 0. The warnings identify non-exhaustive `[total]` functions in
unrelated supplied-semantics features; none is used by this program's intended
integer/float derivative path.

`evidence/concrete_smoke.py` is a fresh auditor program containing the exact
function body and assertions for empty, singleton, first-branch, both prompt
examples, negative/zero, and float inputs. The trusted translator produced the
scratch `.mpy` file. The `krun` command in
`evidence/stage3-krun-concrete.log` exited 0 with final `.K`, `NoExc`, and exit
code 0. Its heap records the expected lists.

### Fresh proof definition and positive claims

The command in `evidence/stage3-kompile-haskell.log` was:

```text
kompile --backend haskell verification.k
  --main-module VERIFICATION --syntax-module MPY-SYNTAX
  --output-definition verification-kompiled
```

It exited 0. Then:

- `SPEC.derivative-loop` was selected alone. It printed `#Top` and exited 0;
  see `evidence/stage3-kprove-loop.log`.
- The complete submitted claim set was run with
  `kprove spec.k --definition verification-kompiled --spec-module SPEC`.
  It printed `#Top` and exited 0; see
  `evidence/stage3-kprove-all.log`. Aggregate `#Top` requires both positive
  claims to close, and the entry claim has its declared loop circularity
  available in this invocation.

For completeness, `evidence/stage3-kprove-entry.log` records a diagnostic that
selected the entry claim while excluding its loop claim. That removes the
circularity and causes unbounded concrete unrolling; I interrupted that
non-target diagnostic with exit 130. It is not a failed candidate command and
is not used as positive evidence. The actual submitted proof set is the
successful complete invocation above.

The clean dynamic reconstruction gate passes.

## 4. Adequacy and real-program pinning

### Claims in plain language

`derivative-loop` says: at the real supplied-semantics
`#loop(list(VS), Name("x"), BODY)` control point, if `i = I >= 0`, the result
heap object contains `ACC`, and the remaining sequence has no raw heap handles,
then executing the loop consumes all of `VS` and changes that heap object to:

```text
derivAcc(ACC, VS, I)
```

It preserves the arbitrary continuation and framed cells. Final local `i` and
`x` are existential, which is safe because the post-loop source code returns
only `result`.

`derivative-entry` says: from the normal empty module/heap state, load the
literal function, call it with any finite `INPUT` satisfying
`noRefsVS(INPUT)`, return `ref(0)`, and leave heap location 0 containing:

```text
derivAcc(.ValSeq, INPUT, 0)
```

It additionally constrains allocation (`heapLoc = 1`), empty call stack,
restored environment, `noRet`, `NoExc`, and exit code 0. Only the final module
scope is existential; the source contract does not observe it.

### Mechanical constructor identity

This is not merely a textual resemblance. I:

1. parsed the trusted-regenerated `solution.mpy` to KORE;
2. used `kprove --dry-run` to compile the entry claim to KORE; and
3. extracted and compared the unique `Module(...)` application in each.

`evidence/compare_kore_program_terms.py` performs balanced KORE extraction and
whitespace normalization outside strings. The commands are in
`evidence/stage4-kast-solution.log`,
`evidence/stage4-kprove-dry-run.log`, and
`evidence/stage4-program-identity.log`. Both normalized constructor terms have
SHA-256:

```text
1176083a113f4a917ae2383d400c4f6917ffe9843ca528217e5f841dc61a6065
```

Thus the claim loads the same binding, parameter list, statement order, loop
target/body, append call, arithmetic expressions, and return as the translated
submitted program.

### Satisfying witnesses and result substitution

The entry precondition is satisfiable. For example:

```text
INPUT = vCons(1, vCons(2, vCons(3, .ValSeq)))
```

contains no `ref`, so `noRefsVS(INPUT) = true`. In the declared empty initial
heap and module scope, the formal result simplifies as:

```text
derivAcc([], [1,2,3], 0)
  = derivAcc([], [2,3], 1)
  = derivAcc([1*2], [3], 2)
  = [2, 2*3]
  = [2,6].
```

The helper claim is likewise satisfiable at the actual loop head, for example
with `I = 1`, `VS = [2,3]`, an allocated empty result at `H = 0`, the function
scope at environment 1, and the caller frame/continuation installed by the
fixed call rule.

Both trusted canonical Python and candidate Python return `[2,6]` on this
input (`stage2-differential.log`). Fresh K execution returns `[2,6]`
(`stage3-krun-concrete.log`), and the fresh negative proof exposes exactly that
heap (`stage6-auditor-vacuity.log`).

`noRefsVS` excludes internal K heap handles, not ordinary numeric source
coefficients. It imposes no bound on sequence length or integer magnitude and
includes the material integer and supported-float coefficient domain of the
polynomial contract. Raw handles, aliasing, user-defined multiplication, and
Python object kinds absent from the supplied subset remain model boundaries;
they are not a hidden finite or fixed-size restriction.

The adequacy and real-program-pinning gate passes.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_rule_inventory.py` inventories every declaration beginning with
`configuration`, `syntax`, `context`, `rule`, or `claim` in the assembled
supplied semantics, all 23 helper files, `verification.k`, and `spec.k`.
The exact generation command is in
`evidence/stage5-rule-inventory-command.log`; the 937-row inventory is
`evidence/rule-inventory.tsv`:

| Kind | Count |
|---|---:|
| configuration | 1 |
| syntax declarations | 229 |
| contexts | 5 |
| rules | 700 |
| claims | 2 |

The inventory records attributes as well: 148 function declarations, 108
`total`, 22 `no-evaluators`, 25 `symbol`, 45 priority, 35 concrete, 26
`owise`, 4 macro, and 3 simplification occurrences. There is no
`functional` declaration. All three simplification rules are the
proof-local `derivAcc` equations.

The candidate's supplied tree is byte-identical to the trusted fixed tree.
Rules for unused constructs cannot become task-answer axioms: they have
different outer constructors, operator/method strings, or value sorts from
the reachable redexes. I checked all potentially overlapping generic,
priority, `owise`, opaque, and total rules on the reachable path. The
compiler's uncovered-totality warnings concern unused `mapStrVS`, `floorFI`,
`toF`, `ceilF`, `joinCodes`, and out-of-bounds `valSeqAt` cases. These are
coverage gaps in other subset features, not false equations and not reachable
from the derivative theorem. No task term (`derivative`, coefficient, or
polynomial) appears anywhere in the supplied semantics.

### Construct-to-rule map for the submitted program

| Program construct | Declaration and material fixed rules |
|---|---|
| `Module`, statement sequence | `syntax.k:56,61`; `core.k:126-129` (`#loadAll`, sequencing, empty statements) |
| `FuncDef`, call, parameter | `syntax.k:53,57`; `functions.k:14`; `call.k:15-18,76-81`; `functions.k:63-69,78-89` |
| `Assign`, `Name` | `syntax.k:41,12`; `core.k:132-153`; `controls.k:9-18` |
| empty `ListExpr`, allocation | `syntax.k:17`; `list.k:13-16`; `core.k:117-121` |
| `For`, list iteration/target binding | `syntax.k:45`; `controls.k:56-69,105-108`; `list.k:8-9`; `tuple.k:31-39` |
| `If`, `Compare(i, > 0)` | `syntax.k:49,30,32`; `controls.k:47-50`; `operators.k:15-19`; `int.k:24`; `core.k:199-205` |
| `Attribute(...,"append")`, `Call` | `syntax.k:28-29`; `call.k:12-18`; `list.k:52-54` |
| `BinOp("*", i, x)` | `syntax.k:15`; `operators.k:10`; `int.k:14`; `float.k:115-117,138-139,195-202` |
| `i + 1` | `operators.k:10`; `int.k:9` |
| `Return(result)` and frame pop | `syntax.k:50`; `functions.k:78-89` |

Evaluation is left-to-right through strict/seqstrict syntax and the fixed
callee/argument machinery. On the intended path:

- the cell-assignment priority rule is disabled because the ordinary function
  frame has no `"$cells"` entry;
- the generic assignment rule therefore updates `i` and `x`;
- the list-append priority rule updates exactly the result heap object;
- `noRefsVS` prevents a raw handle in the coefficient position, so the
  ref-dereference operator rules cannot create an unaccounted aliasing step;
- integer `>` and multiplication rules are sort-disjoint from float rules;
- duplicated int/float equations in the fixed float module have identical
  right-hand sides, so their overlap is consistent; and
- return stores the actual result reference, restores the caller environment,
  deallocates the local scope, and leaves the heap allocation live.

### Proof-local inventory and decisions

There are exactly seven proof-local declarations/rules:

1. `derivAcc(ValSeq, ValSeq, Int)` is a mathematical result summary, not an
   operational bridge or opaque symbol.
2. Its empty rule returns the accumulator.
3. Its nonempty `notBool(I >Int 0)` rule skips that position and decreases the
   remaining sequence.
4. Its nonempty `I >Int 0` rule appends the fixed-semantics
   `applyBin("*", I, V)` and decreases the remaining sequence.
5. `noRefsVS(ValSeq)` is a total precondition predicate.
6. Its empty rule returns true.
7. Its cons rule applies the fixed total `isRefV` test and structurally
   recurses.

For `derivAcc`, empty versus cons is disjoint. On cons, `I > 0` and
`notBool(I > 0)` are disjoint and exhaustive over K integers, and both
recursive cases shorten `VS`. The equations do not replace a `<k>` operation;
the independently proved loop claim connects real execution to the summary.
The multiplication term is the fixed `applyBin`, not a fresh oracle.

For `noRefsVS`, empty versus cons is disjoint and exhaustive, recursion
shortens the sequence, and `isRefV` has a `ref` case plus an `owise` false
case. It affects claim applicability only.

`derivative-loop` is a reachability circularity, not an ordinary rewrite rule.
Its matched control term is the exact loop body and target. It quantifies over
the continuation, stack, other scopes, other heap entries, and allocation
counter rather than discarding them. Its only abstracted state is final `i/x`,
which no subsequent source operation observes. Its proof under fixed semantics
closed independently.

There are no proof-local priority rules, generic call interceptions, abrupt
control bridges, fresh/opaque result symbols, totality assertions beyond the
exhaustive predicate, or equations that encode the task answer without
executing the body. I found no unsound inventoried rule. Consequently there is
no claimed-unsound rule for which a false-conclusion witness is owed. The
uncovered fixed-semantics warnings are reported as the narrower coverage gaps
they are, not mislabeled as unsound equations.

The static soundness gate passes.

## 6. Fresh non-vacuity test

I inspected the candidate mutation only as untrusted historical evidence and
created a different mutation in `evidence/auditor-vacuity.k`. Its ground input
is `[1,2,3]`, which satisfies the entry precondition. It executes the exact
function term but changes the required result from the true `[2,6]` to the
demonstrably false `[2,5]`.

The exact command and output are in
`evidence/stage6-auditor-vacuity.log`. The mutation:

- parsed and built successfully;
- reached `ref(0)`, `.K`, `NoExc`, and exit code 0;
- exposed heap `0 |-> list([2,6])`;
- failed to unify with the required `[2,5]`;
- printed `WarnStuckClaimState`; and
- exited 1.

This is an unmet reachable result obligation, not a parser failure, missing
import, timeout, or unrelated crash. The proof is non-vacuous and
result-constraining.

## 7. Proven versus assumed accounting

### What is formally proven

Under the supplied MPY theory, for every finite `ValSeq INPUT` satisfying
`noRefsVS(INPUT)`, if execution terminates, the exact translated submitted
function returns a fresh reference whose heap list is:

```text
derivAcc([], INPUT, 0)
```

Equivalently within the modeled numeric domain, it drops the constant
coefficient and multiplies each later coefficient by its original zero-based
index. The theorem also establishes the listed normal control state: empty
call stack, restored environment, no pending return, no exception, and exit
code 0. The list length is symbolic and unbounded; this is not finite
unrolling.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K v7.1.293 parser, compiler, Haskell/LLVM backends, SMT/builtin integer theory | All parsing, rewriting, arithmetic, and reachability | Necessary low-level proof trust; version and fresh commands are recorded |
| Byte-identical supplied `reference-semantics` | Defines Python-subset control, environments, heap, calls, loops, mutation, and values | Authorized fixed semantics for this condition; relevant rules were statically checked and concretely exercised |
| Trusted `py2mpy.py` | Source-to-constructor bridge | Byte regeneration plus KORE constructor identity pins the submitted body |
| K integer/Boolean/map/list/string builtins | Result arithmetic and state operations | Ordinary fixed mathematical/collection primitives; no task-specific axiom |
| Supplied `intToF` and `mulF` (`symbol`, `total`, `no-evaluators`) | Symbolic float results | Explicit supplied-semantics trust boundary; LLVM concrete float assertions and Python tests provide finite support, not a universal IEEE theorem |
| Uncovered `applyBin("*", Int, Val)` cases for nonnumeric modeled values | May remain symbolic in a modeled result | Outside the material polynomial-coefficient domain and explicitly not claimed as a CPython object/exception theorem; it does not manufacture a concrete wrong numeric result |
| Natural-language interpretation of “polynomial coefficients” | Connects `derivAcc` to the requested mathematical derivative | Direct ordinary mathematics, additionally supported by canonical differential tests |
| Termination | Whether a final state is reached | Not formally proved; acceptable because the requested theorem is partial correctness. Structural consumption of a finite sequence is an informal termination argument |
| Differential and concrete tests | Source/canonical and finite semantics alignment | Empirical support only; not substituted for the universal K proof |

The internal-handle exclusion does not materially narrow the HumanEval source
contract: numeric coefficients are self-contained K values, and list length
and integer magnitude remain unrestricted. Python user objects, aliasing,
custom `__mul__`, and sequence-repetition behavior outside the supplied subset
are model exclusions, not finitely bounded proof domains.

### Gate and decision summary

- Fresh verification: pass.
- Gate A, real-program soundness and non-vacuity: pass.
- Gate B, full material HumanEval domain and intended postcondition: pass.
- Gate C, trust/evidence auditability: pass.

The reconstructed theorem is sound, result-constraining, unbounded over finite
input length, and mechanically pinned to the real translated program. The
named supplied-semantics boundaries do not create a material adequacy gap for
the polynomial coefficient domain.

VERDICT: PASS
LEGITIMACY: LEGIT
