# Independent adversarial audit: 146-specialFilter

The candidate reconstructs successfully and its submitted claims are
non-vacuous, but those claims do not prove the HumanEval contract. They cover
six fixed lists and five classes of singleton lists only. There is no theorem
for an arbitrary-length list, no list-loop invariant, and no symbolic coverage
for values at least 1000. This is a material adequacy failure, so the candidate
is not a legitimate proof of the requested program-correctness result.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`. `/reference/reference-semantics`
does not exist, so the trusted mount agrees with that mode. I did not search
for or use any hidden reference semantics.

All required candidate source and record artifacts are regular files:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, and `spec.k`. The one structured JSONL trace is also a
regular file. There are no symlinks in the source tree outside the ignored
compiled directories. The detailed type and SHA-256 inventory is in
[stage1-integrity.log](evidence/stage1-integrity.log).

The candidate's `prompt.py` is byte-identical to `/reference/prompt.py`
(SHA-256
`310a71d2feca4b63bf4ab0279cac60820a61a57157a413efd62823e6c69eb917`),
and its `py2mpy.py` is byte-identical to `/reference/py2mpy.py` (SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
There are no missing, changed, mistyped, or symlinked required source
artifacts. `prove.sh` and the two example `.mpy` files are support artifacts.
`semantic-kompiled/`, `verification-kompiled/`, and `__pycache__/` are extra
generated/cache entries; I did not copy or use them.

I copied the source artifacts and trusted inputs to
`/tmp/audit-work/146-specialFilter`; byte-for-byte copy verification is in
[stage1-scratch-copy-verification.log](evidence/stage1-scratch-copy-verification.log).
All later builds used that scratch tree.

I read all five untrusted generation records. Their claims are summarized in
[stage1-generation-claims.log](evidence/stage1-generation-claims.log).
Notably, the record contains three failed `induction-spec.k` attempts with
`WarnStuckClaimState`, after which the general induction artifact was omitted.
The final record's `KPROVE_PASSED` marker refers only to the surviving limited
claims and is not treated as audit evidence.

Stage 1 result: integrity checks pass; no infrastructure breach occurred.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

For a finite list of integers, `specialFilter(nums)` must return the number of
elements that:

1. are strictly greater than 10;
2. have an odd first decimal digit; and
3. have an odd last decimal digit.

The two required examples return 1 and 2 respectively. This restatement follows
`/reference/prompt.py` and `/reference/canonical.py`.

`solution.py` uses an equivalent arithmetic algorithm. For each `num > 10`, it
repeatedly floor-divides a local copy by 10 until only the leading digit
remains, then checks that digit and `num` modulo 2. Because that branch is
entered only for positive integers, these parity tests are equivalent to the
canonical decimal-string tests. Negative and at-most-10 values are skipped.

The exact trusted regeneration command was:

```text
python3 /tmp/audit-work/146-specialFilter/reference/py2mpy.py /tmp/audit-work/146-specialFilter/candidate/solution.py > /tmp/audit-work/146-specialFilter/candidate/regenerated-solution.mpy
```

The regenerated and submitted `solution.mpy` files are byte-identical, both
with SHA-256
`893118e8150e657871695e15b9dc070d9ad32919d7bb8b942c50b6f737898966`.
See [stage2-translation.log](evidence/stage2-translation.log).

### Independent differential test

[differential_test.py](evidence/differential_test.py) independently imports the
trusted canonical entry point and the candidate entry point. It does not reuse
K equations. The exact command and result are in
[stage2-differential.log](evidence/stage2-differential.log).

The run covered:

- both prompt examples, the empty list, threshold and digit-width boundaries,
  repeated values, and very wide integers;
- every singleton integer from -2000 through 20000;
- every list of lengths 1 through 3 over 15 fixed branch-boundary values; and
- 5,000 deterministic random lists of lengths 0 through 30 with values in
  `[-10^12, 10^12]`.

All 30,624 cases matched. The complete generated input set is preserved in
[differential-inputs.jsonl](evidence/differential-inputs.jsonl), SHA-256
`31765be0b65550ce4b3dfe8f79abf95581f55eee90744801fe59c4427511a071`.
This is finite evidence of implementation fidelity, not a universal proof.

Stage 2 result: the submitted Python program is faithful on the intended
integer-list domain, and the submitted constructor program is exactly its
trusted translation.

## 3. Clean proof reconstruction

K v7.1.293 was available directly at `/usr/bin`; `kup` was absent, but no
installation was needed. Versions and paths are in
[toolchain.log](evidence/toolchain.log).

I built two fresh definitions from source, without candidate compiled state:

```text
kompile --backend llvm semantic.k --main-module MPY --syntax-module MPY-SYNTAX --output-definition fresh-semantic-kompiled
kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module VERIFICATION --output-definition fresh-verification-kompiled
```

Both commands exited 0. The LLVM build warned that `#bin` and `#cmp`, despite
being declared `[total]`, are non-exhaustive. See
[stage3-kompile-concrete.log](evidence/stage3-kompile-concrete.log) and
[stage3-kompile-proof.log](evidence/stage3-kompile-proof.log).

