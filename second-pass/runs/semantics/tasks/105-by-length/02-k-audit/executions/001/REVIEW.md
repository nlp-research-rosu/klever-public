# Independent adversarial audit: 105-by-length

The candidate is **not a legitimate proof of the submitted program**. A clean
reconstruction does produce `#Top`, and the postcondition is result-constraining,
but the proof is about a proof-local duplicate of the function body rather than
the submitted `solution.mpy`. More importantly, its two decisive proof rules
replace the source loops without a bridge-free connection theorem and do not
preserve the loop-target binding. Fresh fixed-versus-extended executions give a
concrete false-conclusion witness for each rule.

The supplied-semantics mount is internally consistent with
`SUPPLIED_SEMANTICS`; this is a candidate failure, not an audit-infrastructure
error.

## 1. Input and provenance integrity

### Semantics-mode boundary

`/reference/reference-semantics` is present, as required in
`SUPPLIED_SEMANTICS` mode. The candidate tree
`/candidate/reference-semantics` was compared recursively against it by name,
entry type, symlink target, contents, and SHA-256:

- all candidate and trusted entries have the same relative names and types;
- all are ordinary files/directories, not symlinks;
- there are no missing or additional semantics entries;
- recursive content comparison exited 0;
- every corresponding semantics file has the same SHA-256.

The candidate `prompt.py` and `py2mpy.py` are also byte-identical to their
trusted mounted versions (`cmp` exit 0). See
[01-integrity.log](evidence/01-integrity.log) and the reviewer script
[check_integrity.sh](evidence/check_integrity.sh).

### Missing provenance artifacts

The following requested candidate artifacts are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`
- any structured generation-trace artifact

Consequently there were no generation claims in those files to check. This is a
provenance deficiency but did not prevent independent reconstruction. There is
also no candidate `PROOF.md` or candidate `spec-vacuity.k`. The candidate's
`prove.sh` and `concrete-tests.mpy` were read only as untrusted claims and were
not used as proof evidence.

All required proof/program sources that are present are ordinary files.
`/candidate/__pycache__/solution.cpython-310.pyc` is an additional generated
cache; it was ignored. No candidate-built K definition was present or reused.

### Isolation and toolchain

The source trees were copied to `/tmp/audit-work/105-by-length`; all definitions
were rebuilt there. Reviewer-authored artifacts and bounded logs are under
`/audit-output/evidence`. The live toolchain was K `v7.1.337` and Python
`3.10.12`; see [00-toolchain.log](evidence/00-toolchain.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a finite array of integers:

1. ignore every integer outside `1..9`;
2. order the retained integers from greatest to least, preserving duplicates;
3. replace each retained integer by its English name from `"One"` through
   `"Nine"`;
4. return the resulting list, with `[]` for an empty/no-retained-value input.

The trusted canonical implementation sorts the complete integer list in
descending order and then ignores values absent from its digit dictionary. The
submitted `solution.py` first filters to `1..9` and then sorts descending. These
algorithms are equivalent on the stated integer-list domain. Inputs containing
non-integers are outside both the natural-language and formal `IntSeq` domains
and were not used to excuse any intended-domain divergence.

### Trusted translation

The trusted command

```text
python3 /reference/py2mpy.py /tmp/audit-work/105-by-length/candidate/solution.py
```

regenerated [solution.regenerated.mpy](evidence/solution.regenerated.mpy).
It is byte-identical to the submitted `solution.mpy`; both have SHA-256
`09a6bdd52e92d8f5740c0ed5e724754e39a82967171d9e719f0b13a441e7c742`.
The exact command and statuses are in
[02-translation.log](evidence/02-translation.log).

### Independent differential testing

The reviewer-authored
[differential_test.py](evidence/differential_test.py) imports the trusted
canonical entry point and the scratch copy of the submitted entry point. It
also compares both with an independently written direct contract oracle. The
corpus contains:

- all three documented examples;
- empty input and explicit `-1/0/1/2/8/9/10/11` branch boundaries;
- duplicates, ascending and descending orders, and very large integers;
- every list of length `0..4` over `[-1, 0, 1, 2, 8, 9, 10]`;
- 256 deterministic generated lists of up to 32 integers.

The complete 3,055-input corpus is
[differential-inputs.json](evidence/differential-inputs.json), SHA-256
`f2cda6bf61e28f8591a1c0bd9d26a9dd91c29ac46c4539348d14d31399037ef1`.
The run exited 0 with `mismatch_count=0`; see
[03-differential.log](evidence/03-differential.log).

This establishes strong finite program-fidelity evidence. It is not a
substitute for the K proof or for a universal operational connection theorem.

## 3. Clean proof reconstruction

### Fresh concrete definition and execution

The LLVM definition was built from the scratch copy of the verified supplied
semantics:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/105-by-length/runtime-kompiled
```

