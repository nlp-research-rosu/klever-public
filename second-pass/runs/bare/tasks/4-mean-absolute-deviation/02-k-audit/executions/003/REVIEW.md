# Independent adversarial review: 4-mean-absolute-deviation

The candidate has a reproducible, non-vacuous K reachability proof about its own exact-rational model, and its claim mechanically pins the submitted `solution.mpy`. It is not a legitimate partial-correctness proof of the real generated Python program over the HumanEval source-contract domain. The fatal gap is not merely missing test evidence: the generated arithmetic semantics gives a different result from CPython on a concrete finite `List[float]`, and the formal claim supplies no domain/representation invariant that repairs that mismatch. The claim also admits malformed/negative-denominator `rat` terms for which its `absNum` rule proves the wrong mathematical MAD.

## 1. Input and provenance integrity

### Launcher and campaign records

I read `/audit-input.json` first. It declares:

- problem `4-mean-absolute-deviation`;
- condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- no mounted reference-semantics tree.

The independent checker read and hashed every launcher-mapped mount and every required record for this layout: `/run.json`, `/task.json`, `/generation-result.json`, `invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, `prompt.txt`, the structured trace, and the present `usage.json`. Historical runtime metrics are absent but are not required for this legacy layout. All required entries are regular, readable, non-symlink files/directories. See [01-integrity.log](/audit-output/evidence/01-integrity.log).

The `audit_campaign` object is structurally identical to `/audit-campaign-lock.json`. Its actual SHA-256 is `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`, exactly the hash recorded in `/audit-input.json`. Every launcher-declared per-file hash checked by the independent script matches.

The structured trace has one JSONL file, 206 valid records, 36 tool calls, 36 tool outputs, and a final untrusted `KPROVE_PASSED` claim. The entire trace was parsed rather than accepting that marker; the 14,196-line `codex-output.log` was also read and inventoried. See [01-trace-inventory.log](/audit-output/evidence/01-trace-inventory.log).

### Trusted/candidate boundary

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- Neither `/reference/reference-semantics` nor `/candidate/reference-semantics` exists, as required in `GENERATED_SEMANTICS` mode.
- No mounted candidate, reference, or generation-evidence entry is symlinked.
- Candidate source and trusted inputs were copied to `/tmp/audit-work/4-mad-audit`; their independent per-file hashes are in [01-scratch-source-hashes.log](/audit-output/evidence/01-scratch-source-hashes.log).

There is no infrastructure breach. The generation transcript and its earlier `#Top` were treated only as untrusted historical claims.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt asks `mean_absolute_deviation(numbers: List[float]) -> float` to compute

`average(abs(x - average(numbers)))`

and gives `[1.0, 2.0, 3.0, 4.0] -> 1.0`. It states no explicit input-length or finite-float restriction. The trusted canonical implementation computes the mean with Python `sum` and `/`, then sums a generator of absolute deviations and divides by the length. On an empty list it raises `ZeroDivisionError`.

The candidate uses the same expression but materializes the deviations as a list:

```python
mean = sum(numbers) / len(numbers)
return sum([abs(x - mean) for x in numbers]) / len(numbers)
```

That algorithmic change is extensionally inert for these pure finite iterations.

### Trusted translation

Running the trusted translator on the scratch copy of `solution.py` produced SHA-256 `468cdf1deeb199660cf330c02f1622195cacd82f10142d05fbbbef44b0ed934e`, byte-identical to the submitted `solution.mpy`; `cmp` exited 0. Exact commands and statuses are in [02-translation-fidelity.log](/audit-output/evidence/02-translation-fidelity.log).

### Independent differential test

[differential_test.py](/audit-output/evidence/differential_test.py) loads the candidate and trusted canonical entry points independently. It checks:

- the documented example;
- empty, singleton, all-equal, two-value, and below/equal/above-mean boundaries;
- mixed signs, signed zero, very small and large finite values;
- rounding-sensitive decimals;
- infinities and NaN;
- 250 deterministic generated lists (seed `5062980`).

All 265 cases agree, including exact float bits or the same exception class/arguments. The corpus hash is `cb26d4fba048cc2a11ef5af1d35ddc6c8b7e9f9561a24bcbf96d4313509b08da`; mismatches are zero. Full inputs, command, and results are in [02-differential.log](/audit-output/evidence/02-differential.log). This strongly supports candidate-versus-canonical fidelity on the tested inputs, but it is finite evidence rather than a universal proof.

