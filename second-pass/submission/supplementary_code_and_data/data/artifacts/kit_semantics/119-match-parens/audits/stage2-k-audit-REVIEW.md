# Independent adversarial review: 119-match-parens

This review treats every candidate artifact and generation record as untrusted
evidence. All executable work was performed from source in
`/tmp/audit-work/119-match-parens`; no candidate-provided kompiled definition or
cache was copied or used. Reviewer scripts, mutations, exact commands, and
bounded logs are in `/audit-output/evidence/`.

## 1. Input and provenance integrity

### Record layout and required records

`/audit-input.json` declares:

- `record_layout`: `pipeline-v3`
- problem: `119-match-parens`
- condition: `kit-semantics`
- semantics mode: `SUPPLIED_SEMANTICS`
- candidate mount: `/candidate`
- trusted mounts under `/reference`
- generation records under `/generation-evidence`

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, all seven required generation-evidence
files, `codex-last.txt`, `codex-output.log`, `prompt.txt`, and all 643 JSONL
events in the structured trace. Every required pipeline-v3 record and
launcher-declared mount was present, readable, of the expected file/directory
kind, and not a symlink.

The generation records were used only as claims. They describe a successful
OOM-resume generation invocation and claim prior validation, `#Top`, concrete
execution, and differential success. None of those claims was used in place of
fresh reconstruction.

`/audit-campaign-lock.json` is exactly equal as parsed JSON to the
`audit_campaign` block in `/audit-input.json`. Its independently computed SHA-256
is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
which equals the recorded lock hash. The run, task, stage result, invocation,
metrics, runtime metrics, usage, prompt, Codex output, last message, and trace
file hashes also equal their recorded values. The stage-result output map was
checked against the actual mounted evidence files. See
`evidence/stage1_provenance.log` and the reviewer source
`evidence/provenance_check.py`.

The generation run records a generation-time Kit commit different from the
audit campaign's Kit commit. These are distinct generation and audit records;
the audit lock agrees exactly with the launcher-owned audit campaign block, so
this is not a campaign-lock contradiction.

### Trusted/candidate input identity

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- The required trusted tree `/reference/reference-semantics` exists, as required
  in supplied-semantics mode.
- A recursive comparison of `/candidate/reference-semantics` and
  `/reference/reference-semantics` found exactly the same relative paths, entry
  types, and file bytes. Neither tree contains a symlink, and the candidate has
  no missing or additional entry.
- A reviewer-defined digest over entry kind, relative path, and file bytes is
  `8d947df4087bd37db19499d947a635cb87a6d71158349d2325492fd976158872`
  for each semantics tree.

There is no provenance or semantics-mode infrastructure breach. Stage 1 passes.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt requires a list containing exactly two strings, each made
only of `(` and `)`. The function must return `Yes` iff one of the two possible
concatenation orders is a balanced-parentheses string, and `No` otherwise.
There is no stated length bound.

The trusted canonical implementation tests both concatenations with the usual
running-depth criterion: depth must never become negative and must end at zero.

The generated `solution.py` uses a different but equivalent implementation. It
scans the first order, maintaining the final balance and minimum prefix balance,
returns `Yes` when the final balance is zero and the minimum is nonnegative,
then repeats from fresh local state for the other order and otherwise returns
`No`. Its `else` branch decrements for every non-`(` character, but the source
contract and formal precondition restrict characters to `(` and `)`, so this
does not narrow or alter the intended domain.

### Trusted regeneration