It exited 0. The warnings include intentionally incomplete/opaque total
functions, discussed in stages 5 and 7. The command and output are in
[04-kompile-llvm.log](evidence/04-kompile-llvm.log).

The reviewer generated
[reviewer-concrete-tests.mpy](evidence/reviewer-concrete-tests.mpy) from the
trusted regeneration, not from the candidate's test file. Seven assertions
cover the main example, empty input, strange values, both filter boundaries,
duplicates, all digits, and large integers. `krun` exited 0:

- generator and inputs:
  [make_k_concrete_tests.py](evidence/make_k_concrete_tests.py) and
  [05-make-k-tests.log](evidence/05-make-k-tests.log);
- execution: [06-krun-concrete.log](evidence/06-krun-concrete.log).

### Fresh proof definition and positive target

The Haskell proof definition was independently built with:

```text
kompile verification.k --backend haskell \
  --main-module BY-LENGTH-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/105-by-length/verification-kompiled
```

This exited 0; see [07-kompile-haskell.log](evidence/07-kompile-haskell.log).
`spec.k` contains one positive entry claim. The independent proof command was:

```text
kprove spec.k \
  --definition /tmp/audit-work/105-by-length/verification-kompiled \
  --spec-module BY-LENGTH-SPEC
```

It exited 0 and printed `#Top`; see
[08-kprove-positive.log](evidence/08-kprove-positive.log).

Thus the claim closes under the combined supplied semantics and candidate
proof-local theory. Stages 4 and 5 show why this `#Top` is not a proof of the
real submitted program.

## 4. Adequacy and real-program pinning

### Entry precondition and postcondition

The sole entry claim has no side-condition beyond its term/cell pattern. In
plain language, its precondition is:

- choose any finite `IntSeq IS`;
- directly invoke a proof-local closure `byLengthClosure` with the unboxed
  semantic list `list(intVals(IS))`;
- start in module environment 0 with an empty module scope, the fixed builtins
  scope, empty heap and stack, `noRet`, `NoExc`, and exit code 0.

Its postcondition is:

- after a proof-only `#observeList`, the `<k>` result must be exactly
  `list(tableNames(revVS(sortVS(filterDigits(intVals(IS))))))`;
- the call frame is restored and no exception is present;
- final heap and heap location may be arbitrary existential values.

This is a genuine result equality, not a free result variable, implication, or
tautology. The existential heap variables do not erase the `<k>` result
constraint. The successful fresh false-result test in stage 6 confirms this
point.

The state is satisfiable. For example, `IS = .IntSeq` gives the explicit empty
input state used in the ground non-vacuity run. `IS =
iCons(0,iCons(1,iCons(9,iCons(10,.IntSeq))))` is another satisfying input.
Under the named `sortVS = ascending sort` trust interpretation, the claimed
ground results are respectively `[]` and `["Nine", "One"]`.