## 3. Clean proof reconstruction

No candidate-built definition or cache was reused.

### Fresh standalone semantics

From `/tmp/audit-work/4-mad-audit/candidate`:

```text
kompile semantic.k --backend haskell --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --output-definition semantic-audit-kompiled
```

This exited 0; see [03-kompile-semantic.log](/audit-output/evidence/03-kompile-semantic.log).

Fresh `krun` executions consumed the submitted `solution.mpy` and reached `.K`:

| Input encoding | K result | Independent Python/Fraction result |
|---|---:|---:|
| `1,2,3,4` | `rat(1024,1024) = 1` | `1` |
| singleton `5` | `rat(0,1)` | `0` |
| `-2,0,2` | `rat(108,81) = 4/3` | `4/3` |
| `1/10,2/10,3/10` | a non-normalized `rat` equal to `1/15` | `1/15` |

The executions are in [03-krun-example.log](/audit-output/evidence/03-krun-example.log), [03-krun-singleton.log](/audit-output/evidence/03-krun-singleton.log), [03-krun-abs-boundaries.log](/audit-output/evidence/03-krun-abs-boundaries.log), and [03-krun-decimal-rationals.log](/audit-output/evidence/03-krun-decimal-rationals.log). The independent parser/comparator is [semantic_compare.py](/audit-output/evidence/semantic_compare.py), with results in [03-semantic-python-comparison.log](/audit-output/evidence/03-semantic-python-comparison.log).

The same concrete reconstruction exposes three semantic disagreements:

1. `nums()` terminates normally with `result(rat(0,0))`, while both Python implementations raise `ZeroDivisionError`; see [03-krun-empty-valid.log](/audit-output/evidence/03-krun-empty-valid.log).
2. `nums(rat(1,-1),rat(1,1))`, an accepted representation of `[-1,1]`, returns `rat(0,-8) = 0`; Python/Fraction MAD is `1`; see [03-krun-negative-denominator.log](/audit-output/evidence/03-krun-negative-denominator.log).
3. Encoding the exact IEEE-754 values of `[0.1,0.2,0.3]` as rationals makes K return
   `5404319552844595/81064793292668928`, whereas the actual Python return value is exactly
   `4803839602528529/72057594037927936`. Their difference is
   `-1/648518346341351424`. See [03-krun-binary-float-encoding.log](/audit-output/evidence/03-krun-binary-float-encoding.log) and [03-semantic-python-comparison.log](/audit-output/evidence/03-semantic-python-comparison.log).

The third witness is a normal, nonempty, finite `List[float]` in the source-contract domain. It shows that exact rational arithmetic is not a semantically inert encoding of the real Python execution.

### Fresh proof definition and positive claim

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition verification-audit-kompiled
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC
```

Compilation exited 0. The sole positive target claim printed `#Top` and exited 0. See [03-kompile-verification.log](/audit-output/evidence/03-kompile-verification.log) and [03-kprove-spec.log](/audit-output/evidence/03-kprove-spec.log).

Thus the historical verification result is reproducible, but only under the candidate-generated theory.

## 4. Adequacy and real-program pinning

### Claim in plain language

The sole entry claim has no `requires` clause. Its inferred precondition is:

- `H` is any `Num`;
- `T` is any `Nums`;
- the argument is the nonempty list `nums(H,T)`;
- `<env>` is `emptyEnv`;
- `<result>` is `noResult`;
- `<k>` starts `init(solutionProgram, nums(H,T))`.

Its postcondition requires:

- `<k>` is completely consumed;
- `<env>` contains `mean = sumNums(H,T)/countNums(H,T)` above the original `numbers` binding;
- `<result>` is exactly `result(mathMAD(H,T))`.

The result is not a free variable, tautology, or one-way implication. `mathMAD` expands to the candidate's exact-rational `sumAbs/countNums` expression.

A satisfying state is `H=rat(1,1)` and `T=rat(2,1),rat(3,1),rat(4,1)`. Fresh K execution returns `1`; both Python implementations return `1`. This is the documented witness in Stage 3.

### Mechanical program pinning

