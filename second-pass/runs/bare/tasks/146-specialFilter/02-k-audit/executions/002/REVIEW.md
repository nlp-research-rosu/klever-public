# Independent adversarial review: 146-specialFilter

The candidate reconstructs successfully and its submitted claims are
non-vacuous, body-sensitive claims about the submitted function body. They do
not, however, prove the HumanEval contract over arbitrary integer arrays. The
only symbolic inputs are singleton lists, and positive symbolic elements stop
at 999. Under this benchmark's explicit mapping, that material restriction is
`FAIL / NOT_LEGIT`, even though the bounded theorem itself closes.

All candidate and generation material was treated as untrusted evidence. No
candidate-built definition or cache was reused. Reviewer commands and bounded
logs are indexed in [evidence/COMMANDS.md](evidence/COMMANDS.md).

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `146-specialFilter`, condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- candidate `/candidate`, trusted inputs under `/reference`, and generation
  records under `/generation-evidence`.

The campaign block in `/audit-input.json` is exactly equal to
`/audit-campaign-lock.json`, whose independent SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
The required legacy-selected records are real regular files, the trace is a
real directory containing one regular JSONL file, and neither required tree
contains a symlink or unsupported node. I read and checked `/run.json`,
`/task.json`, `/generation-result.json`, `invocation.json`, `metrics.json`,
the present `usage.json`, `codex-last.txt`, `codex-output.log`, `prompt.txt`,
the legacy records named by the invocation, and all 286 structured trace
records. Historical runtime metrics are absent, which is permitted for this
record layout.

Every directly recorded file SHA-256 matches, including:

- canonical `a72b635e...45be7`;
- trusted/candidate prompt `310a71d2...eb917`;
- trusted/candidate translator `406485ea...db16`;
- run/task/result/invocation/metrics/usage;
- raw generation log, final message, prompt, and trace JSONL.

The independently reimplemented public pipeline tree digest is
`aabf777e...74630` for `/candidate`, exactly matching both the invocation and
stage-result workspace digest. The corresponding trace digest is
`d868e309...b14b`, exactly matching `usage.json`. `/audit-input.json` also
contains differently serialized launcher aggregate values (`17b62e...` and
`ebd6fc...`); its serialization algorithm is not declared, so those values are
not compared as though they were the public pipeline digest. The underlying
file hashes, trace hash, and official pipeline workspace/trace digests are
internally consistent. See [01-integrity.log](evidence/01-integrity.log) and
[integrity_audit.py](evidence/integrity_audit.py).

The generated-semantics boundary is intact:
`/reference/reference-semantics` does not exist and the candidate does not
contain `reference-semantics`. Candidate `prompt.py` and `py2mpy.py` are
byte-identical to their trusted mounts. All required proof source artifacts
exist as regular files. I found no infrastructure breach, so a candidate
verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For an array of integers, return the number of elements that are strictly
greater than 10 and whose first and last decimal digits are both odd. Empty
arrays return 0, repeated qualifying values are counted repeatedly, and
negative values cannot qualify because of the strict `> 10` guard. This is the
behavior stated in `/reference/prompt.py` and implemented by
`/reference/canonical.py`.

`/candidate/solution.py` uses a different but equivalent integer algorithm:
for each value above 10 it repeatedly floor-divides a positive copy by 10 to
obtain the leading digit, tests that digit's parity, tests the original
integer's parity for the trailing digit, and increments `count`.

Using the trusted translator:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
```

produced SHA-256 `893118e8...8966`, byte-identical to the submitted
`solution.mpy`; see [02-regeneration.log](evidence/02-regeneration.log).

The independent differential test imports the trusted canonical entry point
and the copied submitted entry point separately. It checks both prompt
examples, empty and strict-boundary cases, repetitions, all singleton integers
from -250 through 2000, decimal-width transitions, very large integers,
representative pairs, and 1,500 deterministic generated arrays. It performed
4,108 comparisons with zero mismatches:
[differential_test.py](evidence/differential_test.py) and
[02-differential.log](evidence/02-differential.log).

This is strong finite evidence that the Python rewrite implements the intended
integer behavior; it is not a universal proof.

## 3. Clean proof reconstruction

K v7.1.293 and Python 3.10.12 were available
([00-toolchain.log](evidence/00-toolchain.log)). Only source files copied to
`/tmp/audit-work/candidate-src` were used. Fresh Haskell definitions were built
with:

```text
kompile semantic.k --backend haskell --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-audit-kompiled

kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-audit-kompiled
```

Both exited 0; see [03-kompile-semantic.log](evidence/03-kompile-semantic.log)
and [03-kompile-verification.log](evidence/03-kompile-verification.log).

The submitted module itself parses and executes to a stored
`"specialFilter"` binding under the fresh generated semantics
([03-krun-submitted-module.log](evidence/03-krun-submitted-module.log)).
Direct `Run(Module(...), Call(...))` executions—not the proof wrapper—gave:

| Input | K result | Canonical Python | Submitted Python |
|---|---:|---:|---:|
| `[15,-73,14,-15]` | 1 | 1 | 1 |
| `[]` | 0 | 0 | 0 |
| `[10,11,99,100,101,1001]` | 4 | 4 | 4 |
| two 50-digit boundary values | 1 | 1 | 1 |

The preserved inputs and logs are `run-normal.mpy`, `run-empty.mpy`,
`run-boundaries.mpy`, `run-huge.mpy`, `03-krun-*.log`, and
[03-python-concrete-oracle.log](evidence/03-python-concrete-oracle.log).
These runs exercise zero/nonzero `for`, false/true `if`, zero/multiple `while`,
all three used arithmetic operators, all three comparisons, call, return, and
huge mathematical integers.

The original positive command

```text
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC
```

exited 0 and printed `#Top`
([03-kprove-all.log](evidence/03-kprove-all.log)). To check every positive
claim independently, I mechanically copied the claims and added labels `c01`
through `c11` without changing their terms or conditions
([spec-labelled.k](evidence/spec-labelled.k)). All eleven filtered commands
exited 0 and printed `#Top`; the exact expanded commands and individual logs
are in [evidence/COMMANDS.md](evidence/COMMANDS.md).

Thus reconstruction succeeds. The eventual failure verdict is not based on an
old trace, candidate `#Top`, parser error, timeout, or tool failure.

## 4. Adequacy and real-program pinning

### What each entry claim says

Every claim starts with empty `<functions>` and `<env>` maps and ends with an
exact `intVal`, empty maps, and no remaining computation.

| Claim | Plain-language precondition and postcondition |
|---|---|
| c01 | Exact first prompt list returns 1. |
| c02 | Exact second prompt list returns 2. |
| c03 | The exact empty list returns 0. |
| c04 | Exact list `[-999,-11,0,1,9,10]` returns 0. |
| c05 | One exact 12-element parity/width list returns 4. |
| c06 | Exact repeated-value list returns 3. |
| c07 | For every integer `N <= 10`, singleton `[N]` returns 0. |
| c08 | For `11 <= N <= 99` with odd units and tens digits, singleton `[N]` returns 1. |
| c09 | For the complementary parity case in `11..99`, singleton `[N]` returns 0. |
| c10 | For `100 <= N <= 999` with odd units and hundreds digits, singleton `[N]` returns 1. |
| c11 | For the complementary parity case in `100..999`, singleton `[N]` returns 0. |

All preconditions are satisfiable. Ground witnesses respectively are the six
literal claim inputs followed by `N=10`, `11`, `12`, `111`, and `112`. Every
claimed result agrees with both Python implementations; see
[precondition_witnesses.py](evidence/precondition_witnesses.py) and
[04-precondition-witnesses.log](evidence/04-precondition-witnesses.log).

### Program identity

`SFTest(ARG)` expands to `Run(Module(exact function binding and body),
Call(Name("specialFilter"), ARG))`, followed by a cleanup marker. The trusted
regeneration and a constructor-token comparison show that the `Module` term in
this rule is exactly the regenerated `solution.mpy` module. The only
normalization is that the translator omits empty `Stmts` list items while
`verification.k` spells the same K list unit as `.Stmts`. The called binding is
exactly `"specialFilter"` with `ARG`; see
[constructor_compare.py](evidence/constructor_compare.py) and
[04-constructor-compare-fixed.log](evidence/04-constructor-compare-fixed.log).

There are no loop/helper claims and no summary replacing the function body.
The semantics executes the actual assignments, list loop, nested branches,
decimal loop, arithmetic, call, and return. A fresh body mutation changed the
executed outer threshold from `>10` to `>100`. It built successfully, but the
first example proof failed with reachable `intVal(0)` against required
`intVal(1)`, demonstrating body sensitivity. Artifacts:
[verification-body-mutant.k](evidence/verification-body-mutant.k),
[spec-body-mutant.k](evidence/spec-body-mutant.k), and
[04-kprove-body-mutation.log](evidence/04-kprove-body-mutation.log).

