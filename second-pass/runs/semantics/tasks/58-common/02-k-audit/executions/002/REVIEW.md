# Independent adversarial audit: 58-common

The candidate reconstructs cleanly, its three positive K claims close, its
function claim executes a macro expansion mechanically identical to the trusted
translation of `solution.py`, and a fresh false-postcondition mutation is
rejected.  Those facts are not enough to make the proof legitimate.  The
supplied list-membership semantics and the candidate's result summary compare
elements with K constructor equality (`==K`), not Python equality.  On valid,
normally terminating inputs such as `common([True], [1])` and
`common([1], [1.0])`, both the trusted canonical implementation and the
submitted Python implementation return a nonempty list, while fresh execution
of the exact translated program under the supplied semantics computes an empty
list.  The whole-function K claim has no precondition excluding these inputs.

The prompt annotates only `list` and says "common elements"; it does not
restrict elements to a homogeneous K-constructor domain.  The two witnesses
contain hashable, mutually sortable Python numeric values and the canonical
function returns normally.  This is therefore a material source-contract
domain gap, not merely an unused-language observation.  Under the benchmark's
explicit decision boundary, that makes the candidate `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, condition `semantics`, and
`semantics_mode = SUPPLIED_SEMANTICS`.  The required trusted
`/reference/reference-semantics` tree is present, so the rendered mode and
mounts are consistent.  No infrastructure stop condition was found.

The independent checker in `evidence/provenance_check.py` read and checked:

- `/audit-input.json` and `/audit-campaign-lock.json`;
- `/run.json`, `/task.json`, and `/generation-result.json`;
- `invocation.json`, `metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- the complete structured trace (477 JSONL records);
- the additional present legacy records `legacy-metrics.json` and
  `legacy-run-input.json`;
- all trusted reference inputs and all required candidate proof artifacts.

Historical `runtime-metrics.json` is absent, but it is not required for the
declared legacy-selected-stage1 layout.

The campaign-lock JSON is structurally identical to the `audit_campaign` block
and has the recorded SHA-256
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every recorded single-file digest checked by the script matched, including the
run, task, result, invocation, metrics, usage, prompts, logs, canonical, and
translator records.  The current candidate tree independently hashes to the
recorded Stage-1 workspace hash
`bd3c96e08804ddbe24e507fb7b9f583ebdd41b4125ec5ee2fe0678ed5c8311a5`
under the pipeline tree format.  The trace tree independently hashes to
`66554268622a66d26bd19acd4e6d402173901ebb7d802ab0528c80cce4cf9cce`,
matching `usage.json`.

The candidate prompt and translator are byte-identical to their trusted
mounts.  Recursive entry-type and content comparison between
`/candidate/reference-semantics` and
`/reference/reference-semantics` found exactly 25 entries, no missing or extra
entry, no type mismatch, no content mismatch, and no symlink.  The independently
implemented pipeline tree digest is
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
matching the recorded trusted semantics manifest hash.  All required candidate
proof artifacts are regular, readable, non-symlink files.  See
`evidence/provenance.log`.

The generation log and trace were treated only as untrusted history.  The
trace inventory in `evidence/generation-trace-inventory.txt` records all 90
tool calls and outputs, including several failed/stuck construction attempts
and the eventual claimed `#Top` runs.  None of those historical results was
used as proof reconstruction evidence.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: given two Python lists, return a sorted list containing
each element common to both lists once.  The trusted canonical function performs
nested Python `==` comparisons, inserts matches into a Python set, and returns
`sorted(list(ret))`.

The submitted `solution.py` scans `l1` left-to-right.  It appends an item when
Python membership says it occurs in `l2` and has not already been appended,
then returns `sorted(result)`.  This is extensionally equivalent to the
canonical algorithm for the ordinary hashable/sortable domain, although it is
a different algorithm.

Fresh translation used:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

Both commands exited 0.  Both files have SHA-256
`031e94b911c1eae40ab6f6bcda882685fd599c7c48bb1d39f2c3a804e517a352`;
see `evidence/translator-byte-identity.log`.

