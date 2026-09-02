# Independent adversarial audit: 87-get-row

The candidate is not a legitimate proof of the submitted program. Fresh
reconstruction does produce `#Top`, the Python implementation is faithful to
the canonical implementation on substantial differential evidence, the
proof-local `addMatch` equations are sound, and the submitted claims are
non-vacuous. Those positive facts do not cure two material adequacy failures:

1. The claims never load or execute `solution.mpy`. They install
   `getRowClosure`, whose body is a duplicate written in `verification.k`.
   With the active scratch `solution.mpy` materially changed to
   `Return(Int(999))`, a fresh proof build and the submitted spec still close
   with `#Top`. Thus the K theorem is insensitive to the real submitted
   program and proves a substituted closure.
2. The only input shapes proved are the empty outer list and exactly
   `[[], [A], [B,C,D]]`. The natural-language domain is arbitrary finite
   ragged nested lists. Even the first documented example, whose three rows
   each have length six, is outside both formal entry claims.

No candidate-local rule is labeled mathematically unsound in this review. The
failure is real-program pinning and material under-specification, for which a
false-rule witness is neither needed nor claimed.

The complete command/status index is
[`evidence/COMMANDS.md`](evidence/COMMANDS.md). The exhaustive lexical K
inventory is [`evidence/14_rule_inventory.md`](evidence/14_rule_inventory.md).

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. There is therefore no
infrastructure contradiction and the audit proceeds to a candidate verdict.

The reviewer recursively compared the candidate tree with the trusted tree
using `diff --no-dereference -r`. Every directory and file is a regular entry
of the same type and content; there are no missing, additional, changed,
mistyped, or symlinked entries under the candidate
`reference-semantics/`. The candidate's `prompt.py` and `py2mpy.py` are also
byte-identical to `/reference/prompt.py` and `/reference/py2mpy.py`.
See [`evidence/01_provenance_check.sh`](evidence/01_provenance_check.sh) and
[`evidence/01_provenance_check.log`](evidence/01_provenance_check.log).

This identity establishes only integrity of the supplied baseline. It does not
bless the candidate-local rules in `verification.k`, which are reviewed
separately below.

### Missing and untrusted generation records

The following requested generation artifacts are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured trace or trace-like JSONL artifact is present. There is also no
candidate `PROOF.md` or `spec-vacuity.k`. The available `prove.log`,
`prove.sh`, concrete tests, bytecode cache, and other candidate files were read
only as untrusted claims. No candidate-compiled definition or cache was copied
or reused. These provenance omissions reduce auditability but are not an
infrastructure breach, and independent reconstruction below does not rely on
them.

The candidate source hashes and full entry-type inventories are in the stage-1
log. The reviewer scratch tree was populated only with the candidate source
program/spec/proof files, the trusted translator/canonical/prompt, and a fresh
copy of the trusted supplied semantics.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a finite list of finite rows and integer target `x`, return every coordinate
whose element equals `x`. Coordinates are zero-based `(row, column)` tuples.
Rows must occur in ascending order, and matching columns within each row must
occur in descending order. Empty inputs and empty rows are allowed.

The trusted canonical implementation constructs all matching coordinates,
stably sorts first by descending column and then by ascending row, and returns
the resulting list.

### Submitted implementation

`solution.py` is a different but faithful algorithm:

- `enumerate(lst)` visits rows in ascending index order;
- `range(len(row) - 1, -1, -1)` visits every valid column in descending order;
- the equality branch appends exactly `(row_index, column_index)`;
- the result is returned without a later reorder.

This directly implements the required ordering for arbitrary finite ragged
integer lists.

Trusted retranslation produced a byte-identical `solution.mpy`; both files
have SHA-256
`77095066c6cb51ab5f0c562830989906ecdc63f76b1d00d6cc3b74b88f7ac63f`.
See
[`evidence/02_retranslation_check.sh`](evidence/02_retranslation_check.sh),
[`evidence/02_retranslation_check.log`](evidence/02_retranslation_check.log),
and
[`evidence/solution.regenerated.mpy`](evidence/solution.regenerated.mpy).

### Independent differential execution

The reviewer-authored script imports the trusted entry point directly from
`/reference/canonical.py` and the generated entry point from the isolated
scratch copy of `solution.py`. It checks:

- all three documented examples;
- zero rows, one or several empty rows, no-match and match cases;
- the first, middle, and last column boundaries;
- repeated matches and descending-column order;
- negative and arbitrarily large integers;
- every matrix of zero to three rows where each row has length zero to two and
  elements in `{-1,0,1}`, for targets `{-2,-1,0,1,2}`;