The proof-local `clearFunctions` operation is post-call test-harness cleanup.
It changes the semantics' function-map cell—the direct `Run` retains the
binding, while `SFTest` clears it—but it runs only after the returned value and
does not replace or influence the function computation in these empty-
continuation claims. This instrumentation should not be described as an exact
full-configuration equivalence to direct module execution; it is adequate for
the returned-value theorem actually stated.

### Material domain gap

The symbolic theorem is not a contract for arrays:

- all five symbolic claims require exactly one element;
- positive symbolic elements are bounded by 999;
- no invariant or recursive summary proves arbitrary digit width;
- the multi-element claims are six fixed examples, not arbitrary lists.

The fixed c05 example happens to contain several values over 999, but it proves
only that one complete list. Source-valid `[1001]`, `[11,11]`, and a singleton
50-digit qualifying integer are outside every claim, although both Python
implementations return 1, 2, and 1 respectively. See
[coverage_gap_witnesses.py](evidence/coverage_gap_witnesses.py) and
[04-coverage-gap.log](evidence/04-coverage-gap.log). The fresh K concrete runs
also show the semantics can execute such values, so the restriction is in the
theorem, not forced by the program or toolchain.

This is a material narrowing of an unrestricted integer-array HumanEval
domain. The bounded proof does not establish the requested contract.

## 5. Rule-by-rule static soundness review

There are no generated helper K files. The complete local inventory is
`semantic.k`, `verification.k`, and the eleven reachability claims in `spec.k`.
The mechanical declaration listing is
[05-rule-inventory.log](evidence/05-rule-inventory.log).

### Syntax, configuration, and attributes

`MPY-SYNTAX` contains these 21 productions:

- `Program`: `Module(Stmts)`, `Run(Program,Expr)`;
- list/plumbing: `Stmts`, `Exprs`, `Params(Strings)`, `Strings`;
- `Stmt`: `FuncDef`, `Assign`, `AugAssign`, `If`, `For`, `While`, `Return`;
- `Expr`: `Int`, `Bool`, `Name`, `ListExpr`, `BinOp`, `Compare`, `Call`;
- `CmpOp(String,Expr)`.

`MPY` adds 28 productions:

- values `intVal`, `boolVal`, `listVal`, `none`, plus `Values`;
- `function(String,Stmts)`;
- 20 control KItems: `exec`, `moduleDone`, `collectHead`, `prepend`,
  `assignTo`, `augment`, `binLeft`, `binRight`, `cmpLeft`, `cmpRight`,
  `branch`, `startFor`, `setLocal`, `loopFor`, `whileTest`, `invoke`,
  `makeReturn`, `returnScan`, `implicitReturn`, `restoreEnv`;
- functions `#bin(String,Value,Value)` and
  `#cmp(String,Value,Value)`.

`verification.k` adds `SFTest(Expr)` and `clearFunctions`. The configuration
has exactly `<k>`, `<functions>`, and `<env>` cells. There is no heap,
allocation, exception, I/O, or mutable collection state because the submitted
program uses none.

`#bin` and `#cmp` are the only local `[function, total]` declarations. There
are no `[functional]`, `[simplification]`, `[concrete]`, hook, opaque-result,
or explicit priority declarations. The only priority-like attribute is
`[owise]` on return unwinding. There are no proof-local equations, lemmas,
oracles, or auxiliary claims.

### All 49 semantic rules and two verification rules

The following grouping is exhaustive; each listed line denotes one rule (a
line range only joins a multi-line rule):