[claim_substitution.py](evidence/claim_substitution.py) substitutes four
satisfying inputs into the formal `intVals/filterDigits/sortVS/revVS/tableNames`
expression and compares it with both Python implementations. It exited 0 with
no mismatch; see
[25-claim-substitution.log](evidence/25-claim-substitution.log).

### The claim does not execute `solution.mpy`

This is a material pinning failure.

`spec.k:10-14` starts with `#applyK(toCall(byLengthClosure), ...)`.
`verification.k:9-50` separately declares a function-valued constant
`byLengthBody` and turns it into `byLengthClosure`. Neither `spec.k` nor
`verification.k` has a non-comment reference to `solution.py` or
`solution.mpy`. The claim never executes:

- the submitted `Module(...)` term;
- its submitted `FuncDef("by_length", ...)`;
- module loading;
- name binding and lookup of the submitted `by_length` definition.

The proof-local body currently resembles the submitted inner AST, and manual
inspection found no current statement mismatch. That is only an informal copy
comparison; it is not a source-level or K-level identity pin.

The fresh body-sensitivity test makes the failure observable. In an isolated
scratch copy, the implementation was changed from `return result` to
`return []`, and its `.mpy` was regenerated with the trusted translator. The
unchanged `verification.k` and `spec.k` were freshly compiled into a new
definition. The proof still exited 0 and printed `#Top`:

- mutation, hashes, and proof-source reference search:
  [22-pinning-mutation.log](evidence/22-pinning-mutation.log);
- mutated sources:
  [pinning-mutant-solution.py](evidence/pinning-mutant-solution.py) and
  [pinning-mutant-solution.mpy](evidence/pinning-mutant-solution.mpy);
- fresh rebuild:
  [23-pinning-mutant-kompile.log](evidence/23-pinning-mutant-kompile.log);
- unchanged theorem still `#Top`:
  [24-pinning-mutant-kprove.log](evidence/24-pinning-mutant-kprove.log).

The proof is therefore insensitive to the real program artifact. Under the
audit decision boundary, this is a substituted-program proof and independently
requires `FAIL / NOT_LEGIT`.

### Helper/loop correspondence

`intVals`, `filterDigits`, `nameTable`, and `tableNames` express the intended
integer embedding, digit filter, name table, and pointwise lookup on constructor
inputs. The two candidate loop rules match the textual ASTs of the copied
loops. There are, however, no loop claims or invariants proving those summaries
from fixed loop execution. Instead, the rules directly replace the loops. Their
operational mismatch is detailed next.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The audit inventories every `requires`, module/import, configuration, syntax
declaration, context, rule, and claim, including full multiline bodies, guards,
and attributes:

- line-addressable declaration/rule inventory:
  [k-rule-inventory.md](evidence/k-rule-inventory.md);
- literal numbered source corpus:
  [k-sources-numbered.txt](evidence/k-sources-numbered.txt);
- reviewer inventory generator:
  [inventory_k.py](evidence/inventory_k.py);
- generation command, per-file counts, and status:
  [21-k-inventory.log](evidence/21-k-inventory.log);
- one explicit disposition for each of the 1,116 inventoried declaration
  blocks:
  [k-declaration-dispositions.tsv](evidence/k-declaration-dispositions.tsv),
  generated by
  [classify_k_inventory.py](evidence/classify_k_inventory.py) with its command
  in [21a-k-dispositions.log](evidence/21a-k-dispositions.log).

Across the helper semantics and `verification.k`, there are 708 `rule`
declarations and 234 `syntax` declarations. There are five evaluation contexts,
one configuration, and one entry claim. Searches found no `[functional]` or
`[simplification]` declarations. The inventory explicitly records every
`function`, `total`, macro, `owise`, `concrete`, opaque
`symbol(...)/no-evaluators`, and priority occurrence.

The per-file disposition below applies to every entry in the exhaustive
inventory, with candidate-local exceptions expanded individually afterward.