The submitted spec was run unchanged:

```text
kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC
```

It exited 0 and printed exact `#Top`; see
[stage3-kprove-submitted-spec.log](evidence/stage3-kprove-submitted-spec.log).
I also split the 11 claims into separate, otherwise identical spec modules and
ran each independently. Every command exited 0 and printed exact `#Top`.
[stage3-positive-claims-summary.log](evidence/stage3-positive-claims-summary.log)
links that result to the per-claim logs under `evidence/positive-claims/`, each
of which records its exact `kprove` command and output.

For generated-semantics validation, I wrapped the freshly regenerated
`Module(...)` term in `Run(..., Call(...))` without using `SFTest`. Seven
concrete programs covered both examples, empty input, the `10/11` threshold,
digit widths through 90009, negative inputs, and 21- to 51-digit integers.
Fresh LLVM `krun`, trusted canonical Python, and candidate Python agreed in
all seven cases. The manifest and commands are in
[stage3-concrete-input-generation.log](evidence/stage3-concrete-input-generation.log),
[stage3-concrete-summary.log](evidence/stage3-concrete-summary.log), and the
per-case logs under `evidence/concrete-runs/`.

An initial reviewer harness used the internal spelling `.Exprs` in an external
`.mpy` file and had an over-escaped result regex. That preliminary parser/harness
error is preserved in
[stage3-concrete-summary-initial-harness-error.log](evidence/stage3-concrete-summary-initial-harness-error.log);
the corrected external spelling `ListExpr()` then produced the seven successful
runs above. It is not candidate evidence and does not affect the verdict.

Stage 3 result: all submitted positive claims reconstruct cleanly, and the
generated semantics executes the tested real programs correctly.

## 4. Adequacy and real-program pinning

Every claim starts with empty `<functions>` and `<env>` cells and executes an
`SFTest(...)` term. Every destination fixes the returned `intVal` to a concrete
integer and again requires both state cells to be empty. There are no
right-hand-only result variables, tautologies, or one-way result implications.

The entry claims mean:

| Claim | Precondition, in plain language | Required result | Satisfying witness |
|---|---|---:|---|
| 1 | Exact prompt list `[15,-73,14,-15]` | 1 | That list |
| 2 | Exact prompt list `[33,-2,-3,45,21,109]` | 2 | That list |
| 3 | Empty list | 0 | `[]` |
| 4 | Exact at-most-10/negative list | 0 | `[-999,-11,0,1,9,10]` |
| 5 | One exact parity/width coverage list | 4 | The listed 12 values |
| 6 | Exact repetition list | 3 | `[15,15,15,20,20]` |
| 7 | Singleton `[N]` with `N <= 10` | 0 | `N=10` |
| 8 | Singleton `[N]`, `11 <= N <= 99`, odd last and tens digits | 1 | `N=11` |
| 9 | Singleton `[N]`, `11 <= N <= 99`, not both digits odd | 0 | `N=12` |
| 10 | Singleton `[N]`, `100 <= N <= 999`, odd last and hundreds digits | 1 | `N=101` |
| 11 | Singleton `[N]`, `100 <= N <= 999`, not both digits odd | 0 | `N=100` |

All 11 witnesses satisfy their preconditions, and for every witness the claimed
result equals fresh K execution, trusted canonical Python, and candidate Python.
See [stage4-claim-witnesses-summary.log](evidence/stage4-claim-witnesses-summary.log)
and the per-claim logs under `evidence/claim-witnesses/`.