`evidence/differential_test.py` independently imports
`/reference/canonical.py` and the scratch copy of the generated implementation.
It checks the two examples, empty-side cases, both branches of each membership
test, duplicate suppression, sort reordering, negative and unbounded integers,
homogeneous strings, mixed bool/int equality, and mixed int/float equality.  It
also checks all 1,600 pairs of lists of length at most three over
`{-1, 0, 1}` and 10,000 seeded generated integer pairs with lengths from 0 to
20.  There were zero Python-to-Python mismatches
(`evidence/differential-test.log`).  In particular:

```text
FIRST=[True] SECOND=[1]     canonical=[True] generated=[True]
FIRST=[1]    SECOND=[1.0]   canonical=[1]    generated=[1]
```

Those outputs are separately preserved in
`evidence/semantic-domain-source-results.log`.

## 3. Clean proof reconstruction

All candidate source needed for execution was copied to
`/tmp/audit-work/58-common-002`.  Candidate-provided compiled definitions,
caches, `kore-exec.tar.gz`, and prior logs were not copied or used.
K v7.1.293 was available independently.

Fresh concrete build:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

This exited 0 (`evidence/llvm-kompile.log`).  Fresh execution:

```text
krun concrete-tests.mpy --definition audit-runtime-kompiled --output pretty
```

exited 0 with `.K`, `NoExc`, and semantic `<exit-code> 0`
(`evidence/concrete-krun.log`).

Fresh proof build:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition audit-verification-kompiled
```

exited 0 (`evidence/haskell-kompile.log`).  The three candidate-positive proof
targets were then run in their dependency order:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.member-fold --output pretty

kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.member-fold,SPEC.common-loop \
  --trusted SPEC.member-fold --output pretty

kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.member-fold,SPEC.common-loop,SPEC.common-function \
  --trusted SPEC.member-fold,SPEC.common-loop --output pretty
```

Each printed `#Top` and exited 0.  The corresponding bounded transcripts are
`evidence/kprove-member-fold.log`, `evidence/kprove-common-loop.log`, and
`evidence/kprove-common-function.log`.  Trusting the earlier claims in later
commands is not circular here because each dependency was first closed by its
own independent command.

The LLVM compiler emitted six supplied-semantics totality warnings for
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`.
They are reviewed in Stage 5.  They are not infrastructure failures and none
is reachable in this target proof.

## 4. Adequacy and real-program pinning

### Formal claims in plain language

1. `member-fold` has no explicit side condition.  In any framed continuation,
   it says that the supplied operational list-membership iterator
   `#memberAcc(V, list(VS))` returns the proof-local Boolean `memberVS(V, VS)`.

2. `common-loop` also has no `requires` clause, but its cells are a substantial
   structural precondition.  The active environment must name a scope whose
   complete local map contains `l1`, `l2`, `result`, and `item`; `result` must
   refer to heap list `H`; and the computation must be the real
   `#loop` over the remaining `FIRST` values.  It says the loop consumes itself,
   changes the heap list from `ACC` to
   `commonAcc(FIRST, SECOND, ACC)`, and leaves `item` equal to the last iterated
   value (or its old value for an empty remainder).

3. `common-function` starts in the exact pristine semantic configuration,
   loads the `common` definition, and calls it with arbitrary
   `FIRST:ValSeq` and `SECOND:ValSeq`.  It constrains the returned K value to
   `ref(1)`, heap location 0 to the unsorted structural intersection
   `commonSpec(FIRST, SECOND)`, heap location 1 to
   `sortVS(commonSpec(FIRST, SECOND))`, `heapLoc` to 2, the closure binding to
   the exact function body, and all stack/return/exception/exit cells to their
   normal final values.  It is result-constraining, not a tautology or a
   one-way implication.

Satisfiable entry states exist.  For `member-fold`, take `V = 1`,
`VS = vCons(1, .ValSeq)`, `CONT = .K`, and ordinary well-formed framed cells.
For `common-loop`, take `L = 1`, `H = 0`, `FIRST = SECOND =
vCons(1, .ValSeq)`, `ACC = .ValSeq`, `OLD = 0`, the four required local
bindings, the module and builtins frames in the framed scope map, and heap
location 0 containing the empty result list.  For `common-function`, the
claim itself supplies a pristine state for any two `ValSeq`s.  A ground
all-integer witness `FIRST=[3,1,3,2]`, `SECOND=[2,3,2]` gives
`commonSpec=[3,2]` and sorted result `[2,3]`; both Python implementations return
`[2,3]` (`evidence/differential-test.log`).