`solutionProgram` is manually maintained in `verification.k`, but for this immutable candidate it denotes the actual submitted program. [program_term_compare.py](/audit-output/evidence/program_term_compare.py) parses `solution.mpy` with `kast`, extracts the compiled `solutionProgram` rule's RHS, and compares the constructor terms. Both normalized terms are 3,206 characters with SHA-256 `31de4df11a4ddbd2c5912c6d2508946cd6d784535ef3557c3015795156fe146c`; they are byte-identical. See [04-program-term-compare.log](/audit-output/evidence/04-program-term-compare.log).

The entry-selection, assignment, return, and expression rules therefore execute the submitted binding/body rather than a substituted function.

### Body sensitivity

I changed the program term actually executed by the claim: only `solutionProgram`'s real return body was replaced by `Return(Int(0))`. The mutated verification definition compiled successfully, but the original postcondition proof exited 1 with `WarnStuckClaimState` and a residual equality between `rat(0,1)` and the MAD expression. See [04-body-mutation-diff.log](/audit-output/evidence/04-body-mutation-diff.log), [04-body-mutation-kompile.log](/audit-output/evidence/04-body-mutation-kompile.log), and [04-body-mutation-kprove.log](/audit-output/evidence/04-body-mutation-kprove.log).

### Adequacy decision

Program identity and result constraint pass. Intent/domain adequacy fails:

- the formal argument domain is nonempty `Nums`, not `List[float]`;
- `Num` has only unconstrained `rat(Int,Int)` terms—no IEEE infinities, NaN, signed-zero behavior, or float-rounding steps;
- exact rational operations demonstrably disagree with real Python on the finite float witness `[0.1,0.2,0.3]`;
- there is no formal encoding relation or conditional postcondition connecting `rat` execution to CPython floats;
- there is not even a precondition that rational denominators are positive and nonzero.

This is a material narrowing/change of the HumanEval source-contract domain and execution model. Under the benchmark's decision boundary, even a sound theorem for that narrowed domain would be `FAIL / NOT_LEGIT`.

## 5. Rule-by-rule static soundness review

The exhaustive machine-produced inventory is [05-rule-inventory.log](/audit-output/evidence/05-rule-inventory.log): 21 local syntax declarations, 41 candidate-authored rules, and one claim. There are no generated helper K files beyond `semantic.k`.

### Syntax, configuration, and attributes

| File/lines | Declaration | Audit |
|---|---|---|
| `semantic.k:7` | `ModuleAst ::= Module(Stmts)` | Used by `solution.mpy`. |
| `semantic.k:8` | `Stmts ::= List{Stmt,""}` | Used for module/function bodies. |
| `semantic.k:9` | `Strings ::= List{String,","}` | Used by import/params/cell/free metadata. |
| `semantic.k:10` | `Exprs ::= List{Expr,","}` | Used by calls and comprehension guards. |
| `semantic.k:11` | `CompFors ::= List{CompFor,""}` | Used by the single list comprehension. |
| `semantic.k:13` | `Params(...)` | Used by the entry definition. |
| `semantic.k:14` | `CellVars(...)` | Parsed and matched; operationally ignored. |
| `semantic.k:15` | `FreeVars(...)` | Parsed and matched; operationally ignored. |
| `semantic.k:17-21` | `ImportFrom`, two `FuncDef` forms, `Assign`, `Return` | Covers every submitted statement constructor. |
| `semantic.k:23-29` | `Name`, `Int`, `Float`, `Bool`, `BinOp`, `Call`, `ListComp` | Covers every submitted expression constructor. `Float` is declared but has no evaluator rule; unused by the submitted body. |
| `semantic.k:31` | `CompFor` | Covers the submitted comprehension clause. |
| `semantic.k:39-47` | `Num`: `rat` plus eight functions | Exact-rational value layer; material mismatch discussed below. |
| `semantic.k:48` | `Nums` list | Formal input collection. |
| `semantic.k:50-52` | `Value`: `Num`, `nums`, `comprehension` | Represents numeric arguments and a delayed comprehension. |
| `semantic.k:54-55` | `Env`: `emptyEnv`, `bind` | Newest-first lexical environment. |
| `semantic.k:56` | `lookup` | Partial environment function. |
| `semantic.k:58-64` | `eval`, `sumValue`, `lenValue`, `absValue`, `subValue`, `divValue`, `makeComp` | Partial expression/builtin functions. |
| `semantic.k:66` | `Result`: `noResult`, `result` | Return-state cell. |
| `semantic.k:68-73` | Configuration `<mad><k/><env/><result/></mad>` | All three cells are read or written; no unused heap/stack cells. |
| `semantic.k:75-79` | `init`, `seekTarget`, `exec`, `setVar`, `finish` | Control terms for module entry and statements. |
| `verification.k:7` | `solutionProgram [function]` | Exact constructor-tree name; mechanically validated. |
| `verification.k:28` | `mathMAD [function]` | Exact-rational summary, not an independently connected Python-float contract. |

