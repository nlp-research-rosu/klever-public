# Adversarial audit: 29-filter-by-prefix

## Executive decision

The candidate contains a legitimate partial-correctness proof under the supplied
MPY semantics. I independently rebuilt both backends from source, reran the
original two-claim spec to `#Top`, proved the loop obligation separately, proved
the entry obligation compositionally from that separately checked loop lemma,
and obtained meaningful failures from both a false-result mutation and a
program-body mutation.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, for two
auditability limitations:

1. the candidate formalizes an input list with the proof-only
   `stringList(StrList)` constructor rather than a source-language `list`
   value. Its two iterator rules are structurally isomorphic to the fixed list
   iterator, and the program does nothing with the input except iterate it, so
   this is a sound intent bridge on the stated domain. The candidate supplies
   no bridge-free machine-checked theorem connecting those representations;
2. `run-input.json`, `metrics.json`, `codex-last.txt`, and `codex-output.log`
   are missing, and no structured generation trace is present. This prevents
   the requested provenance review, although it does not invalidate the
   independently reconstructed source proof.

No candidate-local unsound rule, free result, execution shortcut, substituted
body, or false conclusion witness was found.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. The mode and trusted mounts
therefore do not contradict one another; this is not an infrastructure breach.
Per the requested boundary, I did not use `writing-semantics`.

The recursive, no-dereference comparison of
`/candidate/reference-semantics` against the trusted tree returned exit 0.
Their path sets, file types, and bytes agree. No symlink occurs anywhere in the
candidate semantics tree. The candidate `prompt.py` and `py2mpy.py` are also
byte-identical to their trusted counterparts:

- `prompt.py`: SHA-256
  `a173ce6b1e3767cabcf0ff73457d20e4eac07e0968b173b76afa0b35c0799646`;
- `py2mpy.py`: SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`;
- top-level `semantics.k`: SHA-256
  `57e8f9f3178639bbb87f95e5cc596bbaa91a6463f965b1965911eff9a0269f97`
  in both trees.

Evidence: [stage1_integrity.sh](evidence/stage1_integrity.sh) and
[stage1_integrity.log](evidence/stage1_integrity.log). The script's exit 1 is
intentional and is solely due to the four provenance omissions below; all byte,
type, and semantics-tree checks exit 0.

### Missing and extra artifacts

The following requested files are absent:

- `/candidate/run-input.json`;
- `/candidate/metrics.json`;
- `/candidate/codex-last.txt`;
- `/candidate/codex-output.log`.

There is no structured generation trace under `/candidate`. Consequently there
were no untrusted generation claims to rely on or compare. The candidate does
contain `__pycache__` bytecode and concrete-test files; these are extra
non-source evidence, not changes to the trusted semantics. I ignored all
candidate caches and rebuilt from source.

All proof-critical submitted sources are ordinary files:
`solution.py`, `solution.mpy`, `spec.k`, `verification.k`, the supplied
semantics tree, and the trusted-equal translator. No required proof source is
missing, mistyped, or symlinked.

The live toolchain is K 7.1.337 for both `kompile` and `kprove`; see
[toolchain.log](evidence/toolchain.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a finite Python `List[str]` and a string prefix, return a new list
containing exactly the input elements whose `str.startswith(prefix)` result is
true. Preserve input order and duplicates. The documented cases require
`([], "a") -> []` and
`(["abc", "bcd", "cde", "array"], "a") -> ["abc", "array"]`.

The trusted canonical implementation is a filtered list comprehension. The
candidate implementation initializes an empty result, iterates the input, tests
`string.startswith(prefix)`, appends matching strings, and returns the result.
On the intended finite list-of-strings domain these algorithms are equivalent.
The extra initialization `string = ""` does not affect the returned result.

### Translator identity

I invoked the trusted translator on the scratch copy of `solution.py`.
The regenerated and submitted `solution.mpy` files are byte-identical, both
with SHA-256
`1c4b746359e3db4ea54a2e3c9dd703b9a4bc4f1b75b0b6c0af45d832931f9502`.
The translator and `cmp` commands both exited 0.

### Independent differential test

[differential_test.py](evidence/differential_test.py) imports the trusted
canonical entry point and submitted entry point from separate scratch files. It
does not reuse any K summary equation. It checks:

- both documented examples;
- empty input and empty prefix;
- empty strings;
- exact match, shorter and longer prefixes;
- both sides of the `startswith` branch;
- order and duplicate preservation;
- Unicode examples;
- all 3,200 combinations formed from all lists of lengths 0 through 3 over
  `["", "a", "b", "aa", "ab", "ba", "bb"]` and eight boundary prefixes.

All 3,214 cases agreed, with zero mismatches and exit 0. Commands, generated
scope, explicit boundary inputs, and results are in
[stage2_run.log](evidence/stage2_run.log). This is finite adequacy evidence, not
a universal proof.

## 3. Clean proof reconstruction

I copied only source artifacts into
`/tmp/audit-work/29-filter-by-prefix/candidate-src`, used the trusted semantics
copy, and copied no candidate-kompiled definition or cache.

The clean reconstruction commands were:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled

krun reviewer-concrete.mpy \
  --definition runtime-audit-kompiled --output pretty

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition verification-audit-kompiled

kprove spec.k --definition verification-audit-kompiled \
  --spec-module FILTER-BY-PREFIX-SPEC
```