| Rules | Count | Review |
|---|---:|---|
| `semantic.k:78`, `:79`, `:80` | 3 | `Run` sequences module before expression; `Module` sequences statements before `moduleDone`; `moduleDone` disappears. Correct for the constructor harness. |
| `:82`, `:83` | 2 | Empty and head/tail statement execution. Correct order. |
| `:85-86` | 1 | Stores the named one-parameter function body in the function map. Correct for the submitted binding. |
| `:88`, `:89`, `:90` | 3 | Integer/boolean literals and environment lookup. Correct; unbound names visibly stick rather than fabricating a value. |
| `:92`, `:93`, `:94`, `:95`, `:96` | 5 | Empty/singleton/multi expression lists evaluate left-to-right and prepend in source order. The singleton/multi overlap, if normalized by list parsing, has the same result. |
| `:98-100` | 2 | Assignment evaluates the RHS then updates the named environment entry. Correct for used assignments. |
| `:102-104` | 2 | Augmented assignment evaluates the RHS, reads an existing binding, and applies `#bin`. Python's exact general lvalue/RHS order is broader, but the only use is side-effect-free `count += 1`, where this is exact. |
| `:106`, `:107`, `:108` | 3 | Binary operands evaluate left-to-right, then call `#bin`. Correct. |
| `:110`, `:111-112`, `:113-114` | 3 | Integer `+`, division, and remainder equations; divisors must be nonzero. Addition and every target-reachable division/remainder case are correct. The global negative-operand issue is detailed below. |
| `:116`, `:117`, `:118` | 3 | Comparison operands evaluate left-to-right, then call `#cmp`. Correct. |
| `:120`, `:121`, `:122` | 3 | Integer `>`, `>=`, and `==` are truthful, disjoint equations. |
| `:124`, `:125`, `:126` | 3 | Condition first, then exactly the true or false statement list. Correct for boolean guards. |
| `:128`, `:129`, `:130-131`, `:132`, `:133-134` | 5 | Evaluates list iterable once, assigns each element in order, executes the body, and continues; empty lists stop. Return unwinding can discard the loop continuation, as Python return should. |
| `:136`, `:137-138`, `:139` | 3 | Re-evaluates the while guard each iteration; false stops. Correct and returns to a stable loop head. |
| `:141`, `:142-145` | 2 | Evaluates the one argument, looks up the exact function binding, installs a fresh local environment, and schedules implicit return plus restoration. Resolution occurs after argument evaluation rather than fully modeling general Python callable evaluation, but the fixed direct name and side-effect-free list argument make it exact here. |
| `:147`, `:148`, `:149`, `:150`, `:151`, `:152-153` | 6 | Evaluates return expression, scans/discards pending function-body KItems until `implicitReturn`, produces the value, and restores caller environment; absent explicit return produces `none`. The `[owise]` rule gives the specific `implicitReturn` case precedence. Correct on all invocation-produced control stacks. |
| `verification.k:11-27` | 1 | Expands `SFTest` to the exact module and call; it does not summarize or bypass execution. |
| `verification.k:29-30` | 1 | Clears the function map after obtaining a value. Correct as explicit harness cleanup; it is not a universal full-state equivalence to execution without cleanup. |

### Construct coverage and state/control fidelity

Every construct in `solution.mpy` maps to the rules above: `Module` and
`FuncDef` (78-86), `Assign` (98-100), `For` (128-134), `If` (124-126),
`While` (136-139), `Return` (147-153), `Int`/`Name` (88/90), `ListExpr`
(92-96), `BinOp` (106-114), `Compare`/`CmpOp` (116-122), `Call` (141-145),
and `AugAssign` (102-104). `Bool` is declared but unused. Concrete tests
exercise every used construct and every material branch.

Evaluation is deterministic on target states. Arguments and operands are
evaluated in source order; environment changes are explicit; function calls
save and restore the caller map; return unwinds pending loop/statement
continuations; there is no hidden result-bearing state. The only extra
observable state effect is the already disclosed `clearFunctions` harness
cleanup.

### Equation and totality findings

The three `#bin` operation strings and three `#cmp` strings are pairwise
disjoint, so their equations do not conflict. The equations cover every
target-reachable application: `+` on integer `count` and 1, `//` on a positive
`first` and 10, `%` on positive values and 2, and the three listed integer
comparisons.

Two language-wide declarations are nevertheless over-broad:

1. K's `/Int` and `%Int` used here truncate toward zero/sign the remainder
   differently from Python floor division/modulo on negative operands. The
   concrete generated-language witnesses `-3 // 2` and `-3 % 2` reduce to
   `-1` and `-1` in K, while Python returns `-2` and `1`; see
   [05-negative-division.log](evidence/05-negative-division.log),
   [05-negative-modulo.log](evidence/05-negative-modulo.log), and
   [05-python-negative-arithmetic.log](evidence/05-python-negative-arithmetic.log).
   These are concrete false equation witnesses over the declared language.
   The actual target cannot reach either bad case: division/remainder occur
   only inside `num > 10`, so both `num` and `first` are positive. Therefore
   this mismatch did not enable a false conclusion for any intended target
   input and is not the basis of the domain-failure verdict. It does prevent
   treating the generated language as a generally sound Python-integer
   semantics without narrowing the rule guards or implementing Python floor
   arithmetic.

