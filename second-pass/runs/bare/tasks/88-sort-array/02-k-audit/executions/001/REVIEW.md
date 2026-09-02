# Independent adversarial audit: 88-sort-array

The candidate's proof commands reconstruct successfully and the entry claims
embed the submitted translated program exactly. Nevertheless, the generated
semantics contains a false totalization for empty-list indexing:
`subscriptVal(ListVal(nil), IntVal(-1))` reduces through `ilast(nil)` to
`IntVal(0)`, whereas Python raises `IndexError`. A fresh, trusted-translation
witness demonstrates the false conclusion on the intended input `[]`. Under
the required global rule audit and Gate A contract, that is an unsound
generated-semantics rule, so the proof is not legitimate even though the
submitted body short-circuits before reaching that rule.

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` is neither present nor a symlink. The trusted
mount therefore agrees with the rendered mode; there is no infrastructure
breach and a candidate verdict is appropriate.

Evidence:

- [`stage1-inventory.log`](/audit-output/evidence/stage1-inventory.log) records
  both absence tests, the recursive type/mode/size inventory, hashes, byte
  comparisons, required-file checks, and JSON parsing.
- The mode checks exited 0. No entry under `/candidate` or `/reference` is a
  symlink.

### Required artifacts and provenance claims

The following required regular, non-symlink files are present:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, and `spec.k`. The structured trace is present at
`/candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-01-49-019f897d-2b95-7350-b0e7-fc9a7a147f0f.jsonl`.
No required artifact is missing, mistyped, or symlinked.

The candidate also contains extra generated state:
`semantic-kompiled/` and `__pycache__/`. These are not source-integrity
failures in generated-semantics mode, but they were treated as untrusted and
were not copied or reused. `prove.sh` and the generation trace were likewise
read only as claims.

The candidate and trusted prompt hashes are both
`a5d671eb2ad240d7b0a2b9b6f889f990b1374fa0a9ee025dd04730328ab328c1`;
`cmp` exited 0. The candidate and trusted translator hashes are both
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`;
`cmp` exited 0.

`run-input.json` claims problem `88-sort-array`, condition `bare`, and no
supplied semantics. `metrics.json` claims generation exit 0 without timeout.
`codex-last.txt`, `codex-output.log`, and the parsed JSONL trace claim that a
single all-claims `kprove` run produced `#Top`. Those are provenance claims
only; none was used as proof evidence. The full bounded extraction and the
reviewer-authored whole-trace parser are preserved as
[`stage1-untrusted-claims.log`](/audit-output/evidence/stage1-untrusted-claims.log)
and
[`summarize_generation_trace.py`](/audit-output/evidence/summarize_generation_trace.py).

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract and implementations

For a list of non-negative integers:

1. Return a new list containing the same values.
2. For nonempty input, sort ascending when the sum of the first and last input
   values is odd; sort descending when that sum is even.
3. Return `[]` for empty input.
4. Do not mutate the input list.

The trusted canonical implementation uses an empty-list conditional and
otherwise calls `sorted(array, reverse=(array[0] + array[-1]) % 2 == 0)`.
The candidate implementation calls `sorted` for every input and uses
`len(array) > 0 and ...` to short-circuit the endpoint expression on empty
input. On the documented list domain these are extensionally equivalent.

### Trusted regeneration

From the source-only scratch copy, the exact command

```text
python3 trusted_py2mpy.py solution.py > regenerated-solution.mpy
```

exited 0. `cmp regenerated-solution.mpy submitted-solution.mpy` also exited 0;
both files have SHA-256
`57b802e7c569929fa610d790e73e2131bdc21b2bbb94f143e6db66365b6f3805`.
See
[`translator-identity.log`](/audit-output/evidence/translator-identity.log).

### Independent differential test

[`differential_test.py`](/audit-output/evidence/differential_test.py) imports
the trusted canonical and submitted generated entry points from distinct
paths. It ran:

- all 4 documented examples;
- 16 explicit empty, singleton, endpoint-parity, duplicate, order, zero, and
  large-integer boundaries;
- every list of lengths 0 through 5 over values 0 through 3 (1,365 cases);
- 300 deterministic generated lists of lengths 0 through 20 and values below
  `10^12`, seed `880088`.

