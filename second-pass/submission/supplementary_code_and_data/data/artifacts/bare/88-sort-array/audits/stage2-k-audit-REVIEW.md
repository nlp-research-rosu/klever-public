# Independent adversarial audit: 88-sort-array

This is an independent reconstruction and static audit of the candidate under
`GENERATED_SEMANTICS`. I did not use candidate-built definitions or accept the
generation report's prior `#Top`.

Outcome: the candidate has a legitimate, unrestricted partial-correctness proof
of the submitted program for finite lists of non-negative integers. The result
is exact and non-vacuous, and the claim executes the byte-identical translated
body. I assign `CONCERNS / LEGIT`, rather than `PASS`, because the generated
semantics contains one demonstrably false but unreachable empty-index rule, and
because its value-only list model does not formalize Python object identity or
allocation. Neither limitation enables a false conclusion about this submitted
program.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = bare`, and `semantics_mode = GENERATED_SEMANTICS` in
`/audit-input.json`.

I inspected all records required by that layout:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`; and
- the JSONL trace at
  `/generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T06-01-49-019f897d-2b95-7350-b0e7-fc9a7a147f0f.jsonl`.

All required paths are real regular files or real directories, and neither the
candidate nor trace trees contain symlinks or unsupported node types. The
structured trace contains 140 parseable JSON records. The hashes for the run,
task, stage result, invocation, metrics, usage, prompt, output, last message,
trusted inputs, and campaign lock all match `/audit-input.json`. The trace file
hash also matches the stage result.

`/audit-campaign-lock.json` is exactly equal as a JSON object to the
`audit_campaign` block and has the recorded SHA-256
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
The independently recomputed pipeline tree digest for `/candidate` is
`07db41bdfb25db8d82fbb49e27f5fa4068f74b416e1def078f50b3e7b4995cf7`,
equal to both the invocation and result's retained-workspace digest. The audit
envelope separately records an audit-launcher aggregate
`candidate_tree_sha256 =
333ec9814fd5fd641e846da248c70fb9bff4907093774946f43131d420be483a`;
because that envelope does not state its tree serialization, I checked every
directly mapped file hash and reproduced the pipeline's defined tree digest
rather than assuming an encoding for that extra aggregate.

The candidate's `/candidate/prompt.py` and `/candidate/py2mpy.py` are
byte-identical to `/reference/prompt.py` and `/reference/py2mpy.py`.
`/reference/reference-semantics` is absent, as required in
`GENERATED_SEMANTICS`; no hidden or inferred semantics was used.

The generation trace and prose only claim that generation succeeded. They did
not contribute to the verdict.

Evidence:

- `/audit-output/evidence/provenance_check.py`
- `/audit-output/evidence/01-provenance-rerun.log` — exit 0
- `/audit-output/evidence/00-toolchain.log`

The first `/audit-output/evidence/01-provenance.log` records a reviewer-checker
schema mistake: it assumed the augmented audit manifest was byte-for-byte the
task manifest. The rerun correctly compares the shared fields and the envelope's
extra `config` field.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract in `/reference/prompt.py` is:

> For any finite list of non-negative integers, return a copy sorted ascending
> when the first-plus-last sum is odd and descending when it is even; return
> `[]` on empty input and do not mutate the argument.

The trusted canonical implementation special-cases the empty list and otherwise
calls `sorted(..., reverse=(array[0] + array[-1]) % 2 == 0)`.
`/candidate/solution.py` uses the equivalent short-circuit condition
`len(array) > 0 and ...`. It preserves the required signature and does not
narrow the list length or integer range.

I regenerated the constructor program with the trusted translator:

```text
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/reconstruction/solution.py \
  > /tmp/audit-work/reconstruction/solution.regenerated.mpy
```

The regenerated file and submitted `/candidate/solution.mpy` are byte-identical,
both with SHA-256
`57b802e7c569929fa610d790e73e2131bdc21b2bbb94f143e6db66365b6f3805`.
See `/audit-output/evidence/02-translation.log`.

The independent differential test imports both `/reference/canonical.py` and
the scratch copy of the submitted solution. It checks:

- all four documented examples;
- empty, singleton, zero, duplicate, even/odd endpoint, ordering, and huge
  integer boundaries;
- every list of length 0 through 4 over values 0 through 5; and
- 500 deterministic random lists of length 0 through 30 with values below
  `10^18`.