Every command exited 0. The concrete run finished with `.K`, `NoExc`, and exit
code 0. The original proof printed `#Top`. Full bounded output is in
[stage3_clean_rebuild.log](evidence/stage3_clean_rebuild.log); the independent
concrete source is [reviewer-concrete.py](evidence/reviewer-concrete.py).

The concrete program tests actual MPY list construction on six normal and
boundary cases: empty input, the documented nonempty case, empty prefix, prefix
longer than the element, duplicate/order preservation, and both branch
outcomes.

### Each positive claim

The original run proves both submitted claims together and prints `#Top`.
I additionally separated the obligations:

- The exact loop claim in [spec-loop-only.k](evidence/spec-loop-only.k)
  independently prints `#Top`, exit 0; see
  [stage3_isolated_claims.log](evidence/stage3_isolated_claims.log).
- The entry claim needs the loop invariant as its induction principle.
  [spec-entry-with-proven-loop.k](evidence/spec-entry-with-proven-loop.k)
  marks the byte-equivalent, already independently proved loop claim
  `[trusted]` and leaves the entry claim as the only new proof obligation.
  That run prints `#Top`, exit 0; see
  [stage3_entry_composition.log](evidence/stage3_entry_composition.log).

An earlier auxiliary attempt passed the preserved evidence spec by absolute
path, so K searched for `verification.k` beside that file and exited 113. After
copying the exact spec into scratch, the loop claim closed. An entry-only
experiment with the loop claim removed was interrupted because it also removed
the induction principle. These are harness diagnostics, not target-proof
failures; they are retained in `stage3_reconstruct.log` and
`stage3_isolated_claims.log` rather than hidden.

The LLVM compiler reports non-exhaustiveness warnings in fixed, unused helpers
such as `mapStrVS`, float conversion, `joinCodes`, and out-of-bounds
`valSeqAt`. The Haskell build reports unused variables in fixed `strLt` rules.
None lies on this program's execution or proof path, and both definitions build
successfully.

## 4. Adequacy and real-program pinning

### Claim meanings

The loop claim says:

- precondition: execution is at the exact `#loop` generated by the submitted
  `for`; the iterator is a finite `stringList(REST)`; the current function frame
  binds `prefix`, `result`, `string`, and `strings`; the result reference `H`
  points to an accumulator sequence `ACC`;
- postcondition: the loop has finished, the arbitrary following continuation is
  preserved, the same frame and result reference remain, and the heap list is
  `ACC` followed by exactly `prefixFilter(PREFIX, REST)`. The final loop
  variable is intentionally existential.

The entry claim says:

- precondition: start from the ordinary module configuration, load the
  translated `filter_by_prefix` definition, and call it with every finite
  `StrList` and every finite `IntSeq` prefix;
- postcondition: normal control returns to module scope with empty stack,
  `noRet`, `NoExc`, one allocated result list at heap location 0, `heapLoc = 1`,
  and an observer that reduces to Boolean `true` only when that list is exactly
  `prefixFilter(PREFIX, INPUT)`.

There is no logical `requires` restriction beyond the algebraic sorts and exact
initial configuration. All `StrList` and `IntSeq` terms are finite constructor
terms.

### Exact body pin