The run covered 1,685 cases: 10 empty, 838 ascending/odd, and 837
descending/even. It found zero result mismatches, zero input mutations, and
zero cases in which either implementation returned the input object itself.
The exact generated inputs are preserved in
[`differential-inputs.json`](/audit-output/evidence/differential-inputs.json);
the command and exit 0 are in
[`differential.log`](/audit-output/evidence/differential.log).

This finite evidence strongly supports implementation/canonical equivalence on
the tested domain. It is not a universal K proof.

## 3. Clean proof reconstruction

### Source-only isolation and fresh builds

Only candidate source files and trusted reference inputs were copied to
`/tmp/audit-work/88-sort-array`; candidate `semantic-kompiled/`, bytecode, and
caches were excluded. The copied hashes and entry types are recorded in
[`prepare-scratch.log`](/audit-output/evidence/prepare-scratch.log).

The independently installed tools are K version `v7.1.293`; all three version
commands exited 0. See
[`tool-versions.log`](/audit-output/evidence/tool-versions.log).

Two new Haskell definitions were built from source:

```text
kompile --backend haskell semantic.k --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition concrete-kompiled
```

and

```text
kompile --backend haskell semantic.k --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition proof-kompiled
```

Both exited 0. Logs:
[`build-concrete.log`](/audit-output/evidence/build-concrete.log) and
[`build-proof.log`](/audit-output/evidence/build-proof.log).

### Fresh concrete reconstruction

[`concrete_semantics_compare.py`](/audit-output/evidence/concrete_semantics_compare.py)
ran 12 separate `krun` commands through `concrete-kompiled` on:

```text
[]
[0]
[5]
[0, 1]
[1, 0]
[1, 1]
[2, 4, 3, 0, 1, 5]
[2, 4, 3, 0, 1, 5, 6]
[3, 3, 0, 3, 1]
[4, 0, 3]
[4, 0, 4]
[10^30, 7, 0]
```

Every `krun` exited 0. Every K result matched both independent Python
implementations, and every K `<input>` cell retained the original value.
Commands, full bounded configurations, comparisons, and the aggregate
`cases=12 failures=0` appear in
[`concrete-semantics-compare.log`](/audit-output/evidence/concrete-semantics-compare.log).

### Fresh positive proofs

The untouched submitted spec was first proved as a whole:

```text
kprove spec.k --definition proof-kompiled --spec-module SPEC
```

It printed exactly `#Top` and exited 0
([`kprove-original-all.log`](/audit-output/evidence/kprove-original-all.log)).

Because the original claims are unlabeled, a copy was changed only by renaming
the module and adding labels. The exact diff is in
[`labeled-spec-diff.log`](/audit-output/evidence/labeled-spec-diff.log), and
the artifact is
[`spec-labeled.k`](/audit-output/evidence/spec-labeled.k). Each claim was then
selected independently:

| Claim | Command suffix after common `kprove spec-labeled.k --definition proof-kompiled --spec-module SPEC-LABELED` | Output | Exit |
|---|---|---|---:|
| Empty | `--claims SPEC-LABELED.empty` | `#Top` | 0 |
| Universal nonempty | `--claims SPEC-LABELED.symbolic-nonempty` | `#Top` | 0 |
| Ascending example | `--claims SPEC-LABELED.example-ascending` | `#Top` | 0 |
| Descending example | `--claims SPEC-LABELED.example-descending` | `#Top` | 0 |

The four logs are
[`kprove-empty.log`](/audit-output/evidence/kprove-empty.log),
[`kprove-symbolic-nonempty.log`](/audit-output/evidence/kprove-symbolic-nonempty.log),
[`kprove-example-ascending.log`](/audit-output/evidence/kprove-example-ascending.log),
and
[`kprove-example-descending.log`](/audit-output/evidence/kprove-example-descending.log).

These successful proof runs establish closure under the supplied generated
theory. They do not validate that theory; Stage 5 finds a concrete false rule.

## 4. Adequacy and real-program pinning

### Claim-by-claim meaning

1. **Empty entry claim.** It has no explicit precondition. Starting with the
   exact function AST followed by `invoke("sort_array", ListVal(nil))`, with
   input `nil` and result `NoneVal`, execution must consume `<k>`, retain the
   input value, and set the result to `ListVal(nil)`.