There are 18 `[function]` symbols: `addNum`, `subNum`, `divNum`, `absNum`, `sumNums`, `countNums`, `sumAbs`, `asNum`, `lookup`, `eval`, `sumValue`, `lenValue`, `absValue`, `subValue`, `divValue`, `makeComp`, `solutionProgram`, and `mathMAD`.

There are no candidate-authored `[total]`, `[functional]`, `[opaque]`, `[simplification]`, `[concrete]`, priority rules, or proof lemmas. Function declarations are partial where equations do not cover a constructor/shape. Guard pairs for `lookup` and `absNum` are syntactically disjoint; recursive list base/step rules are constructor-disjoint.

### Operational and mathematical rules

| ID/location | Rule role | Static decision |
|---|---|---|
| S1 `82` | `init(Module(SS),ARGS) -> seekTarget` | Faithful module-entry step. |
| S2 `83-84` | Skip `ImportFrom` | Sound for the submitted typing-only import; overbroad for arbitrary effectful imports, which are outside the submitted construct instance. |
| S3 `85-88` | Select annotated `mean_absolute_deviation(numbers)` and bind argument | Matches the actual binding/body and resets the local environment appropriately for this entry call. |
| S4 `89-90` | Skip three-argument `FuncDef` | Unused by the submitted module; constructor-disjoint. |
| S5 `91-93` | Skip non-target annotated `FuncDef` | Guard excludes the target name; unused here. |
| S6 `96` | Finish empty statement list | Faithful. |
| S7 `97-99` | Evaluate assignment, then continue | Explicit sequencing is correct for the submitted pure RHS. |
| S8 `100-101` | Prepend assigned binding | Correct newest-binding shadowing. |
| S9 `102-103` | Evaluate `Return`, discard remaining statements | Correct abrupt return for this single frame. |
| S10 `104-105` | Store returned value and consume control | Correct from `noResult`; no stack is needed by this program. |
| S11 `108` | Lookup newest matching binding | Correct. |
| S12 `109-110` | Recurse past nonmatching binding | Guard is disjoint from S11; correct. |
| S13 `114` | Evaluate `Name` by lookup | Correct for available target bindings. |
| S14 `115` | Integer literal to `rat(I,1)` | Mathematically sound; unused by the submitted body. |
| S15 `116-117` | Binary subtraction wrapper | Preserves both operands but delegates to exact rational arithmetic, not Python float arithmetic. |
| S16 `118-119` | Binary division wrapper | Same delegation; does not model Python zero division or rounding. |
| S17 `120` | Builtin `sum` wrapper | Correct name for the target in an ordinary unmodified builtins environment. |
| S18 `121` | Builtin `len` wrapper | Correct for target `nums`. |
| S19 `122` | Builtin `abs` wrapper | Delegates to the flawed unconstrained-rational sign rule below. |
| S20 `123-124` | Turn the one-clause list comprehension into a delayed `makeComp` | Evaluates the iterator once and captures `ENV`; sufficient for the target's pure expression but not a general Python comprehension semantics. |
| S21 `126` | Make a comprehension over `nums` | Correct representation step. |
| S22 `127` | `sumValue(nums(NS)) -> sumNums(NS)` | Correct exact fold, conditional on numeric arithmetic. |
| S23 `128` | `lenValue(nums(NS)) -> countNums(NS)` | Correct. |
| S24 `129` | `absValue(Num) -> absNum` | Shape bridge; inherits S32/S33's denominator defect. |
| S25 `130` | `subValue(Num,Num) -> subNum` | Shape bridge; inherits exact-rational/float mismatch. |
| S26 `131` | `divValue(Num,Num) -> divNum` | Shape bridge; inherits missing zero guard and float mismatch. |
| S27 `136-138` | Fuse `sum(abs(x-m) for x in NS)` to `sumAbs(NS,lookup(m,ENV))` | Result-bearing, task-specific operational bridge. It is correct on the submitted syntactic instance (`X="x"`, `M="mean"`) under the ideal-rational/pure-expression assumptions, but has no bridge-free connection theorem and is false over its complete declared match domain when `X=M`. |
| S28 `140` | `asNum(Num) -> Num` | Correct. |
| S29 `143-144` | Rational addition | Ordinary fraction formula only when denominators denote valid nonzero rationals; performs no CPython float rounding. No invariant supplies either condition. |
| S30 `145-146` | Rational subtraction | Same limitations as S29. |
| S31 `147-148` | Rational division | Missing the nonzero-divisor guard; empty input reaches this rule and fabricates `rat(0,0)`. It also omits float rounding. |
| S32 `149-150` | Negate when numerator is negative | Correct only if denominator is positive. |
| S33 `151-152` | Keep value when numerator is nonnegative | Correct only if denominator is positive. |
| S34 `154` | Empty sum is `0` | Correct. |
| S35 `155` | Recursive sum | Structurally correct; inherits S29. |
| S36 `156` | Empty count is `0` | Correct. |
| S37 `157` | Recursive count | Correct; terminates on finite `Nums`. |
| S38 `158` | Empty absolute-deviation sum is `0` | Correct. |
| S39 `159` | Recursive absolute-deviation sum | Structurally correct; inherits S29/S30/S32/S33. |
| V1 `verification.k:8-24` | Define `solutionProgram` | Exact submitted constructor term; no substitution defect. |
| V2 `verification.k:29-30` | Define `mathMAD` using `sumAbs`, `sumNums`, `countNums`, `divNum` | A definitional summary inside the generated theory. It shares the same result-bearing functions as execution and therefore does not independently establish the HumanEval/CPython meaning. |