There were 2,047 unique cases: 1 empty, 1,002 ascending-branch cases, and
1,044 descending-branch cases. There were zero result mismatches, mutations, or
input/result alias failures.

Evidence:

- `/audit-output/evidence/differential_test.py`
- `/audit-output/evidence/differential-inputs.json`
- `/audit-output/evidence/02-differential.log` — exit 0

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied to
`/tmp/audit-work/reconstruction`. Candidate caches and the candidate's prior
execution were ignored. K 7.1.293 and Python 3.10.12 were available.

Fresh builds:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition concrete-kompiled

kompile semantic.k --backend haskell --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition proof-kompiled
```

Both exited 0; see `03-kompile-concrete.log` and
`03-kompile-proof.log` under `/audit-output/evidence/`.

The fresh LLVM definition executed nine normal and boundary inputs, including
empty, singleton, both parity branches, duplicates, both prompt examples, and
an unbounded-integer example. Every run exited 0, consumed `<k>` to `.K`,
preserved `<input>`, and matched independent Python output. See
`/audit-output/evidence/concrete_semantics_compare.py` and
`03-concrete-semantics.log`.

I added only labels and a distinct module name to a scratch copy of the spec so
that each original positive claim could be selected independently. The claim
bodies are otherwise unchanged:

| Claim | Exact selector | Exit | Output |
|---|---|---:|---|
| Empty | `SPEC-AUDIT.empty` | 0 | `#Top` |
| Symbolic nonempty | `SPEC-AUDIT.symbolic-nonempty` | 0 | `#Top` |
| Ascending example | `SPEC-AUDIT.example-ascending` | 0 | `#Top` |
| Descending example | `SPEC-AUDIT.example-descending` | 0 | `#Top` |

The unmodified aggregate command
`kprove spec.k --definition proof-kompiled --spec-module SPEC` also exited 0
and printed `#Top`. Exact commands, statuses, and output are in
`03-kprove-*.log`; the labeled spec is
`/audit-output/evidence/spec-audit.k`.

## 4. Adequacy and real-program pinning

The four entry claims mean:

1. On the exact translated body and empty input, execution consumes the program,
   leaves the input `nil`, and returns `nil`.
2. On the exact translated body and any `cons(F, REST)` satisfying
   `nonnegative(cons(F, REST))`, execution consumes the program, leaves that
   complete input unchanged, and returns exactly
   `expectedSort(cons(F, REST))`.
3. The six-element ascending example returns exactly `[0,1,2,3,4,5]`.
4. The seven-element descending example returns exactly `[6,5,4,3,2,1,0]`.

The symbolic claim is not size-bounded: `REST` is an arbitrary finite
`IntList`, and K `Int` is unbounded. Together with the separate empty claim it
covers the complete source-contract domain. Its postcondition contains no fresh
or unconstrained result variable.

`/audit-output/evidence/pinning_check.py` balanced-parses each of the four
`Module(...)` terms in `/candidate/spec.k` and mechanically compares it with
the trusted regenerated `solution.mpy`. All four are constructor-identical and
are immediately followed by `invoke("sort_array", ...)`.

Satisfying entry states are:

- empty claim: `INPUT = nil`;
- symbolic claim: `F = 0`, `REST = cons(1,nil)`, for which `nonnegative` is
  true;
- the two literal example inputs for their ground claims.

For the symbolic witness `[0,1]`, the formal result is ascending `[0,1]`;
both Python implementations and the fresh K execution produce that value. The
other three witnesses likewise occur in both the differential and K execution
logs.

A separate body-sensitivity mutation changes the parity comparison in the
executed `Module` term from `% 2 == 0` to `% 2 == 1`, while leaving the
postcondition unchanged. It builds, but `kprove` exits 1 with
`WarnStuckClaimState` and displays the unequal `sortFlag(... == 0)` and
`sortFlag(... == 1)` results. `[0,1]` is a concrete satisfying witness with
opposite outcomes. See `/audit-output/evidence/spec-body-mutation.k` and
`04-body-sensitivity.log`.

The lack of an automatic source-to-spec regeneration step is a maintenance
observation only; byte regeneration plus constructor comparison pins this
immutable candidate.

## 5. Rule-by-rule static soundness review

### Syntax and configuration inventory

`/candidate/semantic.k:8-33` declares:

- `Module(Module(Stmt))`;
- statements `FuncDef(String, Params, Stmt)` and `Return(Expr)`;
- `Params(String)`;
- expressions `Name`, `Int`, two- and three-argument `Call`, `KwArg`,
  `BoolOp`, `Compare`, `CmpOp`, `BinOp`, `UnaryOp`, and `Subscript`;
- lists `nil` and `cons(Int, IntList)`; and
- values `ListVal`, `IntVal`, `BoolVal`, and `NoneVal`.

`/candidate/semantic.k:43-45` adds control terms `invoke`, `execute`, and
`finish`. Lines 62, 92-99, 120-121, and 129-133 declare the function symbols
`eval`, `lenVal`, `sortedVal`, `andVal`, `nonemptyVal`, `compareVal`, `binVal`,
`unaryVal`, `subscriptVal`, `ilen`, `ilast`, `sortAsc`, `insertAsc`,
`sortFlag`, `reverse`, and `reverseAcc`.

`/candidate/verification.k` adds `expectedSort`, `endpointEven`,
`nonnegative`, `ascending`, and `descending`.

There are no local priority, `owise`, `[simplification]`, `[concrete]`,
`[functional]`, macro, anywhere, or proof-local ordinary operational rules.
There are no fresh or opaque result-bearing local symbols. Partial functions
can remain unreduced outside their declared subset; every form reached by the
submitted program is covered.

The configuration (`semantic.k:47-52`) has exactly the state required here:
the computation, immutable mathematical input value, and result value. It
initializes execution as the parsed module followed by an invocation on the
same `$INPUT`.

The translated program uses exactly `Module`, `FuncDef`, `Params`, `Return`,
`Call(sorted,...)`, `Name`, `KwArg(reverse,...)`, `BoolOp(and,...)`,
`Compare/CmpOp` for `>` and `==`, `Call(len,...)`, `BinOp` for `+` and `%`,
`Subscript` at `0` and `-1`, `UnaryOp(-,...)`, and integer literals. Each maps
to the declarations and rules below.

### `semantic.k`: all 40 local rules

| IDs / lines | Exact rule inventory | Classification and decision |
|---|---|---|
| S1, 54-55 | `Module(FuncDef(F,Params(P),BODY)) ~> invoke(F,V) => execute(BODY,P \|-> V)` | Ordinary operational rule. It checks the invoked name by the repeated `F`, binds the sole parameter, and preserves the continuation. Sound for the exact one-function module. |
| S2, 57 | `execute(Return(E),ENV) => finish(eval(E,ENV))` | Ordinary return evaluation. Sound; the language subset has no other statement or frame. |
| S3, 58 | `finish(V) => .K` and `<result> _ => V` | Ordinary completion. Sound; it consumes only `finish` and updates only the result cell. |
| S4-S5, 63-64 | `eval(Name(...))`; `eval(Int(...))` | Definitional expression equations. Lookup is exact in a unique-key K `Map`; integer injection is faithful. |
| S6, 66-67 | two-argument `Call(Name("len"),E)` | Operational equation for the external `len` primitive. Sound on the list value used here. |
| S7, 69-70 | three-argument `Call(Name("sorted"),E,KwArg("reverse",R))` | External-primitive bridge to `sortedVal`. It does not skip program-defined code. On this side-effect-free, well-typed program, unspecified subterm rewrite order has no observable difference. |
| S8, 72-73 | `BoolOp("and",E1,E2)` to `andVal(eval(E1),E2,ENV)` | Preserves short-circuiting by leaving `E2` unevaluated. Sound because the used first operand is Boolean. |
| S9, 77-78 | specialized `len(E) > 0` to `nonemptyVal(eval(E))` | Exact for finite lists; it exposes list shape without changing truth. It is disjoint from S10 by comparator. |
| S10, 80-81 | equality comparison to `compareVal("==",...)` | Sound for the integer operands reached here. |
| S11-S13, 83-90 | `BinOp`, `UnaryOp`, and `Subscript` dispatch | Pure definitional dispatch. Used operator/index cases are covered below; unsupported cases visibly remain partial. |
| S14-S15, 101-103 | `lenVal(ListVal(L))`; `sortedVal(ListVal(L),BoolVal(B))` | `lenVal` is exact. `sortedVal` is the explicit trusted semantics for Python's external `sorted`; `sortFlag` is fully defined by S31-S40. |
| S16-S17, 105-106 | `andVal(false,...)`; `andVal(true,E,ENV)` | Disjoint and complete for Boolean first operands. Crucially, the false rule never evaluates `E`. |
| S18-S19, 108-109 | `nonemptyVal(nil)`; `nonemptyVal(cons(...))` | Disjoint, complete, and mathematically exact. |
| S20, 111 | integer equality | Delegates to trusted K `==Int`; exact. |
| S21-S23, 113-115 | integer `+`, `%`, and unary `-` | Delegate to K integers. Inputs are non-negative where Python/K remainder conventions could otherwise differ; exact on the theorem domain. |
| S24, 117 | index `0` of `cons(I,IS)` | Exact; empty index 0 remains stuck rather than fabricating a value. |
| S25, 118 | index `-1` of any `ListVal(L)` to `ilast(L)` | Correct when `L` is nonempty, which is the only reachable call in this program. It is over-broad for `L=nil`; see the concrete witness below. |
| S26-S27, 122-123 | `ilen(nil)`; recursive `ilen(cons(...))` | Disjoint, complete, structurally descending, and exact. |
| S28-S30, 124-126 | singleton `ilast`; recursive non-singleton `ilast`; `ilast(nil)=>0` | S28-S29 are disjoint, descending, and exact for nonempty lists. S30 totalizes a mathematical helper with a value that is not Python empty-list indexing; combined with S25 it is the identified out-of-path defect. |
| S31-S32, 135-136 | `sortAsc(nil)`; insertion-sort recursion | Disjoint, complete, and structurally descending. |
| S33-S35, 138-140 | insertion into nil, `I <= J`, and `I > J` | The guarded branches are disjoint and exhaustive over K integers. They preserve the multiset and insert at the first ordered position. |
| S36-S37, 142-143 | `sortFlag` false/true | Disjoint and complete for `Bool`; false returns insertion sort and true reverses it. |
| S38, 145 | `reverse(L) => reverseAcc(L,nil)` | Truthful definitional entry. |
| S39-S40, 146-147 | empty/nonempty `reverseAcc` | Disjoint, complete, structurally descending, and exact. |