`verification.k:11-27` expands `SFTest(ARG)` into a literal copy of the
translated `specialFilter` body, calls it with `ARG`, and only then schedules
`clearFunctions`. It does not summarize or replace the function computation.
I compared the normalized `Run(Module(...), Call(...))` term from the freshly
translated program with the term produced by one `SFTest` expansion. Their
SHA-256 hashes are both
`32150c3b4f3a5ef5798e9405785c4c128ef8e3569252ae7b790cc7295cd09d63`;
see [stage4-pinning-summary.log](evidence/stage4-pinning-summary.log) and
[stage4-pinning-detail.log](evidence/stage4-pinning-detail.log). Together with
the byte-identical trusted translation, this pins the duplicated body to the
current submitted program.

The material failure is theorem scope:

- no claim accepts a symbolic `Values`/`Exprs` list or arbitrary list length;
- no claim states a count fold or list-loop invariant;
- the only unbounded symbolic claim is the skip case `N <= 10`;
- positive symbolic cases stop at 999; and
- values such as 1001 or 90009 appear only in finite ground examples.

For example, the intended input `[11, 13]` should produce 2, and `[1001]`
should produce 1. The concrete semantics and Python tests do produce those
results, but no submitted claim quantifies over either class. A successful
proof of unrelated fixed examples cannot be generalized into the requested
all-lists contract.

Stage 4 result: real-program pinning and result constraint pass for each
submitted claim; intent adequacy fails materially.

## 5. Rule-by-rule static soundness review

There are no generated helper K files. The complete local inventory is
`semantic.k`, `verification.k`, and the 11 claims in `spec.k`; a machine
inventory is preserved in [stage5-inventory.log](evidence/stage5-inventory.log).

### Syntax, functions, attributes, and configuration

`MPY-SYNTAX` declares:

- `Program`: `Module(Stmts)` and `Run(Program,Expr)`;
- list sorts `Stmts`, `Exprs`, and `Strings`, plus `Params(Strings)`;
- `Stmt`: `FuncDef`, `Assign`, `AugAssign`, `If`, `For`, `While`, and `Return`;
- `Expr`: `Int`, `Bool`, `Name`, `ListExpr`, `BinOp`, `Compare`, and `Call`;
- `CmpOp(String,Expr)`.

`MPY` declares values `intVal`, `boolVal`, `listVal`, and `none`; list sort
`Values`; stored `function(String,Stmts)`; and the internal continuation forms
`exec`, `moduleDone`, `collectHead`, `prepend`, `assignTo`, `augment`,
`binLeft`, `binRight`, `cmpLeft`, `cmpRight`, `branch`, `startFor`,
`setLocal`, `loopFor`, `whileTest`, `invoke`, `makeReturn`, `returnScan`,
`implicitReturn`, and `restoreEnv`.

The only local functions are `#bin(String,Value,Value)` and
`#cmp(String,Value,Value)`, both marked `[function,total]`. There are no opaque
symbols, simplification rules, concrete rules, proof-local lemmas, auxiliary
claims, or explicit priority rules. The sole fallback attribute is `[owise]`
on `returnScan` at `semantic.k:150`. The configuration has only `<k>`,
`<functions>`, and `<env>` cells, which are exactly the control and state
components this program needs. `verification.k` adds only `SFTest(Expr)` and
`clearFunctions`.

The `[total]` declarations are too broad. The fresh compiler diagnosed both as
non-exhaustive, and the allowed syntax includes unsupported operator/type
combinations. `Run(Module(), BinOp("-", Int(1), Int(1)))` reaches residual
`#bin("-",intVal(1),intVal(1))` and the LLVM interpreter exits 113; see
[stage5-unsupported-op.log](evidence/stage5-unsupported-op.log). This is a
declaration/coverage gap, not an oracle: no arbitrary value is fabricated, and
the real program reaches only the covered integer operators `"+"`, `"//"`,
`"%"`, `">"`, `">="`, and `"=="`.

The arithmetic equations are also broader than Python fidelity. K evaluates
`-3 /Int 2` and `-3 %Int 2` as -1, while Python evaluates `-3 // 2` as -2 and
`-3 % 2` as 1. Concrete witnesses are in
[stage5-negative-floor-div.log](evidence/stage5-negative-floor-div.log) and
[stage5-negative-mod.log](evidence/stage5-negative-mod.log). The submitted
program never applies either operator to a negative operand: the enclosing
`num > 10` branch guarantees positive `num` and `first`. Therefore these
witnesses expose an over-broad general-Python semantics, but not a false
conclusion enabled for `specialFilter` on an intended integer-list input. I do
not label the submitted theorem unsound on that basis.

