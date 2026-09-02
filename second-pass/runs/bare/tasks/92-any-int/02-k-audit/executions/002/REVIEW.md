# Independent adversarial audit: HumanEval 92 `any_int`

## Executive assessment

The candidate contains a cleanly reconstructible, non-vacuous reachability
proof of the exact constructor program generated from its `solution.py`. The
proof executes that program through a small operational semantics; it does not
replace the answer-bearing computation with a lemma, oracle, opaque symbol, or
proof-only rewrite. All seven claims independently close from fresh source
builds.

I assign `CONCERNS / LEGIT`, rather than `PASS`, because the generated Python
uses `type(v) == int` while the trusted canonical uses
`isinstance(v, int)`. The implementations agree throughout the ordinary
built-in-integer/non-integer numeric domain exercised by the task, but differ
on equality-satisfying inputs containing a `bool` or an `int` subclass. I do
not treat those class-hierarchy edge values as a material narrowing of the
HumanEval prompt's ordinary “3 numbers” domain, so this is not
`FAIL / NOT_LEGIT`; it is a real implementation-to-reference limitation that
prevents an unqualified pass.

All commands below ran in `/tmp/audit-work/92-any-int`, using only source files
copied explicitly from the read-only mounts. Reviewer scripts and bounded logs
are in `/audit-output/evidence/`.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `92-any-int`, condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- no mounted reference semantics.

The launcher-owned campaign block is structurally identical to
`/audit-campaign-lock.json`, and the lock's SHA-256 is the recorded
`ad5dfc...d745`. The generated-semantics boundary is correct:
`/reference/reference-semantics` is absent.

I inspected every record required for `legacy-selected-stage1`:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the one 165-record
JSONL file under `codex-trace/`. Historical runtime metrics are not required
for this legacy layout. The structured trace parsed completely as JSON and the
unstructured transcript was independently hashed and line-indexed. These
records were treated only as historical claims.

All required files are real regular files, all required roots are real
directories, and no symlinks occur below `/candidate`, `/reference`, or
`/generation-evidence`. Every launcher-recorded regular-file hash matches,
including each evidence hash duplicated in `generation-result.json` and
`invocation.json`. The mounted candidate's independently recomputed
pipeline-v2 tree digest is
`f1a41ee5b1fe4bdbd51ac69121815ad06ac606d3712e498147ecf8d17963b0d8`,
identical to both the stage-1 result and invocation retained-workspace digest.
The independently recomputed trace-tree digest is
`4eae739b201db2c962ba5b42f7cb84680e729b0b15053ec8dd4e608b421e0300`,
identical to `usage.json`'s source-trace digest. The legacy audit envelope also
records directory snapshot digests under a different convention; direct file
hashes and the generation records provide the independently reproducible
mount checks.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
There is no infrastructure breach.

Evidence:

- `evidence/01-integrity.log`
- `evidence/01-generation-trace-summary.log`
- `evidence/01-generation-output-index.log`

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires a three-argument predicate that returns true
exactly when all three numbers are integers and at least one equals the sum of
the other two; otherwise it returns false. The canonical first applies
`isinstance(v, int)` to every argument and then checks the three equalities.

The generated solution instead returns the conjunction of three exact-type
tests, `type(v) == int`, and the same three equality tests. It preserves
left-to-right short-circuiting and is correct for arbitrary-size exact
built-in integers and ordinary non-integer numbers.

Trusted regeneration produced a file byte-identical to the submitted
`solution.mpy`; both hashes are
`5240ec9e4c19980dec3bdf45eb06f619883af762dd9287e7b77331902b736856`.

The independent differential test ran 5,485 unique cases:

- all triples over integers `[-5,5]`;
- a Cartesian boundary set containing zero, signs, 32/64-bit boundaries, and
  integers of magnitude `10^100`;
- each sum-equality branch and the all-false branch;
- every documented example;
- floats in every position, integral floats, infinities, NaN, `Decimal`,
  `Fraction`, complex values, and invalid non-number probes;
- booleans in every position and a genuine `int` subclass.

There were 176 mismatches. Every mismatch was an equality-satisfying case
containing a `bool` or `IntSubclass`: canonical returned true and generated
code returned false. Representative witnesses are `(True,1,2)` and
`(IntSubclass(1),1,2)`. There were no mismatches for exact built-in integers,
floats, or the other ordinary numeric probes.