### False-conclusion witnesses and construct coverage

**Float arithmetic witness (used construct, intended source domain).** S15/S16/S29-S31 replace each Python float operation with unrounded exact fraction arithmetic. On `[0.1,0.2,0.3]`, encoded by the exact rationals of those three float objects, the final K and Python fractions differ by `-1/648518346341351424`. This is a false operational conclusion for the actual submitted body and a normal intended input. It is the primary material soundness witness.

**Denominator/sign witness (formal entry domain).** The entry claim has no positivity/nonzero-denominator requirement, so `H=rat(1,-1)`, `T=rat(1,1)` satisfies it. S32/S33 decide absolute-value sign from the numerator alone. K consequently proves/result-produces zero for the mathematical list `[-1,1]`; independent Python/Fraction execution returns one. This is a concrete false conclusion enabled by S32/S33 inside the formal precondition.

**Fusion match-domain witness.** S27 permits `X=M`. In [05-fusion-overlap-witness.mpy](/audit-output/evidence/05-fusion-overlap-witness.mpy), the outer environment binds `x=5` and the comprehension binds `x` over `[1]` while evaluating `abs(x-x)`. Python's bound comprehension variable yields `0`; the rule looks up the outer `x` as the center and returns `4`. See [05-fusion-overlap-witness.log](/audit-output/evidence/05-fusion-overlap-witness.log) and [05-fusion-python-oracle.log](/audit-output/evidence/05-fusion-python-oracle.log). The submitted body uses distinct `"x"` and `"mean"`, so this witness does not itself show a wrong submitted-program result; it shows that the unrestricted bridge is false over its declared reusable match domain and should at least require `X =/=String M`.

Every constructor actually present in `solution.mpy` maps to a declaration and rule path: `Module`, `ImportFrom`, annotated `FuncDef`, `Assign`, `Return`, `Name`, `BinOp("-","/")`, builtin `Call(sum,len,abs)`, `ListComp`, `CompFor`, and `Bool(true)`. There are no loops, mutation-bearing collections, program-defined helper calls, heap effects, I/O, or exceptions on the claim's ideal nonempty positive-denominator path. Evaluation order is underspecified for general effectful expressions, but the submitted expressions are pure; this is not an additional target-path defect.

## 6. Fresh non-vacuity test

I created [06-spec-vacuity-audit.k](/audit-output/evidence/06-spec-vacuity-audit.k), which changes only the returned-value obligation to `result(rat(0,1))`. The original precondition remains satisfiable, and `[1,2,3,4]` is a concrete counterexample because both reconstructed K and Python return `1`.