2. **Universal nonempty entry claim.** Its precondition is
   `nonnegative(cons(F, REST))`, meaning every element of the finite nonempty
   integer list is at least zero. It requires the exact function AST to
   have an empty `<k>`, retain the input value, and set the result exactly to
   `ListVal(expectedSort(cons(F,REST)))` whenever execution terminates.
3. **Ascending documented example.** The ground input
   `[2,4,3,0,1,5]` must have `[0,1,2,3,4,5]` and unchanged input on
   termination.
4. **Descending documented example.** The ground input
   `[2,4,3,0,1,5,6]` must have `[6,5,4,3,2,1,0]` and unchanged input on
   termination.

There are no helper or loop claims. The source has no loop. The four claims
are all entry claims over the real control path
`Module/FuncDef -> execute(Return(...)) -> finish`.

### Program identity

The submitted `.mpy` is byte-identical to trusted regeneration. In addition,
[`program_pinning_check.py`](/audit-output/evidence/program_pinning_check.py)
balanced and normalized every embedded `Module(...)` term in `spec.k`; all
four are exactly equal to the regenerated submitted program. The check found
four terms, four matches, and exited 0
([`program-pinning.log`](/audit-output/evidence/program-pinning.log)).

Thus the formal `<k>` terms execute the submitted translated body, not a
substituted program.

### Satisfiability and ground substitution

The empty claim's state is directly realizable. For the universal claim,
`F=4` and `REST=cons(0,cons(3,nil))` satisfy `nonnegative`, because all three
elements are non-negative. Substitution gives input `[4,0,3]`: endpoint sum
`7` is odd and the expected/result value is `[0,3,4]`. For
`F=4`, `REST=cons(0,cons(4,nil))`, endpoint sum `8` is even and the
expected/result value is `[4,4,0]`. Both substitutions match both Python
implementations and fresh K execution in the concrete comparison log.

No result is a fresh or existentially unconstrained variable. The result is an
exact `IntList` term or the transparent `expectedSort` function. However,
`expectedSort` reuses the same `sortFlag` function used to define the
`sorted` builtin's operational result. The K reachability proof therefore
proves an exact execution summary, not an independent theorem using the
otherwise-declared `ascending` and `descending` predicates. Static inspection
shows that the transparent insertion-sort equations have the intended value,
but that summary-to-natural-language bridge is not itself a K claim.

The `<input>` cell proves value preservation in the K model. The model has no
heap or identity, so it cannot formally distinguish a newly allocated list
from returning an alias with the same value. The Python differential test
checks non-aliasing finitely, and the actual implementation calls Python
`sorted`, but the copy-identity clause is outside the formal K theorem.

## 5. Rule-by-rule static soundness review

### Complete declaration inventory

The complete 15-entry declaration inventory and 51-entry local-rule inventory,
with source lines, domains, coverage, and individual decisions, is preserved
in
[`rule-inventory.md`](/audit-output/evidence/rule-inventory.md). The mechanical
source scan is
[`static-declaration-scan.log`](/audit-output/evidence/static-declaration-scan.log).

The declarations are:

- `MPY-SYNTAX`: `Module`; `Stmt` (`FuncDef`, `Return`); `Params`; all eleven
  submitted `Expr` forms; `IntList`; and four `Val` constructors.
- `MPY`: three internal control items; the three-cell configuration; partial
  `eval`; eight partial value helpers; total `ilen` and `ilast`; and five
  total sorting/reversal helpers.
- `MPY-VERIFICATION`: total `expectedSort`, partial nonempty-only
  `endpointEven`, and total `nonnegative`, `ascending`, and `descending`.
- `SPEC`: exactly four reachability claims.

There are no local opaque symbols, `[functional]` declarations, priority
rules, simplification rules, concrete rules, `owise` rules, proof-local
operational bridges, or auxiliary lemmas.

### Submitted-construct coverage and execution

Every constructor in `solution.mpy` maps to a declaration and applicable rule:

| Submitted construct | Declaration/rule path |
|---|---|
| `Module`, `FuncDef`, `Params`, `Return` | R01-R03 |
| `Name("array")`, `Int` | R04-R05 |
| `Call(Name("len"),...)` | R06, R14, R26-R27 |
| `Call(Name("sorted"),...,KwArg("reverse",...))` | R07, R15, R31-R40 |
| `BoolOp("and",...)` | R08, R16-R17 |
| specialized `len(array) > 0` | R09, R18-R19 |
| integer equality | R10, R20 |
| `BinOp("+",...)`, `BinOp("%",...)` | R11, R21-R22 |
| `UnaryOp("-",Int(1))` | R12, R23 |
| indices `0` and `-1` | R13, R24-R25, R28-R30 |