In scratch I ran:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp solution.regenerated.mpy solution.submitted.mpy
```

Both commands exited zero. The submitted and regenerated MPY files have the
same SHA-256:
`002e09688dd1147a9fbf1d96a609099902188fee759cb8d41ef8d9ac9775f4ed`.
See `evidence/stage2_translation.log`.

### Independent differential test

`evidence/differential_audit.py` imports the trusted canonical function from
`/reference/canonical.py` and the generated function from the scratch copy. It
tests:

- both prompt examples;
- both empty strings;
- success only in the first concatenation order;
- success only in the second order;
- success in both orders;
- positive and negative nonzero final balances;
- total balance zero but a bad prefix in both orders;
- one empty component on either side;
- a deeper boundary case; and
- every pair of parenthesis strings whose combined length is at most 10.

The result was 20,481 exhaustive generated pairs, including 1,078 `Yes` and
19,403 `No` outcomes, with zero canonical/generated mismatches. The command
exited zero. This is finite fidelity evidence, not a replacement for the K
proof. See `evidence/stage2_differential.log`.

Stage 2 passes.

## 3. Clean proof reconstruction

Only these sources were copied to scratch: candidate `solution.py`,
`solution.mpy`, `spec.k`, and `verification.k`; trusted `py2mpy.py`, prompt,
canonical solution, and the trusted supplied-semantics tree. Candidate
`runtime-kompiled`, `verification-kompiled`, `__pycache__`, logs, and other
caches were not copied.

The independently installed tools report K 7.1.293. The paths and versions are
recorded in `evidence/stage3_toolchain.log`.

### Fresh definitions

The concrete definition was rebuilt with:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled
```

It exited zero. The warnings concern supplied-semantics declarations whose
declared total domains are broader than their equations
(`mapStrVS`, float conversions, `joinCodes`, and `valSeqAt`) and unused `strLt`
variables. The current program reaches none of the incomplete cases:
`valSeqAt` is reached only at indices 0 and 1 of the formal two-element input.
See `evidence/stage3_kompile_llvm.log`.

The proof definition was rebuilt with:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition proof-kompiled
```

It exited zero; its only compiler warnings are unused pattern tails in the
trusted `strLt` equations. See `evidence/stage3_kompile_haskell.log`.

### Fresh concrete execution

`evidence/concrete_harness.py` contains the generated function plus seven
assertions covering both result branches, each order-specific success branch,
empty input, bad-prefix input, and a deeper input. An AST comparison established
that the harness function is exactly the scratch `solution.py` function before
translation. Trusted translation and:

```text
krun concrete_harness.mpy --definition concrete-kompiled --output json \
  | python3 check_krun_json.py
```

exited zero with an empty final `<k>` cell, `NoExc`, and exit code 0. See
`evidence/stage3_harness_identity.log` and
`evidence/stage3_concrete_krun.log`.

### Positive claims

The spec has two auxiliary loop claims and one entry claim. I ran:

```text
kprove spec.k --definition proof-kompiled --spec-module SPEC \
  --claims SPEC.loop-first
kprove spec.k --definition proof-kompiled --spec-module SPEC \
  --claims SPEC.loop-second
kprove spec.k --definition proof-kompiled --spec-module SPEC
```

Each command exited zero and printed `#Top`. The focused runs establish each
loop claim independently. The full run proves the entry claim with both loop
circularities available and also reproves all claims together. Exact bounded
outputs are in:

- `evidence/stage3_kprove_loop_first.log`
- `evidence/stage3_kprove_loop_second.log`
- `evidence/stage3_kprove_full.log`

Stage 3 passes.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.loop-first` and `SPEC.loop-second` have no explicit `requires` clause.
Each begins at the real internal `#loop` term over an arbitrary string code
sequence `CS`, with the exact two-statement source loop body. The current scope
contains exactly the parameter/local names present at either real loop head.
The claim consumes the loop, preserves `lst`, `text`, the parent scope and
framed configuration, and changes:

- `balance` from `B` to `scanBalance(CS, B)`;
- `minimum` from `M` to `scanMinimum(CS, B, M)`; and
- `char` from `OLD` to `scanLast(CS, OLD)`.

The loop claims accept an arbitrary continuation after the loop. This is sound
for the exact body: it contains no return, exception, break, heap allocation, or
other abrupt control effect, and the successful fixed-semantics proof preserves
the continuation while updating exactly those three locals. The two claims are
textually duplicate obligations for the two identical source loops; either
matches the corresponding real loop state.