First, the mutation parsed and built:

```text
kprove spec-vacuity-audit.k --definition verification-audit-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run \
  --emit-json-spec spec-vacuity-audit.json
```

It exited 0; see [06-vacuity-dry-run.log](/audit-output/evidence/06-vacuity-dry-run.log).

The actual proof command exited 1 with `WarnStuckClaimState`. Its residual explicitly contains the unmet equality between `rat(0,1)` and the computed MAD expression; it was not a parser error, timeout, unrelated crash, or unreachable mutation. See [06-vacuity-kprove.log](/audit-output/evidence/06-vacuity-kprove.log).

The candidate proof is therefore result-constraining and non-vacuous under its supplied theory.

## 7. Proven versus assumed accounting

### Precisely what `#Top` establishes

Under the candidate's generated K rules, for every K term `H:Num` and finite `T:Nums`, execution of the exact submitted constructor body on the nonempty argument `nums(H,T)` reaches a consumed `<k>` cell, stores the syntactically defined exact-rational mean in `<env>`, and stores the syntactically defined `mathMAD(H,T)` in `<result>`.

That is a symbolic execution characterization of the custom rational evaluator. It is not a theorem that actual CPython execution on every `List[float]` returns the mathematical real-number MAD, and it is not even a correct mathematical-rational theorem for all `rat` terms admitted by the claim.

### Trust ledger

| Boundary | Dependents | Classification |
|---|---|---|
| K 7.1.293 parser/compiler/Haskell backend and unbounded `Int`/`Bool`/`String` builtins | All compilation and proof results | Ordinary toolchain trust; version and clean commands recorded. |
| Trusted `py2mpy.py` transliteration | Python-source to `solution.mpy` identity | Acceptable syntactic bridge here: trusted mount, byte-identical candidate copy, fresh regeneration, and byte identity. |
| Manually named `solutionProgram` | Sole entry claim | Acceptable for this immutable candidate: constructor-level mechanical equality and body-sensitivity failure are recorded. It remains a maintenance observation, not the fatal defect. |
| Generated module/statement/environment rules S1-S14 | Program control and bindings | Informally validated against the exact target control flow; concrete executions and body mutation support them. |
| Task-specific comprehension fusion S20/S21/S27 | Returned sum and `mathMAD` claim | Concerning/insufficiently isolated: no bridge-free universal connection theorem; S27 is false on its full match domain. For the exact target syntax it is informally correct only under the candidate's ideal numeric/purity assumptions. |
| Exact rational arithmetic S15/S16/S24-S39 | Mean, deviations, final result, and postcondition | Illegitimate as an unconditional model of Python `float`: a concrete intended-domain witness produces a different value. Denominator well-formedness is also unasserted. |
| `mathMAD` V2 | Final result constraint | Defined, not opaque, but uses the same `sumAbs/divNum` symbols as execution. It proves no independent source-contract bridge and inherits every arithmetic defect. |
| Candidate/canonical differential test | Implementation-fidelity judgment only | Strong finite evidence (265 cases, zero mismatches), not a universal proof and not a repair for K semantic divergence. |
| K/Python concrete comparisons | Semantics-audit witnesses | Finite evidence used appropriately to demonstrate concrete mismatches, not to assert universal equivalence. |

There are no other opaque symbols, totality axioms, simplification lemmas, circularity claims, loop invariants, or auxiliary reachability claims.

### Gate and decision summary

- **Fresh verification:** PASS — the sole claim freshly prints `#Top`.
- **Program pinning/result constraint/non-vacuity:** PASS.
- **Real-program semantic soundness:** FAIL — exact rational rules produce a false result relative to actual Python float execution on `[0.1,0.2,0.3]`.
- **Internal rational-domain soundness:** FAIL — the claim admits negative/zero denominators, and `absNum`/division give false mathematical or exceptional behavior.
- **Intent/domain adequacy:** FAIL — the theorem materially changes/narrows unrestricted `List[float]` behavior to a nonempty ideal-rational model without a proved representation relation.
- **Trust/evidence auditability:** FAIL for full validation — the task-specific result-bearing comprehension bridge has no independent universal connection theorem, though its actual target instance is informally understandable and concretely exercised.

The reproducible `#Top` and successful non-vacuity test do not overcome these semantic and domain failures. By the benchmark-specific mapping, the material HumanEval domain narrowing alone requires `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