| File | Syntax | Rules | Static disposition |
|---|---:|---:|---|
| `semantics.k` | 0 | 0 | Assembly only; `MPY` excludes concrete-only module and `MPY-KRUN` adds it correctly. |
| `syntax.k` | 16 | 0 | Declares every constructor used by the submitted AST; strict/seqstrict positions give the expected evaluation order. |
| `core.k` | 37 | 46 | Used configuration, allocation, sequencing, lookup, literals, argument evaluation, truthiness, and sequence helpers inspected; guards/priorities are compatible on this path. |
| `iter.k` | 1 | 0 | Iterator protocol declaration only. |
| `range.k` | 2 | 6 | Unused by this program/claim; no contribution to closure. |
| `operators.k` | 0 | 10 | Fixed unary/binary/comparison routing is the real-loop behavior displaced by the bridges; operand order and dereference rules are appropriate here. |
| `int.k` | 1 | 16 | Integer comparisons/subtraction used by real execution are ordinary mathematical rules on K integers. |
| `bool.k` | 0 | 13 | Short-circuit `and` rules have correct left-to-right behavior for the filter condition. |
| `float.k` | 34 | 121 | Float syntax/rules and many opaque float symbols are unreachable from formal `IntSeq` inputs and do not contribute. |
| `str.k` | 5 | 28 | ASCII string construction covers all nine names; relevant literal rules are constructor-recursive and terminating. |
| `set.k` | 6 | 12 | Unused; no contribution. |
| `list.k` | 5 | 27 | Relevant literal allocation, iteration, and `append` mutation preserve heap identity and order under fixed semantics. |
| `tuple.k` | 4 | 21 | `#bindTgt(Name(...),V)` is the relevant real-loop target update. This is precisely the state update omitted by both candidate bridges. Other tuple rules are unused. |
| `subscript.k` | 15 | 40 | Relevant list indexing is correct for in-bounds indices. `valSeqAt` is deliberately total but equation-incomplete for empty/OOB/opaque sequences; its use is conditional on the intended in-bounds digit/sort interpretation. |
| `comprehension.k` | 3 | 7 | Unused; no contribution. |
| `methods.k` | 27 | 75 | General method helpers are unused; call routing imports them, while the relevant list `append` rule itself is in `list.k`. |
| `controls.k` | 3 | 34 | Fixed `For` unfolds via iterator yield, performs `#bindTgt`, executes the body, and loops. This correct state footprint is bypassed by the candidate rules. |
| `functions.k` | 4 | 15 | Closure frame creation/binding/return/pop used by the proof-local closure; cells are irrelevant on this path. |
| `builtins.k` | 38 | 137 | Builtins scope and call infrastructure inspected; nearly all builtin equations are unreachable. Opaque `md5hexCodes` is unused. |
| `call.k` | 3 | 21 | Relevant callee and left-to-right argument evaluation, heap dereference, closure frame setup, and builtin dispatch inspected. |
| `sort.k` | 6 | 19 | `sorted` allocation, `condRev`, and `revVS` are used. `sortVS` is a fixed supplied opaque trusted primitive in proof and concrete insertion sort in LLVM; accounted for in stage 7. |
| `assert.k` | 0 | 3 | Not in the entry proof; used only by reviewer concrete/witness programs. |
| `dict.k` | 12 | 28 | Unused; no contribution. |
| `concrete.k` | 5 | 16 | LLVM-only deep equality/keyed-sort rules; unused by the target proof and harmless in reviewer concrete runs. |
| `verification.k` | 7 | 13 | Six proof-local function declarations, one observer, and two operational loop bridges; detailed below. |
| `spec.k` | 0 | 0 | One result-constraining claim, but it invokes the substitute closure. |

No additional used-path false conclusion was found in the supplied semantics.
The LLVM non-exhaustiveness warnings for `mapStrVS`, float conversion helpers,
and `joinCodes` concern value constructors unreachable here. The warning for
`valSeqAt(.ValSeq, _)` exposes the documented total-but-underspecified OOB
boundary; every actual source index is in `0..8` only if filtering and the
trusted sort preserve digit membership.