`SPEC.match-parens` starts with an actual call to `match_parens` on a
two-element `list` value containing strings with code sequences `A` and `B`.
The precondition `parenCodes(A) andBool parenCodes(B)` means every code is 40
(`(`) or 41 (`)`) and imposes no length bound. The complete caller environment,
module/builtins scopes, fresh scope/heap locations, empty heap/stack,
return/exception state, and exit code are pinned.

Its result is existential only as the reached value, then is constrained by:

```text
ensures ?RESULT ==K matchAnswer(A, B)
```

`matchAnswer` is `Yes` exactly when `goodParens(A+B)` or `goodParens(B+A)`,
where `goodParens` requires final balance zero and minimum prefix balance
nonnegative. Otherwise it is `No`. This is an equality, not a tautology or
one-way implication.

### Mechanical program identity

`evidence/program_pinning_check.py` parses the trusted regenerated MPY term and
the entry claim's closure into constructor trees. It checks:

- the module binding is `"match_parens" |-> closureVal`;
- the parameter binding is exactly `"lst"` with defining scope 0;
- every function-body constructor and argument is equal; and
- the only normalization is an explicit `.Stmts` token versus the translator's
  empty statement-list argument.

The normalized bodies contain 177 constructor nodes and have identical digest
`fde5b4790106234deddd85537599340265c7440f4083565921234498b6b00f18`.
This is the actual closure executed by the claim, not a detached source file.
See `evidence/stage4_program_pinning.log`.

The entry term starts at the function call rather than reloading the submitted
`Module(FuncDef(...))`. That is an allowed normalization here: the scope
contains the same function name, parameter, defining environment and exact
trusted-regenerated body that the supplied `FuncDef` rule would install. Name
lookup, argument evaluation/binding, frame creation, the entire body, both
loops and branches, returns, and frame popping still execute under fixed
semantics.

### Satisfying states and ground substitutions

`evidence/claim_witnesses.py` supplies three ground substitutions:

- `A=.IntSeq`, `B=.IntSeq`: precondition true, `matchAnswer=Yes`;
- `A=(41)`, `B=(40)`: precondition true, only the second order is good,
  `matchAnswer=Yes`;
- `A=(41)`, `B=(41)`: precondition true, both orders bad,
  `matchAnswer=No`.

For each, the claimed result equals both the trusted canonical and generated
Python results. Thus the entry precondition is satisfiable and both result
branches are grounded. See `evidence/stage4_claim_witnesses.log`.

### Body sensitivity

A reviewer mutation changed the actual closure's final
`Return(Str("No"))` constructor to `Return(Str("Yes"))`; it did not merely edit
an external source file. The changed file and exact diff are
`evidence/spec_body_mutation_review.k` and
`evidence/stage4_body_mutation_diff.log`.

The mutated spec parsed but `kprove` exited 1 with `WarnStuckClaimState`. Its
residual shows the executed mutated `Yes` result on the path where both
concatenations have nonzero final balance, contradicting the unchanged
`matchAnswer=No` obligation. See
`evidence/stage4_body_mutation_kprove.log`.