A Boolean-list probe is outside the established integer-list domain and did
not terminate within a five-second bound; its bounded diagnostic is preserved
in [stage5-bool-input.log](evidence/stage5-bool-input.log). No conclusion is
drawn from that timeout.

### Used-construct map

Every constructor in `solution.mpy` is declared and has a reached operational
path:

| Program construct | Declaration | Operational rules |
|---|---|---|
| `Module`, statement sequencing | `semantic.k:6,9` | 79-83 |
| `FuncDef`, `Params` | 12-15 | 85-86 |
| `Int`, `Name` | 23-25 | 88, 90 |
| `Assign` | 16 | 98-100 |
| `AugAssign("+")` | 17 | 102-104, 110 |
| `BinOp("//","%")` | 27 | 106-114 |
| `Compare`/`CmpOp` | 28, 31 | 116-122 |
| `If` | 18 | 124-126 |
| `For` | 19 | 128-134 |
| `While` | 20 | 136-139 |
| `Return` | 21 | 147-152 |
| Harness `Run`, `Call`, `ListExpr` | 7, 26, 29 | 78, 92-96, 141-145 |

There is no silently fabricated semantics for a used construct.

### Exhaustive operational rule decisions

The following table accounts for all 49 rules in `semantic.k` and both rules
in `verification.k`.

| Rule line(s) | Decision |
|---|---|
| `semantic.k:78` | `Run` schedules module setup before argument expression evaluation; correct for the harness. |
| `79`, `80` | `Module` executes all definitions/statements and removes `moduleDone`; correct. |
| `82`, `83` | Empty/nonempty statement-list execution; disjoint and order-preserving. |
| `85-86` | Stores the used one-parameter function body in `<functions>`; correct for the submitted definition. General multi-parameter Python is intentionally unmodeled. |
| `88`, `89` | Integer and Boolean literals become corresponding values; true equations. Boolean source literals are unused. |
| `90` | Reads an existing binding without state change; correct. Missing-name exceptions are unmodeled but unreachable. |
| `92`, `93`, `94`, `95`, `96` | Empty, singleton, and nonempty list construction evaluates left-to-right and prepends the saved head. The singleton/nonempty surface patterns may share the empty-tail case, but their right sides agree there. |
| `98`, `99-100` | Evaluates a name-assignment RHS, then updates that binding; correct for all submitted assignments. |
| `102`, `103-104` | Evaluates the used `count += 1` and combines with the old integer binding. Full Python augmented-LHS timing is broader than this model but has no side-effecting witness in the submitted expression. |
| `106`, `107`, `108` | Enforces left-to-right binary operand evaluation before applying `#bin`; correct. |
| `110` | Integer addition equation; ordinary integer arithmetic. |
| `111-112` | Nonzero integer `/Int` equation. It matches Python floor division on the reached positive operands; the negative over-breadth is documented above. |
| `113-114` | Nonzero integer `%Int` equation. It matches Python modulo on the reached positive operands; the negative over-breadth is documented above. |
| `116`, `117`, `118` | Evaluates comparison operands left-to-right and invokes `#cmp`; correct. |
| `120`, `121`, `122` | Integer `>`, `>=`, and `==` equations; disjoint by operator string and mathematically correct. |
| `124`, `125`, `126` | Evaluates an `if` guard and selects exactly the true or false body. Guards are Boolean on every reached path. |
| `128`, `129` | Evaluates the iterable and initializes the list loop; correct. |
| `130-131` | Updates the loop variable before the body; correct. |
| `132` | Empty list terminates the `for`; correct. |
| `133-134` | Nonempty list executes one body and recurs on the tail, preserving order and count state; correct. |
| `136`, `137-138`, `139` | Re-evaluates the while guard after each true body and terminates on false; correct. |
| `141`, `142-145` | Evaluates the one argument, resolves the stored function, installs a fresh local environment, schedules explicit/implicit return handling, and later restoration. The body uses no globals, defaults, closures, or multiple arguments, so this matches its Python behavior. |
| `147`, `148` | Evaluates the returned expression and begins return scanning; correct. |
| `149` | Converts `returnScan(V) ~> implicitReturn` to `V`; correct for the function-call frame. |
| `150` | `[owise]` discards intervening computation until `implicitReturn`. This models abrupt return. The submitted `Return` is final, so no stateful suffix is skipped on its path; the explicit rule at 149 preempts the fallback. |
| `151` | Produces `none` on fall-through. It is unused because the function explicitly returns. |
| `152-153` | Restores the caller environment while preserving the return value and continuation; correct. |
| `verification.k:11-27` | Expands `SFTest(ARG)` to the exact submitted program body and call. It is an execution harness, not a result summary or answer rule. Structural pinning is established in Stage 4. |
| `verification.k:29-30` | Removes the harness-created function table only after obtaining a value, preserves that value and any continuation, and does not touch `<env>`. This cleanup changes internal harness state but cannot synthesize the task result. |