- 2,000 deterministic larger ragged random inputs.

The run covered 14 named cases, 11,900 exhaustive small cases, and 2,000
larger generated cases: 13,914 total with zero mismatches. See
[`evidence/03_differential_test.py`](evidence/03_differential_test.py) and
[`evidence/03_differential_test.log`](evidence/03_differential_test.log).
This is strong finite evidence that the Python program implements the
contract; it is not a substitute for a K reachability theorem.

## 3. Clean proof reconstruction

The live toolchain is K 7.1.337 and Python 3.10.12
([`evidence/00_toolchain.log`](evidence/00_toolchain.log)).

All definitions were built from source under
`/tmp/audit-work/87-get-row`. No candidate build directory existed in that
copy. The selected source semantics was the fresh trusted
`reference-semantics` copy.

### Concrete definition

The reviewer translated an independently authored smoke program and built:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled
```

The build exited 0. `krun reviewer-concrete-tests.mpy --definition
reviewer-runtime-kompiled` also exited 0 and reached `.K`, `NoExc`, and
`<exit-code> 0</exit-code>` on empty, no-match, one-match, and repeated/ragged
boundary cases. See
[`evidence/04_concrete_translate.log`](evidence/04_concrete_translate.log),
[`evidence/05_llvm_build.log`](evidence/05_llvm_build.log),
[`evidence/06_k_concrete_run.log`](evidence/06_k_concrete_run.log), and the
preserved reviewer sources beside them.

The LLVM compiler reported fixed-baseline non-exhaustive-totality warnings for
such operations as `mapStrVS`, float helpers, `joinCodes`, and an out-of-bounds
`valSeqAt` case. None is reached by this program on the exact valid claim
shapes. They are recorded as baseline limitations, not mislabeled as candidate
unsoundness without a false-conclusion witness.

### Proof definition and every positive claim

The fresh proof build was:

```text
kompile verification.k --backend haskell \
  --main-module GET-ROW-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled
```

It exited 0. A reviewer copy of `spec.k` added only inert labels so the two
claims could be selected independently:

- `--claims empty`: exit 0, `#Top`;
- `--claims ragged`: exit 0, `#Top`.

The original, unmodified submitted `spec.k` was then proved as a whole: exit 0,
`#Top`. The first attempted qualified selector
`GET-ROW-SPEC.empty` exited 113 because this K version expects the bare label;
that auditor invocation error is retained transparently and was corrected. It
is not a candidate failure. See
[`evidence/07_haskell_build.log`](evidence/07_haskell_build.log),
[`evidence/08_prove_empty.log`](evidence/08_prove_empty.log),
[`evidence/08b_prove_empty.log`](evidence/08b_prove_empty.log),
[`evidence/09_prove_ragged.log`](evidence/09_prove_ragged.log), and
[`evidence/10_prove_submitted_spec.log`](evidence/10_prove_submitted_spec.log).

Thus the dynamic reconstruction gate succeeds: the claims really do close
under the supplied semantics plus the candidate proof extensions. That fact
alone does not establish real-program pinning or intent adequacy.

## 4. Adequacy and real-program pinning

### Entry claim 1: empty outer list

The first claim has no explicit `requires` clause. Sorts constrain `X` to an
integer. Its exact pre-state is:

- current environment 0;
- module scope maps `"get_row"` to `getRowClosure`, with the supplied builtins
  scope as parent;
- empty heap, heap allocator 0, empty call stack, `noRet`, `NoExc`, exit code
  0;
- call argument is the bare value `list(.ValSeq)`.

It says that, if the modeled call terminates, it returns `ref(0)`, where heap
location 0 is an empty result list and location 1 is the empty list allocated
by eager `enumerate`; the allocator advances to 2 and the other visible cells
are restored.

A satisfying witness is `X = 7` with the cells exactly as written. The claimed
result is `[]`, equal to both Python implementations.

### Entry claim 2: one fixed ragged shape

Again there is no explicit `requires`; the K sorts require
`A,B,C,D,X` to be integers. The outer value is exactly a three-row list of
references:

- row 0 is `[]`;
- row 1 is `[A]`;
- row 2 is `[B,C,D]`;
- the only pre-existing heap locations are 0, 1, and 2; the allocator begins
  at 3; other control cells match the first claim.

It says that the call returns `ref(3)`. Heap location 3 contains:

```text
addMatch(A,X,1,0,
  addMatch(D,X,2,2,
    addMatch(C,X,2,1,
      addMatch(B,X,2,0,.ValSeq))))
```

Location 4 is the eagerly materialized enumeration list; the input rows are
preserved and the allocator advances to 5. This postcondition is
result-constraining for that shape, and it encodes row order 1 then 2 with
columns 2, 1, 0 in row 2.