All `[total]` declarations have complete, compatible equations on their K
sorts: `ilen`, `sortAsc`, `insertAsc`, `sortFlag`, `reverse`, `reverseAcc`,
`expectedSort`, `nonnegative`, `ascending`, and `descending`. Candidate
`ilast` is syntactically total only because of S30; its equations are
mathematically consistent as an arbitrary totalization, but S25 incorrectly
exposes that totalization as Python indexing.

### `verification.k`: all 11 local rules

| IDs / lines | Rule inventory | Classification and decision |
|---|---|---|
| V1-V2, 9-11 | `expectedSort(nil)` and `expectedSort(cons(...))` | Truthful postcondition definition. The cases are disjoint and complete. It does not rewrite operational program terms. |
| V3, 14-15 | `endpointEven(cons(...))` | Truthful on its deliberately nonempty domain; every use is guarded structurally. |
| V4-V5, 23-24 | `nonnegative(nil/cons)` | Disjoint, complete, descending, and exactly states the prompt's element domain. |
| V6-V8, 26-29 | `ascending` for nil, singleton, and length at least two | Structurally disjoint and complete; recursive call descends. These observers are truthful but do not contribute to claim closure. |
| V9-V11, 31-34 | corresponding `descending` rules | Structurally disjoint and complete; truthful and unused by the target claims. |

`expectedSort` shares the already-defined `sortFlag` external-primitive meaning
with operational `sortedVal`. That makes the reachability theorem conditional
on the generated semantics of the standard-library primitive; it does not
constitute an oracle for any program-defined function. The candidate's
function body still executes through S1-S25, and the proof establishes the
direction predicate independently.

### Concrete false-rule witness and containment

The function body `return array[-1]` on the contract-domain input `[]` raises
`IndexError` in CPython, while the candidate semantics returns `IntVal(0)`.
This is the required concrete false-conclusion witness for S25 plus S30:

- `/audit-output/evidence/empty_subscript_witness.py`
- `/audit-output/evidence/empty_subscript_witness.mpy`
- `/audit-output/evidence/05-empty-subscript-python.log`
- `/audit-output/evidence/05-empty-subscript-k.log`

That body is not the submitted body. In the submitted program, S16 handles the
false `len([]) > 0` condition and never evaluates either subscript. For every
nonempty input, S25 receives a `cons`.