Stage 4 passes.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/stage5_rule_inventory.txt` is the exhaustive source-position
inventory for `verification.k`, `spec.k`, the assembly semantics, and every
supplied helper K file. It enumerates every configuration, syntax declaration,
rule, context, claim, and every occurrence of function/total/functional,
simplification, priority, owise, macro, symbol, and concrete attributes.
`evidence/stage5_inventory_counts.log` gives the per-file counts.

Across these files there are 236 syntax-declaration starts, 711 rule starts,
five contexts, three claims, 45 priority attributes, two simplification
attributes, and 25 `symbol(...)` declarations. There is no `[functional]`
declaration. `verification.k` contributes nine syntax/function declarations
and 16 rules; the spec contributes only the three claims. The raw inventory,
not this summary, is the exhaustive enumeration.

### Proof-local extensions

There is no proof-local `<k>` rewrite, operational bridge, priority rule, opaque
symbol, fresh oracle, or trusted primitive.

The nine proof-local functions and all 16 equations are sound:

| Function | Complete rule decision |
|---|---|
| `parenCodes` | Empty/cons constructors are exhaustive and recursion descends. It is true exactly for code sequences containing only 40/41. |
| `nextBalance` | Guards `C==40` and `C=/=40` are disjoint and exhaustive. The two simplification equations are the exact increment/else-decrement source branches. |
| `scanBalance` | Empty/cons cases are exhaustive and structurally descending; it is the exact repeated `nextBalance` fold. |
| `nextMinimum` | Guards `N<M` and `N>=M` are disjoint and exhaustive over integers; results exactly implement `minimum=min(N,M)`. |
| `scanMinimum` | Empty/cons cases are exhaustive and descending; the next balance is used both as the new balance and in the minimum update, exactly as the source loop. |
| `scanLast` | Empty/cons cases are exhaustive and descending; the cons step replaces the prior value with the yielded one-character string. |
| `goodParens` | Transparent equation for final balance zero and nonnegative minimum prefix. |
| `possibleMatch` | Transparent disjunction of the two concatenation orders. |
| `matchAnswer` | `possibleMatch` and its negation are disjoint/exhaustive; the right sides are exactly the code sequences for `Yes` and `No`. |

The two simplification rules are therefore true over their full guards. The
`total` declarations have constructor-complete or complementary-guard coverage.
There are no overlaps with disagreeing right sides and every recursive call
decreases an `IntSeq`.

The loop claims are derived reachability circularities, not ordinary assumed
rules. Their exact invocation/control/state connection is established by the
focused fixed-semantics `#Top` runs. They do not replace either loop with an
oracle; the circularity closes only after one real source iteration has
established the invariant step.

### Used-construct mapping

Every material submitted-program constructor has a fixed declaration and
execution path:

| Submitted construct | Fixed source/rules used |
|---|---|
| call, name lookup, argument binding, frame push/pop | `core.k` lookup/evaluation rules; `call.k` closure call; `functions.k` bind/return/pop |
| `Assign` and `AugAssign` | `syntax.k`; `controls.k` scope updates; `int.k` `+`/`-` |
| two-element list subscripts at 0/1 | `subscript.k` contexts, `applyIndex`, `valSeqAt`, `normIdx` |
| string literals, concatenation, equality, iteration | `str.k` `strToCodes`, `seqConcat`, comparison and iterator rules |
| integer literals and comparisons | `core.k`, `operators.k`, `int.k` |
| `For` and target binding | `controls.k` `#loop` protocol; `str.k` iterator; `tuple.k` `#bindTgt` |
| nested `If` statements | strict syntax plus `controls.k` `#branch` rules |
| `Return` | strict syntax plus `functions.k` return and pop rules |

Evaluation is left-to-right where material: `BinOp` is `seqstrict`, subscript
has ordered contexts, calls evaluate callee then arguments, and loop iteration
binds the yielded character before executing the two body statements. The entry
state makes list indices 0 and 1 in bounds. The input strings are ASCII
parenthesis codes, within `strToCodes`'s modeled domain. Each call frame is fresh
at `scopeLoc=1`; the heap, stack, return, exception, and exit cells follow the
fixed call/return rules.

### Entire supplied-semantics inventory

Every inventoried supplied rule was reviewed by module. The classification
below applies to all rules in each row; exact individual source lines are in
the exhaustive inventory.