### Construct-to-semantics map

Every constructor in `solution.mpy` has a declaration and fixed behavior:

| Submitted construct | Declaration/fixed rules |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k`; module sequencing in `core.k`; definition binding in `functions.k` |
| `Assign`, `Name` | `syntax.k`; assignment in `controls.k`; scope-chain lookup in `core.k` |
| `ListExpr`, `Str`, `Int`, `Bool` | `syntax.k`; allocation in `list.k`; literals in `str.k`/`core.k` |
| `For` and target `Name("value")` | `controls.k` loop protocol; `tuple.k` `#bindTgt` |
| `If`, `BoolOp`, `Compare` | `controls.k`, `bool.k`, `operators.k`, `int.k` |
| `Expr`, `Call`, `Attribute`, `append` | `controls.k`, `call.k`, `list.k` |
| `sorted(..., reverse=True)` and `KwArg` | `core.k` keyword evaluation, `call.k`, `sort.k` |
| `Subscript`, `BinOp("-")` | `subscript.k`, `operators.k`, `int.k` |
| `Return` | `functions.k` |

The mapping exists; the proof fails because it preempts the fixed `For` rules
and never loads the submitted module.

### Candidate-local rule inventory

The 13 rules in `verification.k` are:

1. `byLengthBody` expansion (`:10-47`): a definitional copy of the current
   inner AST. Its equations are not mathematically false, but it is not linked
   to `solution.mpy`.
2. `byLengthClosure` (`:50`): constructs a closure over that copy; also
   unpinned from the submitted definition.
3. `intVals(.IntSeq)` (`:55`): valid empty embedding.
4. `intVals(iCons(...))` (`:56`): valid recursive integer embedding.
5. `filterDigits(.ValSeq)` (`:61`): valid empty filter.
6. inclusive `filterDigits` rule (`:62-64`): valid on integer heads in `1..9`.
7. excluding `filterDigits` rule (`:65-67`): valid on integer heads outside
   `1..9`; guards are disjoint from and exhaustive with rule 6 for integers.
8. `nameTable` (`:70-79`): correct nine-name sequence.
9. `tableNames(.ValSeq)` (`:83`): valid empty mapping.
10. recursive `tableNames` (`:84-85`): correct in-bounds table lookup on digit
    heads. Its `[total]` declaration is broader than its useful integer/digit
    domain, but this is a coverage/underspecification boundary rather than a
    false equation.
11. `#observeList` (`:90-91`): a proof observer that reads the returned heap
    list without changing the heap; sound for its exact marker context.
12. first-loop operational bridge (`:98-124`): **unsound**.
13. second-loop operational bridge (`:126-152`): **unsound**.

The six function declarations (`byLengthBody`, `byLengthClosure`, `intVals`,
`filterDigits`, `nameTable`, and `tableNames`) are marked `[function,total]`.
There are no proof-local opaque symbols, simplification rules, or auxiliary
claims. The only proof-local priority rules are the two rejected bridges,
both `[priority(40)]`.

### First-loop bridge: concrete false-conclusion witness

The bridge at `verification.k:98-124` replaces the exact filter `For` with:

- removal of the entire loop from `<k>`;
- a direct heap update from `list(.ValSeq)` to
  `list(filterDigits(VS))`;
- no change to the current scope map.

Fixed `For` execution binds `value` on every iteration through
`#bindTgt`. The bridge's `...` admits every trailing continuation, yet it
preserves an old `"value"` binding or leaves it absent. There is no
bridge-free universal connection claim in the candidate, let alone one over
this arbitrary continuation and complete state.

The reviewer witness starts with `values=[]`, `value=99`, executes the exact
filter loop over the intended integer input `[1]`, and immediately observes
`value`:

- under fixed supplied semantics, `value == 1` passes:
  [13-bridge-fixed-real.log](evidence/13-bridge-fixed-real.log), with the final
  scope explicitly showing `"value" |-> 1` in
  [13a-bridge-fixed-real-config.log](evidence/13a-bridge-fixed-real-config.log);
- under the candidate bridge definition, the false conclusion `value == 99`
  passes:
  [14-bridge-enabled-stale.log](evidence/14-bridge-enabled-stale.log), with
  `"value" |-> 99` in
  [14a-bridge-enabled-stale-config.log](evidence/14a-bridge-enabled-stale-config.log);
- fixed semantics rejects `value == 99`:
  [15-bridge-fixed-rejects-stale.log](evidence/15-bridge-fixed-rejects-stale.log);
- the bridge definition rejects the real `value == 1`:
  [16-bridge-enabled-rejects-real.log](evidence/16-bridge-enabled-rejects-real.log).

The source witnesses are
[bridge-witness-real-value.mpy](evidence/bridge-witness-real-value.mpy) and
[bridge-witness-stale-value.mpy](evidence/bridge-witness-stale-value.mpy).
This is a false conclusion on an intended-domain input enabled by the exact
rule's broad continuation and omitted scope update. Priority 40 makes it
preempt fixed iteration once the list is exposed; priority does not justify
equivalence.

### Second-loop bridge: concrete false-conclusion witness

The bridge at `verification.k:126-152` similarly replaces the exact map loop
with a direct update from `list(.ValSeq)` to `list(tableNames(VS))`. It checks
the names/result heap bindings but again omits the loop-target scope write and
accepts an arbitrary continuation.

The independent witness initializes the exact nine-name table, `result=[]`,
and `value=99`, then executes the exact map loop over `[1]`:

- fixed supplied semantics accepts the real final `value == 1`:
  [17-map-bridge-fixed-real.log](evidence/17-map-bridge-fixed-real.log), with
  `"value" |-> 1` in
  [17a-map-bridge-fixed-real-config.log](evidence/17a-map-bridge-fixed-real-config.log);
- the bridge definition accepts the false stale `value == 99`:
  [18-map-bridge-enabled-stale.log](evidence/18-map-bridge-enabled-stale.log),
  with `"value" |-> 99` in
  [18a-map-bridge-enabled-stale-config.log](evidence/18a-map-bridge-enabled-stale-config.log);
- fixed semantics rejects stale 99:
  [19-map-bridge-fixed-rejects-stale.log](evidence/19-map-bridge-fixed-rejects-stale.log);
- the bridge definition rejects real 1:
  [20-map-bridge-enabled-rejects-real.log](evidence/20-map-bridge-enabled-rejects-real.log).

Sources:
[map-bridge-witness-real-value.mpy](evidence/map-bridge-witness-real-value.mpy)
and
[map-bridge-witness-stale-value.mpy](evidence/map-bridge-witness-stale-value.mpy).

This separately witnesses the second rule's false state conclusion on an
intended-domain input.

### Circular result-summary use

Even ignoring the witnessed scope error, neither bridge has the required
bridge-free universal connection theorem showing that fixed execution of its
loop produces exactly `filterDigits(VS)` or `tableNames(VS)` over the complete
match domain. The same summaries introduced by the bridges are used directly
in the final postcondition. Constructor equations and finite tests make the
summaries plausible; they do not connect real loop execution to those
summaries. This is the circular
`programExpression => summary` / `postcondition(summary)` pattern prohibited
by the proof-extension soundness contract.

## 6. Fresh non-vacuity test

No candidate vacuity test was present. The reviewer created a fresh mutation
that changes the result obligation for the satisfying ground input `[]` from
`[]` to `["One"]`:

[spec-reviewer-vacuity-ground.k](evidence/spec-reviewer-vacuity-ground.k).

It was first parsed/compiled using `kprove --dry-run`; this exited 0, proving
that the mutation is well-formed:
[11-vacuity-ground-dry-run.log](evidence/11-vacuity-ground-dry-run.log).