`filterByPrefixDef` expands to the same AST as the submitted, trusted-translated
`solution.mpy`: import, parameters, both assignments, `For`, `If`,
`startswith`, `append`, and `Return(Name("result"))` all agree. Empty AST lists
are merely written explicitly as `.Exprs`/`.Stmts`. Thus the `<k>` cell loads
and executes the real submitted body, rather than a summary call.

The definition is duplicated as a macro rather than read from the `.mpy` file
at proof time. The byte-identical translator check pins the current submission,
and the independent body mutation gives dynamic sensitivity evidence:
changing `Return(Name("result"))` to `Return(ListExpr(.Exprs))` built
successfully but failed proof with a residual comparing `.ValSeq` to
`prefixFilter(PREFIX, INPUT)`, an extra heap entry, and `heapLoc = 2`.
See [stage5_body_sensitivity.log](evidence/stage5_body_sensitivity.log).

### Satisfiable witnesses and ground substitution

[claim_witness_check.py](evidence/claim_witness_check.py) exhibits:

- entry: `INPUT = ["abc", "bcd", "array"]`, `PREFIX = "a"`, the exact empty
  initial heap/stack/return/exception state; the claimed, canonical, and
  candidate results are all `["abc", "array"]`;
- loop: `L = 1`, `H = 7`, `SC = .Map`, `CURRENT = ""`,
  `ACC = ["seed"]`, `REST = ORIGINAL = ["abc", "bcd", "array"]`,
  `PREFIX = "a"`; the claimed final heap value and both Python calculations are
  `["seed", "abc", "array"]`.

The script exits 0; see [stage4_witnesses.log](evidence/stage4_witnesses.log).

### Result constraint and representation limitation

`#checkFilter` reads the actual list behind the returned reference and produces
`ACTUAL ==K EXPECTED`; it does not introduce a fresh result. The exact final
heap is also constrained. The fresh false-postcondition mutation in Stage 6
confirms this is discriminating.

The entry claim supplies `stringList(INPUT)`, not fixed-semantics
`list(vCons(...))` or a heap reference to such a list. This is a proof-only
input value. Its empty and cons iterator rules are a step-for-step
bisimulation with the fixed list iterator after the mapping
`sCons(S,R) <-> vCons(str(S),R)`: both produce `#iterDone` at empty and
the same string yield plus corresponding rest at cons. Since the function only
iterates its input, this soundly covers the intended observable behavior.
Nevertheless, no separate bridge-free K theorem states that relation. That is
the principal reason for `CONCERNS`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[rule_inventory.md](evidence/rule_inventory.md) is a generated,
line-addressed inventory of every top-level syntax declaration, configuration,
context, ordinary rule, equation, simplification, priority/owise/concrete
attribute, and claim in all supplied K files plus `verification.k` and
`spec.k`. The source and generator are
[inventory_k.py](evidence/inventory_k.py), with command record in
[stage5_inventory.log](evidence/stage5_inventory.log).

The inventory contains 944 records:

- 232 syntax declarations;
- 704 rules: 458 equations, 5 simplification equations, and 241 operational
  rules;
- 5 contexts;
- 1 configuration;
- 2 reachability claims.

Records 1–928 are the integrity-exact supplied semantics; records 929–942 are
all candidate proof-local declarations/rules; records 943–944 are the claims.
Every row includes an audit disposition. There are no hidden imported
candidate helper modules.

### Supplied configuration and rule families

The selected fixed semantics has the expected cells for computation,
environment, scopes, allocation, heap, call frames, return, exception, and
exit code. On the used path:

| Submitted construct | Fixed/proof rule path and decision |
|---|---|
| `Module`, statement sequence | `#loadAll` and statement sequencing in `core.k`; preserves continuation and cells. |
| `ImportFrom("typing","List")` | Generic import no-op in `controls.k`; type hints have no runtime effect here. |
| `FuncDef`, call | Closure creation in `functions.k`; callee and arguments evaluate left-to-right in `core.k`/`call.k`; frame push/bind/pop restores caller state. |
| `Name` | Scope-chain `#look`; the concrete frames used here do not enter the higher-priority closure-cell branch. |
| `ListExpr()` | Left-to-right element evaluation followed by one fresh heap allocation in `list.k`/`core.k`. |
| `Assign` | Updates the current ordinary frame; no cell-variable branch is enabled. |
| `Str("")` | `strToCodes("") = .IntSeq`; no ASCII limitation is reached for any nonempty source literal. |
| `For` | Evaluates its iterable once, enters `#loop`, and uses the iterator protocol. |
| `stringList` input | The two proof-local empty/cons rules yield the same protocol events as fixed list iteration. |
| `If` | Strict condition evaluation followed by the disjoint `truthy` branches. Here the condition is already Boolean. |
| `Attribute`/`Call` | Produces a bound method, evaluates arguments left-to-right, and dispatches without bypassing a user body. |
| `str.startswith` | `applyMethod` calls total `startsWith`; its empty/nonempty equations are exhaustive, disjoint, and structurally descending. |
| `list.append` | Higher-priority mutator rule updates exactly the referenced heap list with one right-end element and returns `noneV`; `Expr` discards that value. |
| `Return` | Evaluates the actual result name, sets `retV`, pops exactly one frame, restores the saved continuation/environment, and preserves escaping heap objects. |

The strict/sequence contexts establish the needed evaluation order.
Allocation is monotone and guarded for freshness. The active priority rules
only select list dereference/mutation and normal cell/call specializations;
their guards are disjoint in this concrete ordinary-frame path. No exception,
break, continue, closure-cell, output, or external-state rule is abstracted by
the candidate.

The supplied tree also defines many constructs unused by `solution.mpy`.
Those remain part of the fixed semantics boundary rather than candidate proof
extensions. The inventory explicitly exposes all 25 symbolic/opaque primitives:
`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
`roundFN`, `sqrtF`, `sortVS`, and `sortKeyVS`. None is reachable from this
program, its invariant, `startsWith`, `prefixFilter`, or the result observer.
They therefore cannot influence control, heap, or postcondition in this proof.

### Candidate proof-local inventory

| Records | Extension | Classification and decision |
|---|---|---|
| 929–930 | `filterByPrefixDef` syntax/macro | Exact syntax pin, not an execution summary. It expands to the trusted-translated body. Body mutation is rejected. Sound. |
| 931–932 | `StrList`, `stringList` declarations | Free algebraic proof representation. No equations or answer are hidden in the constructors. Sound, with the Stage 4 adequacy bridge. |
| 933–934 | `#iterNext(stringList(...))` | Operational extension only for the new constructor. Empty/cons cases are exhaustive and disjoint, preserve arbitrary continuation and all cells, and emit exactly the list iterator's protocol events. No fixed rule is preempted. Sound. |
| 935–938 | `prefixFilter` and three equations | Definitional result summary. Empty/cons constructors are exhaustive; true/false guards are disjoint and cover Boolean `startsWith`; recursion strictly descends `REST`. This defines, rather than assumes, the intended retained sequence. Sound. |
| 939 | `valSeqConcat(VS,.ValSeq) = VS` | Right identity derived by induction from fixed left-recursive concatenation. Its overlaps agree at empty and cons cases. Sound. |
| 940 | associativity simplification | Ordinary associativity for finite `ValSeq`; right-associating orientation descends in left nesting and all overlaps agree with fixed concatenation. Sound. |
| 941–942 | `#checkFilter` declaration/rule | Proof observer, not a program bridge. It reads exactly the returned heap object, leaves heap and other cells unchanged, preserves arbitrary suffix, and replaces only the observer by structural equality. Sound and result-bearing. |

There is one candidate-local `[total]` function (`prefixFilter`), five
candidate simplification equations (three filter equations and two list
lemmas), no `functional` declaration, no opaque candidate symbol, and no
candidate priority rule.

`prefixFilter` appears in the postcondition, but no operational rule rewrites
the program call, loop, `startswith`, or append directly to `prefixFilter`.
The actual loop body executes and the loop reachability claim establishes the
connection. This is not the circular oracle pattern.

No inventoried candidate rule was labeled unsound, because there is no
satisfying intended-domain witness on which any such rule derives a false
conclusion. The narrower evidence gap for `stringList` is the absent universal
representation theorem, not a false iterator equation.

## 6. Fresh non-vacuity test

I created [spec-vacuity.k](evidence/spec-vacuity.k) in scratch. It retains the
real loop invariant and changes only the entry observer to demand