The prompt has scalar arguments, so there is no meaningful empty-container
case; zero and the no-equality branch are the relevant empty/boundary analogues.
The exact-type/reference difference is retained as the audit concern described
above.

Evidence:

- `evidence/02-translator-regeneration.log`
- `evidence/differential_test.py`
- `evidence/02-differential.log`

## 3. Clean proof reconstruction

I copied only the candidate's source artifacts to scratch. No candidate-built
definition or cache was copied. K is version 7.1.293, Python is 3.10.12, and
Java is OpenJDK 17.0.16.

Fresh builds:

```text
kompile verification.k --backend llvm --main-module ANY-INT-VERIFICATION --syntax-module ANY-INT-VERIFICATION --output-definition concrete-kompiled
EXIT_STATUS: 0

kompile verification.k --backend haskell --main-module ANY-INT-VERIFICATION --syntax-module ANY-INT-VERIFICATION --output-definition proof-kompiled
EXIT_STATUS: 0
```

A preliminary concurrent invocation caused the LLVM wrapper to transiently
report an empty Java-version detection while the Haskell build succeeded. The
identical LLVM command succeeded sequentially without any environment change;
the observation and both statuses are preserved and do not affect the
candidate assessment.

Twelve fresh LLVM executions covered the examples, each equality branch,
all-false, zero, negatives, an unbounded large integer, a float in each
position, a boolean, and the modeled catch-all non-integer number. Every K
result matched direct execution of `solution.py`, and every final `<env>` was
`.Map`.

Each positive target claim was then placed unchanged in its own reviewer
module and run independently against the fresh Haskell definition. Claims
1–7 each printed exactly `#Top` and exited 0:

```text
kprove audit-spec-N.k --definition proof-kompiled --spec-module AUDIT-SPEC-N
```

Evidence:

- `evidence/02-scratch-copy.log`
- `evidence/03-toolchain-versions.log`
- `evidence/03-preliminary-concurrent-build-note.txt`
- `evidence/03-build-concrete.log`
- `evidence/03-build-proof.log`
- `evidence/03-concrete-python-compare.log`
- `evidence/k/audit-spec-1.k` through `evidence/k/audit-spec-7.k`
- `evidence/03-proof-claim-1.log` through
  `evidence/03-proof-claim-7.log`

## 4. Adequacy and real-program pinning

The seven entry claims say:

1. For arbitrary integer `X,Y,Z`, return true if `X+Y=Z`.
2. Return true if the first equality is false and `X+Z=Y`.
3. Return true if the first two equalities are false and `Y+Z=X`.
4. Return false if all three equalities are false.
5. Return false if the first argument is a modeled non-integer, regardless of
   later arguments.
6. Return false if the first is an integer and the second is a non-integer,
   regardless of the third.
7. Return false if the first two are integers and the third is a non-integer.

All claims require the actual initial state used by the semantics:
`<env> .Map </env>`. The integer claims are exhaustive because the four
guards partition the truth values of the three equalities in their
left-to-right order. Claims 5–7 partition the location of the first
non-integer, exactly matching short-circuit control. `NonIntVal` contains
floats, booleans, and a tagged catch-all for other non-integer numbers.
Internal `typeVal` values are not source-level numeric arguments and are
properly outside this input partition.

The postconditions are exact returned `boolVal` values, not free variables,
implications, or unconstrained summaries. The claims also reach the cleared
environment. There are no helper or loop claims.

`RunAnyInt(X,Y,Z)` macro-expands to
`Invoke(solutionProgram,X,Y,Z)`. Independently parsing the regenerated
`solution.mpy` and expanding `solutionProgram` produced byte-identical
4,029-byte KORE terms with SHA-256
`d397a39a506ec56ba3cd5a1a716682a9d3d53d3716a63475b8eee1b719b9064f`.
Thus the theorem executes the same function binding, parameters, and body as
the trusted translator output.

Each precondition is satisfiable. Ground witnesses are:

| Claim | Witness | Result in canonical/generated/K |
|---|---|---|
| 1 | `(5,2,7)` | true / true / true |
| 2 | `(2,5,3)` | true / true / true |
| 3 | `(5,2,3)` | true / true / true |
| 4 | `(3,2,2)` | false / false / false |
| 5 | `(1.0,2,3)` | false / false / false |
| 6 | `(1,2.0,3)` | false / false / false |
| 7 | `(1,2,3.0)` | false / false / false |