2. `[total]` is false as a coverage assertion over the declared
   `String × Value × Value` domains. For example,
   `#bin("*",intVal(1),intVal(2))` remains as a residual term
   ([05-totality-gap.log](evidence/05-totality-gap.log)); unsupported value
   sorts and comparison strings are likewise uncovered. This probe does not
   establish a false result conclusion, so I classify it as a totality/evidence
   gap rather than claim that it proved a wrong target result. No submitted
   claim reaches an uncovered application.

No rule encodes the task's answer, introduces an unconstrained result oracle,
replaces a property-bearing computation, or silently fabricates a target
result. The positive proofs close by bounded symbolic/concrete execution.

## 6. Fresh non-vacuity test

I did not rely on any candidate mutation. The fresh
[spec-vacuity.k](evidence/spec-vacuity.k) copies c08's satisfiable
precondition but changes its result from `intVal(1)` to `intVal(0)`.
`N=11` is an explicit satisfying witness and both Python implementations
return 1.

The dry run parsed and built successfully with exit 0
([06-vacuity-dry-run.log](evidence/06-vacuity-dry-run.log)). The real proof:

```text
kprove spec-vacuity.k --definition verification-audit-kompiled \
  --spec-module SPEC-VACUITY
```

exited 1 with `WarnStuckClaimState`. Its reachable residual contains
`intVal(1)` and the still-satisfiable symbolic conditions, while the mutated
destination requires `intVal(0)`; see
[06-vacuity-kprove.log](evidence/06-vacuity-kprove.log). This is a meaningful
unmet result obligation, not a parser/import error, timeout, or unreachable
mutation. The bounded theorem is result-constraining and non-vacuous.

## 7. Proven versus assumed accounting

### Formally established

Under the freshly compiled candidate semantics, the exact submitted
`specialFilter` constructor body reaches the exact return values for the six
ground configurations and five bounded singleton families listed in stage 4.
The maps are initially empty; the call environment is restored; the proof
harness clears the function map. The false-result and body mutations show that
claim closure depends on both the result and the executed body.

That is all. In particular, there is no formal result for arbitrary array
length, arbitrary positive integer width, or the general counting relation.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K compiler, Haskell backend, and K reachability implementation | All `krun`/`kprove` evidence | Standard unavoidable low-level trust boundary; version recorded. |
| Imported K `INT`, `BOOL`, and `MAP` primitives | Arithmetic, guards, environment/function updates, all claims | Acceptable for mathematical integers and maps. Target-reachable division/remainder operands are positive. |
| Trusted `py2mpy.py` translation | Source-to-constructor identity | Authorized trusted input; byte regeneration succeeds. Constructor comparison mechanically connects the proof term to that output. |
| Generated `semantic.k` | Meaning of every K execution/proof | Not assumed: audited exhaustively above and tested concretely. General negative floor arithmetic and false `[total]` scope remain disclosed limitations. |
| `SFTest` and `clearFunctions` harness | Every formal claim | Exact body/call execution plus post-result cleanup. Cleanup affects only the semantic function-map cell after the value; it is not a source operation or a universal context equivalence. |
| Canonical-vs-submitted Python equivalence | Implementation-to-intent bridge | 4,108 finite differential checks and direct reasoning support it; this testing is empirical, not a theorem. |
| Decimal-leading-digit reasoning for arbitrary widths/lists | Intended HumanEval property | Not assumed legitimately and not proved. This is precisely the missing theorem. |

There are no opaque result symbols, empirical oracles inside the K proof,
proof-local simplifications, connection lemmas, or circular summaries.
Candidate prose and generation traces were not used as proof substitutes.

### Gate and verdict rationale

- Fresh verification: pass—all eleven submitted claims print `#Top`.
- Real-body/result non-vacuity: pass for those claims.
- Language-wide semantics validation: limited by the disclosed negative
  floor-arithmetic and totality issues, though target-reachable operations are
  not shown false.
- Intent adequacy: fail materially—the theorem consists of fixed examples and
  bounded singleton families, not the unrestricted integer-array contract.
- Evidence auditability: pass for the reconstructed commands and retained
  artifacts, with finite testing labeled as finite.

In Kit terminology, the strongest charitable reading is a sound bounded
theorem with a material Gate B limitation. The benchmark prompt explicitly
maps such HumanEval-domain narrowing to `FAIL / NOT_LEGIT`, not
`CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