### Mechanical pinning

The trusted translator regenerated `solution.mpy` byte-for-byte.  Independently,
`kast` parsed both the regenerated `solution.mpy` and
`Module(commonDefinition)` using the fresh proof definition and emitted
canonical KORE.  The KORE files are byte-identical, both with SHA-256
`2efed36c798d24a4b8579dfad30aafef9f12ce6499006ac3ea2b3e35ae5b6cba`;
see `evidence/program-term-pinning.log` and
`evidence/macro-module.mpy`.  Thus the syntax macros are semantically inert
normalization of the actual submitted module; the claim does not substitute a
different function body.

A separate body-sensitivity mutation deletes the `result.append(item)` effect
from the macro term actually executed by the loop claim.  The mutated
definition builds successfully, but the loop proof exits 1 with
`WarnStuckClaimState` and the expected unmet equality between the accumulator
with and without the appended value.  See
`evidence/verification-body-mutation.k`,
`evidence/spec-body-mutation.k`, `evidence/body-mutation-kompile.log`, and
`evidence/body-mutation-kprove.log`.

### Fatal source-semantics mismatch

Real-program pinning requires more than syntactic identity: the fixed semantics
must give each material operation its real behavior.  Here it does not.
`reference-semantics/semantics/list.k:63-66` implements list membership as:

- success only when `E ==K V`; and
- recursion when `notBool (E ==K V)`.

The proof-local `memberVS` equations in `verification.k:34-41` deliberately
repeat the same K-constructor equality, so `member-fold` is sound with respect
to the supplied semantics.  But K constructor equality distinguishes the Bool
constructor `true` from Int `1`, and Int `1` from Float `1.0`; Python equality
does not.

This gives concrete false-conclusion witnesses on the claimed domain:

- `FIRST = vCons(true,.ValSeq)`, `SECOND = vCons(1,.ValSeq)`;
- `FIRST = vCons(1,.ValSeq)`, `SECOND = vCons(1.0,.ValSeq)`.

For both, the K summary reduces to `.ValSeq`.  The fresh K witness specification
proves those reductions with `#Top`
(`evidence/spec-semantic-witness.k`,
`evidence/semantic-summary-witness-kprove.log`).  Fresh LLVM execution of the
exact translated submitted body against assertions for the real Python outputs
exits 1 in both cases, with `<exc> AssertionError`, semantic
`<exit-code> 1`, and an empty computed result heap object
(`evidence/semantic-mismatch-bool.py`,
`evidence/semantic-mismatch-float.py`, their trusted-translator `.mpy` outputs,
and `evidence/semantic-membership-mismatch.log`).  In contrast, both trusted
canonical and submitted Python return the nonempty outputs shown in Stage 2.

The whole-function claim quantifies over arbitrary `ValSeq`s and has no
homogeneous-integer or homogeneous-constructor precondition.  Even if one read
an unstated integer intention into the examples, Python `bool` is an integer
subtype and the prompt provides no exclusion.  The int/float witness is an
additional normally terminating numeric case.  Hence the successful K theorem
does not establish the submitted program's behavior over the material
source-contract domain.

## 5. Rule-by-rule static soundness review

`evidence/rule_inventory.py` generated the exhaustive line-addressed inventory
in `evidence/rule-inventory.txt`.  It contains every declaration and normalized
full rule body from the supplied `semantics.k`, every helper K file,
`verification.k`, and `spec.k`: 235 syntax declarations, 707 rules, 5 contexts,
1 configuration, and 3 claims.  It records all attributes, including 112
`total`, 150 `function`, 25 `symbol`, 22 `no-evaluators`, 45 `priority`, 35
`concrete`, 26 `owise`, 7 `macro`, 1 `macro-rec`, and the 3 proof-local
`simplification` occurrences.  There are no `[functional]` declarations.