The `and` rule passes its right expression unevaluated and the false case
discards it, so the empty submitted execution correctly short-circuits.
Argument/evaluation ordering is simplified relative to full Python, but all
target subexpressions are pure and the builtin names are not rebound, so no
observable target behavior changes. The exact `finish` rule matches the whole
`<k>` cell and therefore does not discard a framed continuation.

The environment holds the sole `array` binding. There is no heap, allocation,
exception, output, or call-stack cell; these omissions are adequate for value
execution of this pure body except for allocation identity and exceptional
behavior discussed below.

The total-function equations are otherwise constructor-complete, disjoint,
and descending:

- `ilen`: `nil` or `cons`.
- `sortAsc`: `nil` or `cons`.
- `insertAsc`: `nil`, or `cons` split by disjoint/exhaustive integer guards
  `I <= J` and `I > J`.
- `sortFlag`: both Booleans.
- `reverseAcc`: `nil` or `cons`.
- `expectedSort`, `nonnegative`: `nil` or `cons`.
- `ascending`, `descending`: empty, singleton, or length at least two.

Insertion sort preserves the multiset and inserts each head into an ascending
recursive result; reversing the ascending result produces descending order.
Those are truthful mathematical equations, not opaque oracles. No equation
overlap has disagreeing right-hand sides.

### Unsound rules and concrete false conclusion

Two linked rules are unsound on their declared domain:

```text
R25 / semantic.k:118
subscriptVal(ListVal(L), IntVal(-1)) => IntVal(ilast(L))

R30 / semantic.k:126
ilast(nil) => 0
```

R25 has no nonempty guard, and R30 falsely totalizes empty-list last access.
Together they enable the conclusion that Python `[][-1]` returns integer zero
instead of raising `IndexError`.

This is not merely a hypothetical evidence gap. The reviewer created
[`last_empty_probe.py`](/audit-output/evidence/last_empty_probe.py), whose body
is `return array[-1]`, and translated it with the trusted translator into
[`last_empty_probe.mpy`](/audit-output/evidence/last_empty_probe.mpy). On the
intended non-negative-integer-list input `[]`:

- CPython raised `IndexError: list index out of range` and the checker exited
  0 after confirming that exact exception
  ([`last-empty-python.log`](/audit-output/evidence/last-empty-python.log)).
- The fresh K semantics exited 0 with `<result> IntVal ( 0 ) </result>`
  ([`last-empty-k.log`](/audit-output/evidence/last-empty-k.log)).
- Trusted translation exited 0 and the exact constructor term is recorded in
  [`last-empty-translate.log`](/audit-output/evidence/last-empty-translate.log).

The actual submitted empty-input execution does not reach R25/R30 because R16
short-circuits the endpoint expression. That limits the bad rule's effect on
the submitted trace, but it does not make the declared total equation true.
The required validation contract explicitly disallows excusing a globally
false equation as off-path; generated semantics could instead leave
`ilast(nil)` undefined and guard negative-one subscription by nonemptiness.
This false result for a used language construct is a Gate A semantics
soundness failure.

### Other limitations that are not labeled unsound

- `sortedVal` is a transparent insertion-sort model, not an unconstrained
  oracle. Its value equations are mathematically correct. The bridge to full
  CPython `sorted` and its allocation behavior remains partly informal and
  empirically tested.
- Arithmetic uses unbounded K integers, matching Python integers on this
  domain. Modulo is only exercised with positive divisor `2`.
- The specialized `len(E) > 0` rule is truthful for `IntList`.
- Missing semantics for unused Python constructs/operators is allowed in this
  generated-semantics mode and is not a defect.
- `ascending` and `descending` are truthful but unused by the proof; they
  cannot make a claim close.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to rely on. The reviewer copied the
original spec, renamed only its module, and changed the empty result obligation
from `ListVal(nil)` to the demonstrably false
`ListVal(cons(0,nil))`. The preserved artifact is
[`spec-vacuity.k`](/audit-output/evidence/spec-vacuity.k), and the exact
two-change diff is
[`vacuity-mutation-diff.log`](/audit-output/evidence/vacuity-mutation-diff.log).