| Module | Rules | Static decision and relevance |
|---|---:|---|
| `syntax.k` | 0 | Grammar declarations cover every submitted AST constructor; unused grammar is inert. |
| `core.k` | 46 | Configuration, scope lookup, sequencing, literals and structural helpers are coherent. The reachable lookup/eval/helpers preserve all pinned cells. OOB write behavior is outside this source contract. |
| `iter.k` | 0 | Declares the iterator protocol only. |
| `range.k` | 6 | Guarded range length/iteration equations are structurally faithful; unreachable here. |
| `operators.k` | 10 | Ordered evaluation and dispatch are faithful; reachable string/int cases select disjoint sort-specific equations. Ref priorities are unreachable for the unboxed read-only input representation. |
| `int.k` | 16 | Reachable addition, subtraction and comparisons are ordinary integer facts. Division/modulo/power are unreachable. |
| `bool.k` | 13 | Short-circuit/value rules and ref priorities are coherent but unreachable in this body. |
| `float.k` | 121 | Float dispatch and 22 named opaque proof-domain symbols are unreachable from parenthesis strings and integer counters, so none can influence a branch, result, cell, or postcondition. |
| `str.k` | 28 | Reachable literal, concatenation, equality and iteration rules are exact on codes 40/41 and the literal result codes. Prefix/membership/order helpers are structurally defined and unused. |
| `set.k` | 12 | Structural set-code equations; unreachable. |
| `list.k` | 27 | List construction/equality/membership/mutation rules are unreachable; the input is already a legal bare list value and is only read by subscript. |
| `tuple.k` | 21 | The reachable `#bindTgt(Name,Val)` rule updates only the loop target. Tuple creation/unpacking/indexing paths are unreachable. |
| `subscript.k` | 40 | The reachable object/index contexts and in-bounds list equations are exact. Total-but-underspecified OOB access and all slicing rules are unreachable because the formal input has exactly two elements and only indices 0/1 occur. |
| `comprehension.k` | 7 | Syntactic macro expansion only; unreachable. |
| `methods.k` | 75 | String/list method functions are unreachable. Their constructor recursions and complementary guards do not contribute to proof closure. |
| `controls.k` | 34 | Reachable assign/if/for rules match real control and scope updates. Break/continue/import/while/ref rules are unreachable. Priorities resolve cell/ref overlaps and do not bypass this execution. |
| `functions.k` | 15 | Reachable bind, return and pop preserve the caller continuation and restore stated cells. Closure-cell/lambda rules are unreachable. |
| `builtins.k` | 137 | Builtin folds/conversions and opaque `md5hexCodes` are unreachable because the body calls no builtin. |
| `call.k` | 21 | Reachable generic callee/argument evaluation and ordinary closure call preserve binding/order/state. Builtin, method, type and annotated-closure routes are unreachable. |
| `sort.k` | 19 | Opaque `sortVS`/`sortKeyVS` and sorting rules are unreachable; the body never resolves or calls `sorted`/`.sort`. |
| `assert.k` | 3 | Assert execution is used only by the reviewer LLVM harness, not by the proof or submitted function body. Its true/false rules correctly consume or signal the assertion. |
| `dict.k` | 28 | Dict rules are unreachable. |
| `concrete.k` | 16 | Imported only by `MPY-KRUN`, never by the Haskell proof module. Its rules affect finite concrete evidence only. |

The supplied semantics intentionally leaves some invalid or out-of-subset
behaviors abstract instead of modeling Python exceptions, notably out-of-bounds
`valSeqAt`, and contains opaque float, sorting, and digest symbols for other
tasks. There is no satisfying input in this theorem's intended domain that
reaches any such case. Accordingly there is no false-conclusion witness on the
intended domain, and these are excluded-language observations rather than
unsound rules contributing to this proof.

No inventoried rule encodes this task's answer, intercepts this function,
fabricates a loop result, or makes a false result provable on the intended
domain. Stage 5 passes.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The reviewer mutation changes the
entry result obligation from `matchAnswer(A,B)` to constant `No`:

```text
ensures ?RESULT ==K str(iCons(78, iCons(111, .IntSeq)))
```