The following table is the disposition of every inventoried file.  Full
per-rule text and line locations are in the inventory; the table groups rules
only where they have the same audit disposition.

| File/module | Syntax / rules | Static disposition |
|---|---:|---|
| `semantics.k` (`MPY`, `MPY-KRUN`) | assembly only | Imports exactly the supplied modules; no local equation or bridge. |
| `syntax.k` | 16 / 0 | Grammar declarations. Every constructor in `solution.mpy` is declared; strictness is checked below. |
| `core.k` | 37 / 46 | Configuration, allocation, sequencing, lookup, literals, argument evaluation, truthiness, and sequence helpers. Target-reachable rules preserve the relevant cells and evaluate arguments left-to-right. Unused closure-cell/general helpers do not contribute to closure. |
| `iter.k` | 1 / 0 | Iterator protocol declarations only. |
| `range.k` | 2 / 6 | Unused by this program; guarded structural range equations. |
| `operators.k` | 0 / 10 | Target comparison dispatch and heap dereference preserve order and state, but delegate list membership to the defective `list.k` fold identified below. |
| `int.k` | 1 / 16 | Unused arithmetic/comparison equations apart from the ordinary integer value domain. Division exceptional cases are outside this target path. |
| `bool.k` | 0 / 13 | The target `and` rules correctly short-circuit and return values; guards are complementary. Heap-ref variants preserve object identity. |
| `float.k` | 34 / 121 | Float operators and proof-opaque primitives are unused by the program body. Float values are nevertheless admitted as list elements, which makes the `list.k` equality defect target-reachable. Duplicate mixed arithmetic equations have agreeing right sides. |
| `str.k` | 5 / 28 | Structural string/list iteration equations are unused on the integer witnesses; homogeneous strings behave consistently in differential tests. ASCII-only literal support is a supplied subset limitation, not used to close this proof. |
| `set.k` | 6 / 12 | Unused by the submitted program and proof. |
| `list.k` | 5 / 27 | Literal allocation, iteration, concatenation, and append preserve the exact target heap effect. **Rules 63-66 are not Python-faithful on mixed equal numeric constructors**; the two ground witnesses above show the false result they enable. |
| `tuple.k` | 4 / 21 | The target uses name-target binding from this module; it updates only the current scope as required. Tuple-specific rules are unused. |
| `subscript.k` | 15 / 40 | Unused. `valSeqAt` is declared total without an empty/OOB equation; this is one compiler-reported coverage gap, but it does not contribute to any target claim. |
| `comprehension.k` | 3 / 7 | Unused syntax macros. |
| `methods.k` | 27 / 75 | General string/list methods are unused; target append is intercepted by the specific `list.k` rule. `joinCodes` has a compiler-reported totality gap for non-string elements but is unreachable here. |
| `controls.k` | 3 / 34 | Target assignment, `if`, `for`, and iteration dereference follow the submitted control flow. The snapshot-iteration limitation is inert because `l1` is never mutated. |
| `functions.k` | 4 / 15 | Target function definition, parameter binding, return, frame pop, and heap preservation match the complete call context. No proof-local rule bypasses the body. |
| `builtins.k` | 38 / 137 | Most rules are unused. Name registration and generic routing used by `sorted` are consistent. `mapStrVS` is declared total with uncovered `Val` constructors; compiler warning, no target dependency. |
| `call.k` | 3 / 21 | Target name lookup, callee evaluation, argument evaluation, user-frame creation, append dispatch, and builtin dispatch preserve binding, continuation, stack, heap, and environment. |
| `sort.k` | 6 / 19 | `sorted(list)` allocates a fresh object containing opaque `sortVS(VS)`. This is an explicit result-bearing trusted primitive, not a proof of ascending order. Its ground int/string insertion rules are consistent; arbitrary symbolic `ValSeq` remains opaque. |
| `assert.k` | 0 / 3 | Used only by concrete audit drivers. It correctly exposes the mixed-equality mismatch as `AssertionError`; not imported as a proof shortcut. |
| `dict.k` | 12 / 28 | Unused. |
| `concrete.k` | 5 / 16 | LLVM-only deep-equality/keyed-sort rules; none is in the Haskell proof definition or target path. |
| `verification.k` | 8 / 12 | Three exact body macros plus five total definitional summaries. No operational bridge, oracle, priority rule, or unconstrained fresh value. The equations are terminating and their constructor cases are disjoint/exhaustive. The three `memberVS` simplifications are true for `==K`, but that very definition is inadequate for Python equality. |
| `spec.k` | 0 / 0, 3 claims | Claims are satisfiable and result-constraining; dependencies are proved before being trusted. The whole claim is too broad for the supplied equality model relative to real Python. |