```text
vCons(str(PREFIX), prefixFilter(PREFIX, INPUT))
```

while the actual final heap obligation remains
`prefixFilter(PREFIX, INPUT)`. A concrete satisfying witness is empty input and
prefix `"a"`: both Python implementations return `[]`, while the mutation
demands `["a"]`.

`kprove --dry-run` exits 0, proving the mutation parses and builds against the
fresh definition. The live proof exits 1 with `WarnStuckClaimState`; its
residual explicitly fails the implication

```text
prefixFilter(PREFIX, INPUT)
  #Equals vCons(str(PREFIX), prefixFilter(PREFIX, INPUT))
```

and ends with the expected prover error, not a parser/import/backend failure.
The mutation harness itself exits 0 only because that proof failure is the
expected result. Exact commands and complete bounded residual are in
[stage6_nonvacuity.log](evidence/stage6_nonvacuity.log).

## 7. Proven versus assumed accounting

### What is formally established

Under the supplied MPY semantics plus the audited proof-local definitions, the
successful reachability proof establishes partial correctness:

> For every finite constructor `INPUT:StrList` and
> `PREFIX:IntSeq`, if the exact submitted `filter_by_prefix` AST executes from
> the claim's initial state and reaches normal completion, the sole allocated
> result list contains, in original order and with duplicates preserved,
> exactly those `str(S)` elements for which the supplied
> `startsWith(PREFIX,S)` is true. The call stack is empty, return state is
> cleared, and no exception is present.

The loop claim formally establishes the accumulator invariant for any finite
remaining `StrList`, arbitrary accumulator, and arbitrary following
continuation matching its frame.

This is a partial-correctness result. It is not a claim about resource bounds,
Python implementation internals, or behavior outside the supplied MPY subset.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.337 parser/compiler/Haskell prover and its logical kernel | All machine-check results | Necessary low-level tool trust; version and exact outputs recorded. |
| Trusted mounted `prompt.py`, `canonical.py`, and `py2mpy.py` | Intent statement, translator pin, differential oracle | Authorized trusted inputs. Candidate copies of prompt/translator are byte-identical. |
| Integrity-exact supplied MPY semantics | All execution claims | Authorized fixed semantics level. Used rules were reviewed in detail; unused warnings/opaque primitives cannot flow to this result. |
| Python string-to-`IntSeq` interpretation | Natural-language string meaning | Ordinary sequence-of-code-points bridge. The proof accepts arbitrary finite integer sequences, a sound over-approximation for intended strings; the only nonempty program string data enter as values, not unsupported source literals. |
| Python list-to-`StrList`/`stringList` interpretation | Universal intent bridge from formal input to `List[str]` | Structurally justified by the two iterator isomorphisms and by the fact that the body only iterates. Sound but not separately machine-checked; principal concern. |
| `prefixFilter` equations | Formal expected result | Not opaque or assumed: exhaustive guarded recursive definition, statically audited. |
| Supplied `startsWith` equations | Branch condition and summary | Total structural definition; used directly by real execution and the mathematical summary. |
| 3,214-case Python differential | Candidate-to-canonical adequacy only | Finite empirical support, never used as a proof substitute. |
| Six actual-list concrete K runs | Real-list behavior on selected cases | Finite semantics evidence, not a universal connection theorem. |
| Missing provenance files/trace | Audit of how the candidate was generated | Evidence gap only; reconstruction did not rely on those claims. |

The fixed opaque primitives listed in Stage 5 are trusted/abstract operations
for other language features. They have no dependent claim here. There are no
proof-local opaque values, empirical oracles, or fresh symbols influencing the
branch, heap, return, or postcondition.

### Gate summary and verdict rationale

- Real-program soundness: passes. The exact body executes; proof-local rules are
  truthful; control and state are preserved; the result is constrained; both
  result and body mutations fail meaningfully.
- Intent adequacy: legitimate but limited by the unproved
  `stringList`-to-source-list representation theorem. The structural
  isomorphism and the program's iteration-only use make this non-material to
  behavior on the intended domain.
- Evidence auditability: dynamic reconstruction and reviewer evidence are
  reproducible, but candidate provenance metadata is missing.

These limitations warrant `CONCERNS`, not `FAIL`: neither can make a false
postcondition provable, and the candidate proves the real translated body
rather than a substituted or summarized program.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