A satisfying mixed witness is
`A=5, B=9, C=5, D=5, X=5`, corresponding to
`[[],[5],[9,5,5]]`. The claimed and both Python results are
`[(1,0),(2,2),(2,1)]`. No-match and all-match substitutions also agree. See
[`evidence/11_claim_ground_witnesses.py`](evidence/11_claim_ground_witnesses.py)
and
[`evidence/11_claim_ground_witnesses.log`](evidence/11_claim_ground_witnesses.log).

### The claims do not execute `solution.mpy`

The `<k>` cells start at a direct `Call`. The scope already binds `"get_row"`
to the proof-local constant `getRowClosure`. `verification.k` expands that
constant to:

```text
closureVal(("lst","x",.ParamNames), getRowBody, 0)
```

and separately expands `getRowBody` to a hand-copied AST. Neither
`verification.k` nor `spec.k` requires, parses, or loads `solution.mpy`. The
claims never execute the submitted `Module(FuncDef(...))` or derive the
function binding through the supplied `#loadAll`/`FuncDef` rules. The copied
body is textually faithful to the current submission, but this is an informal
comparison, not real-program execution or a machine-checked connection claim.

The reviewer performed a body-sensitivity test:

1. Preserve the submitted `solution.mpy`.
2. Put a materially different artifact at the active scratch path, changing
   the function's final statement to `Return(Int(999))`.
3. Hash that active file.
4. Rebuild the Haskell proof definition from scratch.
5. Prove the submitted `spec.k`.

The active mutant had SHA-256
`d3f36c7b41f9c9541044aa8f6e82a28ed47babf69679eca226ba66c9103af855`.
The build exited 0 and the proof still exited 0 with `#Top`. An independent
Python and K concrete program executes that mutation as the value 999. The
self-contained evidence is
[`evidence/13b_body_sensitivity.sh`](evidence/13b_body_sensitivity.sh) and
[`evidence/13b_body_sensitivity.log`](evidence/13b_body_sensitivity.log);
the original and mutant files are
[`evidence/solution.original.mpy`](evidence/solution.original.mpy) and
[`evidence/solution.body-mutant.mpy`](evidence/solution.body-mutant.mpy).
Concrete mutation execution is in
[`evidence/13a_body_mutant_concrete_run.log`](evidence/13a_body_mutant_concrete_run.log).

This is a direct program-identity failure: a material body change does not
invalidate or alter the K proof because the submitted program is not an input
to that proof.

### Material domain gap

There are no helper or loop-invariant claims. The two fixed finite input shapes
are simply unrolled by symbolic execution. No claim accepts an arbitrary outer
`ValSeq` or arbitrary row `ValSeq`s.

For example, `[[1]]` with `x=1` is in the intended domain and both Python
implementations return `[(0,0)]`, but neither entry precondition accepts that
heap shape. More starkly, the prompt's first documented example has row lengths
six, six, and six and lies outside both formal claims. Differential tests show
the submitted implementation handles these cases; the K proof does not.

Consequently the proof both substitutes the executable body and omits most of
the stated input domain. These are material adequacy failures, not merely thin
empirical bridges.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer lexically inventoried all 24 supplied K files plus
`verification.k` and `spec.k`, preserving normalized full rule blocks,
guards, attributes, source lines, origin, and an audit disposition. The final
inventory contains:

- 1,108 declarations total;
- 699 `rule` blocks;
- 230 syntax declarations;
- 5 explicit contexts and 1 configuration;
- 45 priority rules (`priority(39)`, `priority(40)`, or `priority(45)`);
- 148 function declarations, 108 `total` declarations, 35 `concrete`
  attributes, and 22 `no-evaluators` declarations;
- zero local `functional` and zero local `simplification` attributes/rules.

The complete 261 KB inventory, rather than a selective excerpt, is
[`evidence/14_rule_inventory.md`](evidence/14_rule_inventory.md), generated by
[`evidence/14_static_inventory.py`](evidence/14_static_inventory.py). Its
SHA-256 is
`60beac214e5f9ecc3cdd8e5f38f3a9219d1fa6d64da300797bf62a7522e56f69`.

Every supplied rule is classified as fixed-baseline and candidate-identical.
Rules that cannot occur on this program's execution path are marked
`imported-unused`; this does not silently promote them to proof-specific
lemmas. All rules and declarations on the used path were then reviewed as
follows.

### Used-construct map and operational behavior