### Used-construct map and evaluation/control audit

The submitted term uses `Module`, `FuncDef`, `Params`, `Assign`, `Name`,
`ListExpr`, `Int`, `For`, `If`, `BoolOp`, `Compare`, `CmpOp`, `Expr`, `Call`,
`Attribute`, and `Return`.  Their syntax is in `syntax.k:9-61`; statement
sequencing/loading and literals are in `core.k:123-127,183-196`; lookup is in
`core.k:129-181`; list construction, iteration, membership, and append are in
`list.k:8-15,52-67`; comparison routing and dereference are in
`operators.k:10-46`; short-circuit `and` is in `bool.k:13-46`; assignment,
branching, and the `for` protocol are in `controls.k:8-74,93-108`; name-target
binding is in `tuple.k:30-41`; function/frame/return behavior is in
`functions.k:13-20,62-91`; uniform call and argument dispatch is in
`call.k:15-74`; and `sorted` allocation is in `sort.k:34-37`.

This route evaluates the callee and arguments left-to-right, binds the selected
closure from the module/builtins scope chain, allocates the result list, reads
both inputs without mutation, updates only the result list during append,
short-circuits the second membership test when the first is false, iterates in
left-to-right order, allocates the sorted result, returns it through the saved
continuation, restores the caller environment, removes the callee scope, and
preserves escaped heap objects.  The successful body mutation probe confirms
the loop circularity depends on the actual append effect.

All 45 priority-bearing entries are listed verbatim in the inventory.  The
target-relevant priorities only select specific heap dereference, mutable
method, and list/control cases over generic dispatch; they do not fabricate a
result or discard an admitted continuation.  There is no candidate-added
priority.

The six fresh totality warnings are coverage defects in unused supplied
helpers.  For example, `mapStrVS(vCons(cellsMark(...), ...))`,
`joinCodes(..., vCons(cellsMark(...), ...))`, and
`valSeqAt(.ValSeq, 0)` have no defining equation despite a `total`
declaration.  I do not label those declarations as target-unsound because no
false target conclusion witness or dependency was found; the narrower finding
is incomplete totality evidence in the fixed, unused semantics.  By contrast,
the membership rules have the required concrete false-result witnesses and are
the basis for the verdict.

## 6. Fresh non-vacuity test

The reviewer-authored `evidence/spec-vacuity.k` retains the two proved helper
claims but changes the whole-function result obligation to require heap
location 1 to contain the empty list for every input.  This is demonstrably
false for the satisfying input `FIRST=[1]`, `SECOND=[1]`, on which both Python
implementations return `[1]`.

The dry-run command successfully parsed and built the mutated specification:

```text
kprove spec-vacuity.k --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.member-fold,SPEC-VACUITY.common-loop,SPEC-VACUITY.common-function-false-empty \
  --trusted SPEC-VACUITY.member-fold,SPEC-VACUITY.common-loop --dry-run
```

It exited 0 (`evidence/vacuity-dry-run.log`).  Running the same target without
`--dry-run` exited 1 with `WarnStuckClaimState`.  The residual is the expected
unmet result equality
`.ValSeq == sortVS(commonAcc(FIRST, SECOND, .ValSeq))`, not a parser failure,
timeout, missing import, or unrelated crash
(`evidence/vacuity-kprove.log`).  The original proof is therefore
discriminating and non-vacuous.

## 7. Proven versus assumed accounting

### What the successful K reachability proof actually establishes