A separate body-sensitivity probe changed the program term actually passed to
`Invoke` to `return False`. Its expanded KORE hash changed to
`41676b...dff`, the mutated module built successfully, and the original true
obligation for `(5,2,7)` failed with final `boolVal(false)`. This is a genuine
executed-body mutation, not a change to an ignored external Python file.

Evidence:

- `evidence/03-program-kore-identity.log`
- `evidence/04-claim-witnesses.log`
- `evidence/k/verification-body-mutated.k`
- `evidence/k/body-mutation-spec.k`
- `evidence/04-body-mutation-build.log`
- `evidence/04-body-mutation-term-diff.log`
- `evidence/04-body-mutation-proof.log`

## 5. Rule-by-rule static soundness review

### Local declarations

`MPY-SYNTAX` declares:

- `Program`: `Module(Stmts)`;
- `Stmts`: one `Stmt`;
- `Stmt`: `FuncDef(String,Params,Stmts)` and `Return(Expr)`;
- `Params`: exactly three string names;
- `Expr`: `Name`, `Int`, `Bool`, `BinOp`, `Call`, `Compare`,
  three-operand `BoolOp`, and four-operand `BoolOp`;
- `CmpOp`: one operator string and right expression;
- `IntVal`: `intVal(Int)`;
- `NonIntVal`: `floatVal(Float)`, `boolVal(Bool)`, and
  `otherNumberVal(String)`;
- `Val`: `IntVal`, `NonIntVal`, and internal `typeVal(String)`;
- `KItem`: `Invoke(Program,Val,Val,Val)`.

`MPY-SEMANTICS` declares the `<mpy><k/><env/></mpy>` configuration and helper
K-items `exec`, `eval`, `finishCall`, `typeOf`, `binLeft`, `binRight`,
`compareLeft`, `compareRight`, `andThen`, and `orThen`.

`verification.k` adds only the `solutionProgram` syntax macro and the
`RunAnyInt` syntax macro. There are no local K functions, `total` or
`functional` declarations, opaque symbols, priority rules, simplification
rules, `owise` rules, or auxiliary proof lemmas. No helper K file exists.

The exact submitted program uses `Module`, `FuncDef`, `Params`, `Return`,
four- and three-operand `BoolOp`, `Compare`, `Call`, `Name`, `CmpOp`, and
`BinOp`; every one maps directly to the declarations above.

### Operational rules

The 24 semantic rules were assessed individually:

1. `Invoke(Module(FuncDef(...)))` binds the exact three parameters
   left-to-right into an initially empty environment, schedules the exact
   body, then `finishCall`. The function name is immaterial because the
   `Program` value itself is explicitly supplied and mechanically pinned.
2. `exec(Return(E))` evaluates the returned expression.
3. `Val ~> finishCall` returns that value and clears the call-local
   environment. `Invoke` only starts from `.Map`, so no caller environment is
   discarded on the claim domain.
4. `eval(Int(I))` truthfully constructs `intVal(I)`.
5. `eval(Bool(B))` truthfully constructs `boolVal(B)`.
6. `eval(Name("int"))` yields the fixed built-in exact-int type object used by
   this program.
7. `eval(Name(X))` reads the corresponding local environment binding.
8. `eval(Call(Name("type"),E))` evaluates `E`, then applies exact type
   classification. The target has an unshadowed built-in `type`.
9. `IntVal ~> typeOf` yields `typeVal("int")`.
10. `NonIntVal ~> typeOf` yields `typeVal("non-int")`.
11. `eval(BinOp(OP,E1,E2))` starts left evaluation.
12. The `binLeft` rule evaluates the right operand only after the left value.
13. `binRight("+",intVal(I1))` computes unbounded K integer addition in source
    operand order.
14. `eval(Compare(E1,CmpOp(OP,E2)))` starts the left comparison operand.
15. `compareLeft` evaluates the right operand after the left.
16. Integer `==` returns K integer equality as a Python boolean value.
17. Type-object `==` returns string equality; only the exact-int/non-int tags
    can reach it in the target.
18. Three-operand `and` schedules operands left-to-right.
19. Four-operand `and` does the same for the exact outer target expression.
20. True `andThen(E)` evaluates the next operand.
21. False `andThen` skips the next operand and propagates false; repeated
    continuations skip all remaining operands.