| Submitted construct | Declaration/rule route | Static conclusion |
|---|---|---|
| `Module`, `FuncDef` | `syntax.k`, `core.k` `#loadAll`, `functions.k` `FuncDef` | These are the correct fixed-semantics loading rules, but the entry claims bypass them; this is the pinning failure above. |
| Function call and names | `core.k` `#look`, `#evalArgs`; `call.k` `#callee`, `toCall`, closure dispatch; `functions.k` binding/return/pop | Callee then arguments evaluate left-to-right, params bind in a fresh scope, return value and caller environment are restored. The surrogate closure follows these rules. |
| `result = []` | `syntax.k` strict assignment; `list.k` `ListExpr`/`toList`; `core.k` `#alloc`; `controls.k` name assignment | Allocates the result before enumeration at heap 0 or 3, matching both post-heaps. |
| Outer `for ... in enumerate(lst)` | `builtins.k` eager `enumerate`/`enumVS`; `controls.k` `For/#loop`; `iter.k`; `list.k`; `tuple.k` target unpacking | Enumerates rows in ascending order, allocates the temporary list at heap 1 or 4, and binds `(row_index,row)` correctly. |
| `len(row)-1`, `-1`, `-1` | `call.k`, `builtins.k` `len/seqLen`, `operators.k`, `int.k` subtraction/unary minus | Computes the last valid index, stop -1, and step -1 over integer rows. |
| Inner `range` and loop | `builtins.k` range dispatch; `range.k` `inRange` and `#iterNext`; `controls.k` loop rules | For a row of length `n`, yields exactly `n-1,...,0`; empty rows yield nothing. Step zero is excluded and never constructed. |
| `row[column_index]` | `subscript.k` dereference, `normIdx`, `applyIndex`, `valSeqAt`; `core.k` `vsLen` | Every generated index is in bounds on the exact finite row shapes, so the partially total out-of-bounds case is not reached. |
| Integer equality and `if` | `operators.k` comparison contexts/dispatch; `int.k` equality; `controls.k` `#branch` | Each matching integer takes exactly the append branch. Guards and evaluation order agree with the Python subset. |
| `result.append((row,column))` | `call.k` attribute/bound-method routing; `tuple.k` construction; `list.k` priority-40 append rule | The tuple is built left-to-right and appended in place to the allocated result; returned `noneV` is discarded by the expression-statement rule. |
| `return result` | name lookup plus `functions.k` `Return/#pop` | Returns the result reference and restores stack, environment, scope allocator, return, and exception cells as claimed. |

The relevant priority rules only preempt generic dispatch to preserve heap
dereference, allocation, or mutating-method behavior. Their guards are
consistent with the used concrete/symbolic shapes. Allocation is monotonic in
`heapLoc`; input rows are read but not mutated; the only observable mutation is
append to the newly allocated result. No used rule introduces an opaque result,
oracle, exception shortcut, abrupt control bridge, or fabricated coordinate.

On the used path, guarded pairs are disjoint and covering: empty/cons iterator
rules cover each concrete `ValSeq`; `inRange` and its negation cover each
nonzero-step range state; true/false branch rules cover the integer-equality
result; and integer equality/disequality partition every symbolic match.
`enumVS`, `vsLen`, `vals2valSeq`, and `valSeqConcat` structurally descend.
`valSeqAt` is only partially equational despite `[total]`, but every reached
index is generated from the row length and is in bounds, so its residual
totalization is never used. There are no local simplification rules whose
orientation or overlap could change this execution.

### Candidate-local extension inventory

`verification.k` adds exactly three syntax symbols and four equations:

1. `getRowBody : Stmts [function]` and its one unconditional equation. The
   equation terminates in one step and faithfully restates the current
   generated body AST. It does not intercept a running source term. Its defect
   is adequacy: it is a surrogate not connected to the actual `solution.mpy`
   module by any reachability theorem.
2. `getRowClosure : Val [function]` and its one unconditional equation. It
   constructs the copied two-parameter closure at module scope 0. There is no
   overlap or recursion. Again, it bypasses rather than derives the submitted
   program binding.
3. `addMatch(Int,Int,Int,Int,ValSeq) : ValSeq [function,total]` with two
   equations. On integers, `V ==Int X` and `V =/=Int X` are disjoint and
   exhaustive. The matching rule prepends exactly `(R,C)` and the nonmatching
   rule returns `REST`. It is a truthful, terminating definitional summary
   used only in the postcondition; it does not replace program execution and
   is not an unconstrained oracle.

There are no candidate-local priority, concrete, opaque, simplification, or
functional declarations, and no candidate operational interception of
`Call`, loop, append, subscript, or return.