Under the supplied K theory, for arbitrary algebraic `ValSeq` inputs and normal
symbolic execution, the exact submitted constructor term scans `FIRST`,
retains values that are `==K`-identical to a value in `SECOND`, suppresses later
`==K`-identical duplicates, allocates a fresh list containing that sequence,
allocates a second fresh list containing the opaque term `sortVS` applied to
that sequence, and returns the second reference with the exact final cells in
`common-function`.  It also independently establishes the supplied structural
membership fold and the loop circularity.  This is a genuine partial-correctness
theorem about the supplied K model.

It does **not** establish that the same term implements Python common-element
semantics for all source-contract inputs.  The mixed bool/int and int/float
witnesses refute that bridge.  It also does not prove a mathematical ordering
or permutation theorem for `sortVS`, and it does not prove termination (the
Kit's theorem class is partial correctness).

### Trust ledger

- **Fixed operational semantics.**  All target execution rules listed in
  Stage 5 are assumed to model Python.  This boundary is illegitimate for the
  target membership operation because `list.k:63-66` demonstrably disagrees
  with normally terminating Python executions.  Every positive claim depends
  on that fold directly or through the loop/function claims.

- **Proof-local summaries.**  `memberVS`, `shouldAdd`, `commonAcc`,
  `commonSpec`, and `lastAfter` are terminating, exhaustive definitional
  summaries.  They introduce no unconstrained value.  `memberVS` is connected
  universally to the supplied fold by the separately proved `member-fold`
  claim, but its `==K` meaning makes `commonAcc/commonSpec` a structural
  intersection rather than Python's equality-based intersection.  Thus the
  connection theorem is internally sound but inadequate for the real program.

- **Opaque result-bearing `sortVS`.**  `sortVS` is a fixed-semantics external
  primitive declared `[function,total,symbol,no-evaluators]`; its concrete
  insertion equations cover ground int and string lists.  The target proof
  returns the term parametrically and does not use an ordering lemma.  Treating
  that term as real ascending `sorted` is conditional on the named external
  contract and finite differential evidence.  This would be a non-fatal trust
  limitation by itself, but it cannot repair the membership counterexample.

- **Other opaque symbols.**  The complete unused opaque/symbol inventory is:
  `md5hexCodes`; `sortKeyVS`; `intFloatDiv`, `divII`, `floatMod`,
  `floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`,
  `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`,
  `truncF`, `roundF`, `roundFN`, and `sqrtF`.  None except `sortVS`
  contributes to the target claims.  Their concrete equations or external
  contracts therefore supply no evidence for the target result.

- **K mathematical/data primitives.**  K Int/Bool/String, Boolean operators,
  maps, lists, and `==K` are trusted low-level primitives.  Their algebraic
  behavior is acceptable; using `==K` as Python element equality is the
  illegitimate higher-level step exposed above.

- **Input representation.**  The entry claim passes read-only input lists as
  unboxed semantic `list(ValSeq)` values rather than allocating them from
  source literals.  Because this function only reads those inputs and the fixed
  `For`/membership rules operate on the same structures, this representation
  bridge is acceptable for the target path.  Concrete source-level execution
  and all-integer differential tests support it but do not prove it
  universally.

- **Source-to-term identity.**  Trusted regeneration plus canonical KORE
  equality proves the syntax-macro term is the submitted program.  The
  body-sensitivity mutation confirms that changing the executed body changes
  the proof obligation.

- **Claim dependencies.**  `member-fold` and `common-loop` are trusted only
  after separate successful `kprove` runs.  This is an acceptable modular
  proof dependency, not an assumption imported from candidate prose.

- **Empirical evidence.**  The 11,600-plus Python differential cases and the
  four original LLVM smoke cases support the ordinary homogeneous-integer
  bridge only finitely.  The two adversarial mixed-numeric executions are
  counterexamples to the unrestricted bridge.  Neither testing set substitutes
  for the K proof.

Kit gate accounting: fresh verification closure passes; non-vacuity and body
sensitivity pass; source-to-term pinning passes.  Real-program soundness and
intent adequacy fail because a target-reachable equality rule yields false
Python results on satisfying contract inputs.  Evidence auditability passes,
but later evidence cannot cure that material semantic/domain failure.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