The empty starting state satisfies the claim (there is no precondition), and
fresh concrete execution establishes the true result `ListVal(nil)`.

The build/parse-only command

```text
kprove spec-vacuity.k --definition proof-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

exited 0 and emitted a valid `kore-exec ... --prove ...` command
([`vacuity-dry-run.log`](/audit-output/evidence/vacuity-dry-run.log)).

The real proof command exited 1 with `WarnStuckClaimState`. Its residual is a
fully terminated configuration with empty `<k>`, unchanged empty input, and
actual result `ListVal(nil)`, which does not unify with the mutated `[0]`
destination. See
[`vacuity-proof.log`](/audit-output/evidence/vacuity-proof.log).

This is a meaningful non-vacuity pass: the positive proof discriminates a
false result obligation. It does not repair the independent Stage 5 semantics
soundness failure.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the candidate's generated K theory:

- If empty-input execution terminates, its K list result is `nil`, and the
  input value cell is unchanged.
- If execution on a finite nonempty `IntList` satisfying recursive
  nonnegativity terminates, its input value cell is unchanged and its result
  is exactly `expectedSort(input)`.
- `expectedSort` selects transparent insertion sort or its reverse according
  to the parity of the first and last values.
- The two longer prompt examples have their stated exact lists on termination.

The result is constrained, the entry states are satisfiable, the submitted
program is pinned exactly, and the fresh false-result mutation is rejected.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K v7.1.293 compiler/prover and imported `INT`, `BOOL`, `STRING`, `MAP` modules | Parsing, arithmetic, Boolean logic, maps, rewriting, proof closure | Necessary low-level trusted base; acceptable for this audit. |
| Trusted `/reference/py2mpy.py` | Connects `solution.py` syntax to the exact constructor program | Byte identity is proved. Faithfulness of the trusted translator itself is an external trusted input. |
| Manually generated Python-subset semantics | Connects constructor execution to Python behavior | Must be rule-audited; most target rules are transparent and sound, but R25/R30 fail. |
| Textual builtin binding for `len` and `sorted` | Selects builtin behavior without a Python environment lookup | Acceptable for this fixed source, which contains no rebinding; not a general Python theorem. |
| `sortFlag`/insertion-sort equations | Determines every nonempty result and the postcondition | Transparent and mathematically truthful; not opaque. The K claim reuses this semantic function, so the sorting-intent bridge is static/informal rather than a separate K theorem. |
| `ilast(nil) => 0` and unguarded `[-1]` helper | Value and exception behavior on empty lists | Illegitimate. A fresh intended-domain witness produces a false `IntVal(0)` conclusion. |
| Omitted heap/allocation identity | “Return a copy” clause | Concerning adequacy limitation. K proves value preservation, not distinct object identity; finite Python tests support but do not prove the bridge. |
| Omitted general exceptions and side effects | Behavior outside the fixed pure target path | Missing unused constructs are allowed, but the fabricated used-construct exception result is not. |
| Differential testing | Candidate/canonical equivalence, no mutation/aliasing on 1,685 inputs; K/Python agreement on 12 inputs | Reproducible finite evidence only, never a substitute for the K proof or a universal semantics connection theorem. |

There are no opaque result symbols, empirical oracles, proof-local
simplification axioms, priority shortcuts, or helper claims. The illegitimate
boundary is the explicit false operational value for empty negative-one
indexing.

### Gate and decision summary

- **Dynamic reconstruction:** pass. Fresh concrete builds/runs and all positive
  claims succeeded.
- **Program identity/result constraint:** pass. The exact submitted AST is
  embedded in all claims, and the mutation test is discriminating.
- **Gate A, generated-semantics soundness:** fail. R25/R30 enable a concrete
  false Python conclusion on intended input `[]`.
- **Intent adequacy:** additionally limited by the lack of allocation identity
  and by an informal, rather than separately claimed, sorter-to-order bridge.
- **Evidence auditability:** pass for the recorded commands and bounded
  artifacts.

Because the proof closes only under a generated theory that fails the mandated
global rule soundness audit, it is not a legitimate partial-correctness proof
of the real generated Python program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