Accordingly, this audit does **not** allege an unsound `addMatch` or fixed
semantic rule. The body-sensitivity witness establishes a missing real-program
connection, not a false equation in the supplied semantics.

## 6. Fresh non-vacuity test

The reviewer created a new module, not the candidate's absent vacuity artifact.
For the satisfiable empty-input claim it changes the result heap at location 0
from `[]` to the deliberately false `[(0,0)]`, while retaining the actual
return reference and all other obligations. `X=7` is a concrete satisfying
witness and the false result is demonstrably wrong in both Python
implementations.

The exact mutation is
[`evidence/spec-vacuity.k`](evidence/spec-vacuity.k).

First:

```text
kprove spec-vacuity.k --definition reviewer-verification-kompiled \
  --spec-module GET-ROW-SPEC-VACUITY --dry-run
```

exited 0, confirming the mutation parses and builds. The real proof command
then exited 1 with `WarnStuckClaimState`, not a parser error, missing import,
timeout, or unrelated crash. Its residual has `<k> ref(0) ~> .K </k>` and the
actual heap:

```text
0 |-> list(.ValSeq)
1 |-> list(.ValSeq)
```

which cannot unify with the mutated nonempty result. See
[`evidence/15_vacuity_dry_run.log`](evidence/15_vacuity_dry_run.log) and
[`evidence/16_vacuity_proof_failure.log`](evidence/16_vacuity_proof_failure.log).
The claims therefore genuinely constrain their results on the two stated
shapes. Non-vacuity does not repair the program-identity or domain failures.

## 7. Proven versus assumed accounting and decision

### What the successful reachability proof establishes

Under the exact supplied MPY semantics and candidate-local definitions, the
successful proof establishes partial correctness of the **proof-local copied
closure** for:

- every integer target on the empty bare list, with the exact return,
  allocation, stack, environment, exception, and exit-code post-state in claim
  1; and
- every five integers `A,B,C,D,X` on exactly `[[],[A],[B,C,D]]`, with the
  exact `addMatch` result and post-state in claim 2.

There is no general loop invariant or arbitrary-list theorem. The proof does
not establish canonical equivalence, the natural-language contract for all
ragged lists, or any property of the parsed `solution.mpy` module.

### Trust ledger

- **Trusted supplied semantics:** all 24 files in
  `/reference/reference-semantics`, exactly matched by the candidate tree.
  This is the selected language model, not a candidate conclusion. Used rules
  were reviewed above; unused rules do not contribute to these executions.
- **K/toolchain primitives:** K's Int/Bool/String/Map/List/equality hooks,
  generated heating/cooling from strictness attributes, the Haskell
  reachability backend, and its arithmetic/SMT reasoning. These are ordinary
  low-level verification trust boundaries and are acceptable for this audit.
- **Imported opaque or proof-opaque symbols:** `intFloatDiv`, `divII`,
  `floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`,
  `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
  `roundFN`, `sqrtF`, `md5hexCodes`, `sortVS`, `sortKeyVS`, plus the
  concrete-only symbolic helpers `floorFI`, `toF`, and `ceilF`. All are visible
  in the exhaustive inventory. None occurs in `solution.mpy`, either claim,
  either result, or any reachable control branch here, so none bears the
  theorem's result.
- **Partially specified totals in the baseline:** in particular
  out-of-bounds/opaque `valSeqAt` and compiler-warned unused functions. The
  range construction keeps every used list index in bounds for both exact
  claim shapes; these boundaries do not influence the proved results. No
  broader claim is inferred from them.
- **`addMatch`:** not assumed or opaque. Its exhaustive equations
  mathematically define the postcondition value.
- **Copied-program bridge:** equality between `getRowBody` and the submitted
  program is only a textual, reviewer-observed bridge. It has no bridge-free
  connection claim and fails body sensitivity: the proof remains `#Top` after
  a material submitted-body mutation. Because this bridge determines the
  entire returned value and control flow, it is illegitimate for claiming a
  theorem about the real submitted program.
- **Intent/canonical bridge:** the contract reading and 13,914-case
  differential run are independent finite evidence that `solution.py` is
  correct. They neither universally prove canonical equivalence nor connect
  `solution.mpy` to the K entry claims.
- **Termination:** the report makes only the requested partial-correctness
  claim. It does not silently promote the reachability result to a universal
  termination theorem.

### Decision

Fresh verification, proof-local rule soundness, and non-vacuity all pass for
the theorem actually written. Real-program pinning fails decisively, and intent
adequacy fails materially. The explicit decision boundary classifies a proof
of a substituted program as not legitimate. The fixed-shape claims also omit
most intended inputs, including a documented example. These are candidate
failures, not audit infrastructure uncertainty.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