I confirmed proof independence mechanically by narrowing S25 to `cons`, making
`ilast` partial, deleting S30, rebuilding, and reproving the unmodified complete
spec. The narrowed build exits 0 and all claims still produce `#Top`; see
`/audit-output/evidence/semantic-narrowed.k`,
`05-narrowed-kompile.log`, and `05-narrowed-proof.log`. Therefore the false
out-of-path rule cannot make a false target conclusion provable. It is a
non-fatal generated-semantics hygiene concern, not a legitimacy failure.

No rule encodes the whole task answer as an operational shortcut, fabricates a
fresh result, replaces the submitted function body, or changes an observable
cell that the real operation would preserve.

## 6. Fresh non-vacuity test

The candidate supplied no vacuity artifact, so there was nothing to trust. I
created `/audit-output/evidence/spec-vacuity.k` from the labeled scratch spec.
Only the ascending example's required result was changed from
`[0,1,2,3,4,5]` to the demonstrably false `[5,4,3,2,1,0]`. Its precondition is
satisfied by the literal prompt input `[2,4,3,0,1,5]`.

The dry-run build exits 0 (`06-vacuity-build.log`). The actual proof exits 1
with `WarnStuckClaimState`; its residual final configuration contains the real
ascending result `[0,1,2,3,4,5]`, which does not unify with the mutated
destination (`06-vacuity-proof.log`). This is an expected unmet result
obligation, not a parser, import, timeout, or unrelated backend failure.

The separate body-sensitivity failure in Stage 4 tests execution fidelity; this
Stage 6 mutation tests result constraint.

## 7. Proven versus assumed accounting

### Formally established

Under the submitted generated K semantics, the exact constructor translation
of `/candidate/solution.py`, followed by `invoke("sort_array", input)`, has the
following partial-correctness property:

- on `nil`, it consumes `<k>` and returns `ListVal(nil)`;
- on every arbitrary finite nonempty `IntList` whose elements satisfy
  `nonnegative`, it consumes `<k>` and returns exactly
  `ListVal(expectedSort(input))`; and
- the `<input>` cell is unchanged.

`expectedSort` is `sortAsc` when the first-plus-last sum is odd and
`reverse(sortAsc(...))` when it is even. This covers arbitrary finite length and
unbounded non-negative integers, not examples or bounded unrollings.

### Trust ledger and limitations

| Boundary | Dependents | Evidence and judgment |
|---|---|---|
| K 7.1.293 parser, Haskell/LLVM backends, and imported `INT`, `BOOL`, `STRING`, and `MAP` theories | All builds, executions, and proofs | Ordinary toolchain trust. Version and fresh-build evidence are recorded. Acceptable. |
| Trusted `py2mpy.py` translation scheme | Source-to-constructor identity | Trusted mount plus byte regeneration and four constructor-level comparisons. Acceptable. |
| Generated list/value semantics for this Python subset | Meaning of every reachability step | Audited rule-by-rule and concretely compared on nine normal/boundary runs. Partial unsupported syntax stops visibly. Acceptable for the real program, with the S25/S30 concern explicitly contained. |
| `sortedVal`/`sortFlag` as the semantics of Python's external `sorted` | Exact returned list | `sortFlag` is not opaque: it is a complete insertion sort plus reverse. Its ordering/permutation interpretation follows by ordinary structural induction, not a separate machine-checked connection theorem. Full-program K/Python runs and 2,047 Python canonical differentials give finite supporting evidence. This is a non-fatal informal standard-library bridge. |
| Mathematical value lists rather than Python heap objects | The non-mutation/copy clause | The theorem proves the input value cell unchanged, but has no allocation or identity cell and therefore does not prove `result is not input`. The actual candidate and canonical returned distinct lists in every differential case. Because the contract's material observable requirement is non-mutation and the implementation uses `sorted`, this is a non-fatal adequacy limitation. |
| Python exceptions and behavior outside the submitted path | Reuse of the generated semantics | Empty negative indexing is modeled incorrectly, with the recorded witness. The submitted empty path short-circuits, and deletion of the defect leaves the proof unchanged. Not a false target conclusion. |

There are no proof-local opaque symbols, assumed lemmas, simplification rules,
operational bridges for program-defined code, or empirical facts used as a
substitute for `kprove`.

Gate summary:

- Dynamic clean reconstruction: pass.
- Real-program soundness, result constraint, and pinning: pass.
- Full material source-contract domain: pass.
- Reusable-semantics fidelity and audit evidence: legitimate with the two
  non-fatal limitations above.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