Rule overlaps are either disjoint (`#bin`, `#cmp`, Boolean branches,
empty/nonempty loop) or agree on the only possible list-tail overlap.
`returnScan` uses the explicit `implicitReturn` case plus an `owise` fallback.
No rule encodes the desired count, bypasses the function body, introduces a
fresh result oracle, or supplies an unconstrained value.

Stage 5 result: the semantics soundly covers the operations reached by the real
program on integer-list inputs, with documented over-broad totality and
negative-arithmetic limitations. The decisive defect remains the absent
general correctness claim, not an answer-smuggling rule.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`. I created the independent mutation
[spec-vacuity.k](evidence/spec-vacuity.k), copying submitted claim 1 but
changing its required result from `intVal(1)` to the demonstrably false
`intVal(2)`. The satisfying input is `[15,-73,14,-15]`; both Python
implementations and fresh K execution return 1.

The mutation first built successfully:

```text
kprove spec-vacuity.k --definition fresh-verification-kompiled --spec-module SPEC-VACUITY --dry-run
```

This exited 0; see
[stage6-vacuity-dry-run.log](evidence/stage6-vacuity-dry-run.log). The actual
proof command:

```text
kprove spec-vacuity.k --definition fresh-verification-kompiled --spec-module SPEC-VACUITY
```

exited 1 with `WarnStuckClaimState`. Its residual final configuration contains
`intVal(1)` and cannot unify with the mutated `intVal(2)` destination. See
[stage6-vacuity-proof.log](evidence/stage6-vacuity-proof.log).

Stage 6 result: pass. The submitted claim is result-constraining and the proof
rejects a meaningful reachable false result.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Conditional on the reconstructed K definition, the 11 reachability claims
listed in Stage 4 close. Thus, for their exact initial configurations and
requires clauses, executing the pinned function body reaches their exact
integer result with empty harness state. The proof does not establish any
statement for arbitrary lists or for all integer values.

### Trust and evidence ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K compiler, LLVM/Haskell backends, reachability logic | All executions and proofs | Standard unavoidable toolchain trust. Fresh builds reduce cache/provenance risk. |
| Built-in `INT`, `BOOL`, `MAP`, K sequencing and cells | All semantic rules | Acceptable low-level trust. Positive integer arithmetic is the reached subset. |
| Trusted `/reference/py2mpy.py` | Link from `solution.py` to `solution.mpy` | Authorized trusted input; byte regeneration establishes the current link. The translator itself is not proved here. |
| Generated `semantic.k` | Meaning of every K execution | Informally audited rule-by-rule and tested concretely. No separate universal metatheorem connects this custom subset to CPython. Over-broad totality and negative arithmetic are documented. |
| `SFTest` literal-body duplication and `clearFunctions` | All submitted claims | Normal proof harness boundary. The body executes; no opaque result is introduced. Current-artifact pinning is supported by normalized-term equality, but the source-to-wrapper equality is audit evidence rather than an internal K theorem. |
| Trusted canonical Python implementation | Natural-language adequacy oracle | Authorized trusted input. The 30,624-case differential is finite empirical evidence only. |
| Informal arithmetic equivalence of leading-digit division/parity and decimal first/last odd digits | Bridge from candidate algorithm to prompt | Convincing for positive integers and supported by differential tests, but not formalized in K. |
| Partial-correctness termination boundary | All claims | K reachability proves the submitted terminating cases. No general termination or partial-correctness theorem exists because there is no general entry claim. |

The successful `#Top`, generation trace, candidate final report, and
differential test are not substitutes for the missing quantified K theorem.
Finite tests show that the implementation is likely correct; they do not prove
the all-lists postcondition.

### Decision

The reconstructed theory is discriminating and the limited claims genuinely
execute the current submitted program. Nevertheless, a proof of finitely many
lists plus bounded singleton classes is not a proof that `specialFilter`
returns the required count for every intended list. This is a material
adequacy gap under the stated decision boundary, requiring `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