The actual proof exited 1 with `WarnStuckClaimState`. Its residual `<k>` is
`list(.ValSeq)` while the destination requires a one-element list, followed by
the expected "configuration cannot be rewritten further" prover error:
[12-vacuity-ground-kprove.log](evidence/12-vacuity-ground-kprove.log).

This is valid non-vacuity evidence: the entry precondition is satisfiable, the
mutated obligation is reached, and failure is the expected result mismatch.

For transparency, an earlier universal prepend mutation built successfully but
the backend was killed with code 137 and no logical residual
([09-vacuity-dry-run.log](evidence/09-vacuity-dry-run.log),
[10-vacuity-kprove.log](evidence/10-vacuity-kprove.log)). It is explicitly not
counted as evidence. The ground mutation above is the qualifying test.

Passing this gate shows only that the postcondition constrains a result. It
does not repair the unpinned program or unsound operational bridges.

## 7. Proven versus assumed accounting

### What the successful reachability proof actually establishes

Under the combined theory consisting of the supplied `MPY` semantics plus all
13 candidate verification rules, for every symbolic `IntSeq IS`, direct
invocation of the proof-local `byLengthClosure` reaches:

```text
list(tableNames(revVS(sortVS(filterDigits(intVals(IS))))))
```

after `#observeList`, with the modeled call frame restored and no modeled
exception. The closure body is the proof-local `byLengthBody`; the two loops
are evaluated by the candidate summary rewrites, not derived from fixed loop
execution.

It does **not** establish that:

- the submitted `solution.mpy` or its `FuncDef("by_length",...)` was executed;
- a change to the submitted program changes or invalidates the theorem;
- either loop summary follows from fixed semantics;
- the loop-target/local-scope state matches real execution;
- `sortVS` implements ascending sort by a theorem inside this proof.

### Trust and assumption ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K `v7.1.337` parser/compiler/Haskell and LLVM backends | All rebuild, execution, and proof results | Normal toolchain trust; exact commands/statuses preserved. |
| Trusted mounted prompt, translator, canonical implementation | Contract/fidelity bridge | Acceptable audit inputs. Candidate copies match; trusted regeneration is byte-identical. |
| Supplied `MPY` semantics | Language execution model | Required fixed trust boundary for this mode; candidate tree exactly matches it. Relevant paths were statically reviewed and concretely exercised. |
| `sortVS` (`sort.k:18`) | Determines the order in the formal postcondition | Fixed externally trusted builtin abstraction: opaque to Haskell proof, concrete insertion sort for LLVM. Conditional/empirical bridge, not a theorem proved here. |
| `valSeqAt` `[total]` underspecification | `tableNames` on opaque sequences | Acceptable only under the named in-bounds digit-preservation interpretation; compiler warning and limitation recorded. |
| Other opaque float, keyed-sort, and MD5 symbols | None on this program/claim | Unreachable and non-contributing. |
| Current manual equality of `byLengthBody` to the submitted inner AST | Supposed real-program identity | **Illegitimate as pinning.** No source reference or theorem; body mutation leaves `#Top` unchanged. |
| First-loop candidate bridge | Produces `filterDigits` heap summary and enables the entry proof | **Illegitimate.** No connection theorem; concrete false scope conclusion. |
| Second-loop candidate bridge | Produces `tableNames` heap summary and enables the entry proof | **Illegitimate.** No connection theorem; concrete false scope conclusion. |
| Python differential and LLVM assertion tests | Supports implementation/intent and concrete sort behavior on tested values | Strong finite evidence only; cannot justify universal bridges. |

### Decision

Clean `#Top`, Python agreement, concrete tests, and a successful non-vacuity
mutation do not overcome Gate A and pinning failures. The proof substitutes a
separate closure for the submitted program and depends on two materially
unsound operational rules. Each unsoundness finding has a satisfying
intended-domain false-conclusion witness.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