It is demonstrably false for the satisfying ground state `A=.IntSeq`,
`B=.IntSeq`, where the real and claimed correct result is `Yes`. The generated
mutation and exact diff are:

- `evidence/spec_false_result_review.k`
- `evidence/stage6_false_result_diff.log`

`kprove --dry-run` exited zero, establishing that the mutated spec built and
parsed successfully. The actual proof exited 1 with
`WarnStuckClaimState`; the residual contains the real `Yes` string and the path
conditions for zero final balance and nonnegative minimum, while the destination
requires `No`. This is the expected reachable unmet result obligation, not a
parser error, timeout, import failure, or unrelated crash. See
`evidence/stage6_false_result_dry_run.log` and
`evidence/stage6_false_result_kprove.log`.

Stage 6 passes.

## 7. Proven versus assumed accounting

### What is formally proved

Conditional on the supplied MPY definition and K toolchain, the reachability
proof establishes partial correctness for every pair of finite `IntSeq`
strings whose codes are all 40 or 41, with no length bound:

- the exact submitted function body is called with the pair;
- both real scans execute with correct balance, minimum, and final-character
  updates;
- real branch and return control executes; and
- if the call reaches a result, it is `Yes` iff at least one concatenation has
  final balance zero and no negative prefix, otherwise `No`.

The proof does not merely establish examples or a finite unrolling. The loop
claims are symbolic over arbitrary `IntSeq` tails.

### Trust ledger

| Boundary | Effect on theorem | Decision/evidence |
|---|---|---|
| Trusted supplied semantics | Defines all K execution, state and control behavior. | Acceptable mandated trust boundary. Candidate copy is byte-identical to the trusted tree. Used rules were statically audited and concretely exercised on representative cases. |
| Trusted `py2mpy.py` | Connects generated Python AST to submitted MPY. | Acceptable mandated translator boundary. Trusted regeneration is byte-identical, and constructor comparison pins the exact regenerated body in the claim. |
| K 7.1.293 compiler, Haskell backend, LLVM backend and SMT/K builtins | Establish build, concrete execution and `#Top`. | Standard low-level proof-tool trust boundary; versions and fresh outputs are recorded. |
| Ordinary mathematical characterization of balanced parentheses | Connects `final balance = 0` plus `minimum prefix >= 0` to the prompt's word “balanced.” | Exact standard characterization over the parenthesis-only domain; no extra source-domain assumption. |
| Bare read-only `list(ValSeq)` input representation | Represents the source-contract list without heap allocation in the entry claim. | Acceptable within the supplied semantics, which explicitly permits bare list values for read-only claim inputs. This body only reads indices 0/1 and never observes identity or mutation. |

The proof theory contains these 25 supplied opaque/named symbols:

- float/conversion symbols:
  `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`,
  `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
  `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
  `roundFN`, and `sqrtF`;
- sorting symbols: `sortVS` and `sortKeyVS`; and
- digest symbol: `md5hexCodes`.

None is reachable from this program term or used by a proof-local function,
loop claim, path condition, result, or postcondition. There is no proof-local
opaque symbol.

The differential test empirically supports generated-versus-canonical Python
fidelity on its finite domain. The LLVM harness empirically supports the
exercised supplied-semantics execution bridge on seven cases. Neither is used
as a substitute for the universal K proof.

Excluded behavior is limited to inputs outside the stated source contract,
Python features outside the supplied MPY subset, and a separate theorem of
termination/liveness. There is no finite-size restriction or material
source-contract omission.

### Gate and verdict decision

- Gate A, real-program soundness: PASS.
- Gate B, intent adequacy: PASS.
- Gate C, trust/evidence auditability: PASS.

The proof reconstructs cleanly, constrains the result, executes and is
sensitive to the exact real submitted body, covers the unrestricted
parenthesis-string source domain, and uses no materially unsound proof
extension. The appropriate benchmark verdict is therefore `PASS / LEGIT`.

VERDICT: PASS
LEGITIMACY: LEGIT