22. Three-operand `or` schedules operands left-to-right.
23. False `orThen(E)` evaluates the next operand.
24. True `orThen` skips the next operand and propagates true through any
    remaining continuation.

The two verification rules are syntax-only expansions: `solutionProgram`
expands to the exact submitted constructor tree, and `RunAnyInt` expands to
`Invoke` of that tree. They do not replace execution or introduce a result.

The rule set preserves the target's evaluation order, short-circuit control,
bindings, exact-integer arithmetic, returned value, and sole mutable cell.
There is no heap, allocation, I/O, exception-producing used operation, nested
call stack, or loop to model. Unsupported operator strings or unused AST forms
stop rather than fabricate results, which is acceptable for generated minimal
semantics.

There is a deliberately narrow source-language boundary: the built-in
`Name("int")`/`Name("type")` handling is fixed rather than a complete Python
global lookup semantics. The exact submitted function neither binds nor
mutates those names, and its only environment keys are `"x"`, `"y"`, and
`"z"`, so the generic lookup rule cannot overlap on an actual execution.
No false-conclusion witness exists on the intended target input domain; this
is therefore recorded as unused-language incompleteness, not an unsound target
rule.

No task-answer encoding, execution bypass, unconstrained oracle, or false
semantic/proof rule was found.

Evidence: `evidence/05-static-source-inventory.log`.

## 6. Fresh non-vacuity test

The fresh reviewer mutation changes claim 1's postcondition from
`boolVal(true)` to `boolVal(false)` while retaining the satisfiable
precondition `X +Int Y ==Int Z`. `(5,2,7)` is an explicit false witness.

The mutated spec compiled to KORE successfully:

```text
kprove audit-spec-vacuity.k --definition proof-kompiled \
  --spec-module AUDIT-SPEC-VACUITY --dry-run
EXIT_STATUS: 0
```

The real proof run exited 1 with `WarnStuckClaimState`. Its irreducible state
contains `boolVal(true)` while the destination requires `boolVal(false)`.
This is the expected unmet result obligation, not a parse error, missing
import, timeout, or unrelated crash.

Evidence:

- `evidence/k/audit-spec-vacuity.k`
- `evidence/06-vacuity-dry-run.log`
- `evidence/06-vacuity-proof.log`

## 7. Proven versus assumed accounting

### Formally established

Under the submitted K semantics, the exact regenerated constructor program,
when it reaches a result on a modeled numeric input:

- returns true for exact integers precisely in the three equality regions;
- returns false for exact integers when all three equalities fail;
- returns false as soon as the first modeled non-integer is encountered;
- clears its local environment.

The seven claims collectively cover arbitrary unbounded exact integers and
every position of the first non-integer. This is not a finite-size proof.

### Trust boundary and informal bridges

- **K kernel/backend and compiler:** trusted to implement reachability,
  rewriting, macro expansion, and the reported `#Top`.
- **K built-ins:** unbounded `Int`, `Bool`, `String`, `Map`, `Float` parsing,
  `+Int`, `==Int`, `==String`, and Boolean guard operations are trusted
  primitives. They are low-level language infrastructure, not task-answer
  assumptions.
- **Trusted translator:** `/reference/py2mpy.py` is outside the theorem. Its
  output linkage is strengthened by byte-identical regeneration and
  constructor-level KORE identity.
- **Generated Python-to-K value bridge:** exact Python `int` values map to
  `intVal`; every exact non-int numeric value maps to one of the
  `NonIntVal` constructors. The catch-all tag is never inspected after exact
  type failure, so it cannot smuggle an equality result. This bridge is
  audited statically and tested concretely but is not itself a machine-checked
  CPython formalization.
- **Canonical/source intent:** finite differential evidence supports ordinary
  numeric behavior but does not prove universal equivalence. The observed
  `bool`/`int`-subclass discrepancy remains explicit.
- **Partial correctness:** reachability proves the stated final results; it is
  not a general theorem about arbitrary Python programs or unsupported
  constructor terms.

There are no opaque result-bearing symbols, operational bridges, empirical
task-answer primitives, proof-local mathematical lemmas, or assumed loop
invariants.

Gate A (real-program soundness and non-vacuity) passes. Gate B passes for the
ordinary HumanEval numeric domain, with the documented exact-type/canonical
edge-domain concern. Gate C passes: all claimed reconstruction, differential,
pinning, body-sensitivity, and mutation evidence is reproducible and bounded.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
