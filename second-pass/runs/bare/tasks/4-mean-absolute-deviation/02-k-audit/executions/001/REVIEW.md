# Independent adversarial audit: 4-mean-absolute-deviation

## Audit outcome

The candidate's source-only proof reconstruction succeeds: fresh LLVM and
Haskell definitions build, the sole positive claim exits 0 with `#Top`, the
claim executes the submitted program's constructor tree, and a fresh false
result mutation is rejected for the expected stuck result.

The proof is nevertheless **not legitimate**. The entry claim admits every
nonempty list of `Num`, including valid rational encodings with negative
denominators. The generated `absNum` rules decide sign from the numerator
alone, without an invariant or guard requiring a positive denominator. On the
satisfying input

```text
nums(rat(3,-1),rat(1,-1))
```

which denotes `[-3,-1]`, mathematical and Python MAD is `+1`, while fresh K
execution returns `rat(-8,8)`, or `-1`. Both `absNum` branches contribute to
this false result. The postcondition's `mathMAD` uses those same flawed helper
rules, so `#Top` only shows agreement between execution and an unsound
task-specific arithmetic theory. This is a material generated-semantics
soundness failure on the formal entry domain, not a testing limitation.

All paths below are candidate paths unless prefixed by `evidence/`. Candidate
logs, traces, reports, and compiled output were treated only as untrusted
claims.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`, and
`/reference/reference-semantics` does not exist. This is the required mount
state; there is no infrastructure breach and no hidden or inferred semantics
was used. The candidate's `/candidate/semantic.k` is therefore audited on its
own merits.

### Required artifacts and trusted comparisons

The following required candidate artifacts exist as regular files:

```text
run-input.json       metrics.json          codex-last.txt
codex-output.log     prompt.py             py2mpy.py
solution.py          solution.mpy          semantic.k
spec.k               verification.k        prove.sh
```

No required artifact is missing, mistyped, or symlinked, and a recursive
candidate symlink search found none. There are no generated helper K source
files. The candidate does contain an extra `verification-kompiled/` cache; it
was ignored and never copied into the reconstruction.

`prompt.py` is byte-identical to `/reference/prompt.py`, with SHA-256
`2717edd5d203ea22a6eebf62263effd9b792e1a2ef93e017868cedaac7b5ef10`.
`py2mpy.py` is byte-identical to `/reference/py2mpy.py`, with SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
Both values agree with the untrusted provenance claims in `run-input.json`.

`metrics.json`, `codex-last.txt`, `codex-output.log`, and the one structured
JSONL generation trace were read only as claims. They report a successful
generation and prior `#Top`, but none was used as proof evidence.

Evidence:

- [`evidence/01_integrity.sh`](evidence/01_integrity.sh) is the reviewer-authored check.
- [`evidence/01_integrity.log`](evidence/01_integrity.log) records every command,
  artifact type, hash, exit status, and bounded excerpts from the untrusted run
  claims.

Stage 1 result: **pass**.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a supplied list of numbers, calculate its arithmetic mean, take the
absolute difference of each element from that mean, then return the average of
those absolute differences. The documented example `[1.0, 2.0, 3.0, 4.0]`
returns `1.0`.

The prompt does not define the empty-list case. The trusted canonical Python
implementation divides by `len(numbers)` and therefore raises
`ZeroDivisionError` on an empty list.

### Source fidelity

`solution.py` computes:

```python
mean = sum(numbers) / len(numbers)
return sum([abs(x - mean) for x in numbers]) / len(numbers)
```

The trusted canonical implementation uses a generator rather than a list
comprehension for the second `sum`, but has the same evaluation order and
numeric result. The candidate preserves the required signature and entry-point
name.

Running the trusted `/reference/py2mpy.py` over the scratch copy of
`solution.py` generated a file byte-identical to submitted `solution.mpy`.
Both have SHA-256
`468cdf1deeb199660cf330c02f1622195cacd82f10142d05fbbbef44b0ed934e`.

### Independent differential test

The reviewer-authored test imports `/reference/canonical.py` and the scratch
candidate from different explicit paths. It records every input and both
outcomes. The corpus contains 217 cases:

- the documented example;
- empty and singleton boundaries;
- equal values, opposite signs, negative zero, negative/zero/positive
  deviations, duplicates, fractional values, cancellation, tiny and large
  finite floats;
- infinity and NaN observations;
- 100 deterministic generated lists from a boundary pool;
- 100 deterministic generated finite-float lists.

There were zero mismatches. Empty input raised `ZeroDivisionError` in both
Python implementations. This finite test supports implementation-to-canonical
fidelity only; it is not a universal theorem and does not validate the K
semantics.

Evidence:

- [`evidence/02_program_checks.sh`](evidence/02_program_checks.sh) and
  [`evidence/02_differential.py`](evidence/02_differential.py).
- [`evidence/02_program_checks.log`](evidence/02_program_checks.log) contains
  all 217 inputs and outcomes, the zero-mismatch summary, hashes, commands, and
  exit statuses.

Stage 2 result: **pass** for candidate-versus-canonical fidelity.

## 3. Clean proof reconstruction

Only these source artifacts were copied to `/tmp/audit-work/reconstruction`:

```text
prompt.py  py2mpy.py  solution.py  solution.mpy
semantic.k  verification.k  spec.k  prove.sh
```

No candidate definition, cache, or compiled file was reused.

Using K version `v7.1.293`, the reviewer ran:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --output-definition semantic-kompiled

kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition verification-kompiled

kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Both builds exited 0. The sole positive proof command exited 0 and printed
exactly `#Top`.

### Fresh generated-semantics execution

Fresh LLVM execution produced:

| Input | K result | Mathematical value | Independent oracle |
|---|---:|---:|---:|
| `[1,2,3,4]` | `rat(1024,1024)` | `1` | `1` |
| `[5]` | `rat(0,1)` | `0` | `0` |
| `[-2,0,2]` | `rat(108,81)` | `4/3` | `4/3` |
| `[1/2,3/2]` | `rat(256,512)` | `1/2` | `1/2` |

These normal and nonempty boundary cases agree.

The concrete empty input `nums()` terminates with `rat(0,0)`, whereas both real
Python implementations raise `ZeroDivisionError`. The formal entry claim
excludes empty lists by its `nums(H,T)` shape, so this is a language-model
adequacy limitation rather than the decisive proof failure.

Fresh execution also exposed noncanonical-denominator behavior; the stronger
false-result witness is analyzed in Stage 5.

Evidence:

- [`evidence/03_reconstruct.sh`](evidence/03_reconstruct.sh) and the independent
  exact-rational observations in
  [`evidence/03_python_oracle.py`](evidence/03_python_oracle.py).
- [`evidence/03_reconstruct.log`](evidence/03_reconstruct.log) records the
  source-only builds, all concrete runs, tool versions, the positive `#Top`,
  and exit statuses.
- [`evidence/03_rebuild_preparation.log`](evidence/03_rebuild_preparation.log)
  records the recoverable relocation of the first reviewer-built definitions
  before the final clean rerun.

Stage 3 result: **pass** for clean positive-proof reconstruction; generated
semantics fidelity has the material Stage 5 failure.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The claim has no explicit `requires` clause. Its source configuration provides:

- `<k>` equal to `init(solutionProgram, nums(H,T))`;
- `<env>` equal to `emptyEnv`;
- `<result>` equal to `noResult`.

Sort inference makes `H` a `Num` and `T` a `Nums` list, so the input is
structurally nonempty. There is no restriction that a `rat(A,B)` denominator be
positive or even nonzero.

At termination it requires:

- `<k>` to be consumed as `.K`;
- `<env>` to contain `mean` bound to
  `divNum(sumNums(H,T),countNums(H,T))`, followed by the original `numbers`
  binding;
- `<result>` to equal `result(mathMAD(H,T))`.

Thus the returned value is an exact destination term, not a free variable,
tautology, implication, or omitted cell.

### Real control flow

The claim follows the actual submitted control flow:

1. `init` unwraps the module.
2. `seekTarget` ignores only the `typing.List` import and selects the actual
   unary `mean_absolute_deviation(numbers)` definition.
3. `exec(Assign(...))` evaluates `sum(numbers) / len(numbers)` and binds
   `mean`.
4. `exec(Return(...))` evaluates the submitted list comprehension and final
   division.
5. `finish` writes the computed value to `<result>` and consumes `<k>`.

There is no loop and no auxiliary loop claim. No source helper function is
replaced. The task-specific comprehension fusion is assessed as an operational
semantic rule in Stage 5.

### Program identity

`verification.k`'s `solutionProgram` equation is a readable wrapper around the
same constructor tree as regenerated `solution.mpy`. The only textual
difference with empty `FreeVars()` is K's internal `.Strings` spelling.
Manual constructor-by-constructor review found no substituted expression,
statement, binding, or continuation.

As a dynamic check, the submitted MPY and a separately parsed copy of the
claim's right-hand constructor tree produced byte-identical final
configurations on the documented input. This dynamic check supports, but does
not replace, the static tree comparison.

### Satisfying states and concrete substitutions

A concrete satisfying state is:

```text
<k> init(solutionProgram,
     nums(rat(1,1),rat(2,1),rat(3,1),rat(4,1))) </k>
<env> emptyEnv </env>
<result> noResult </result>
```

Here `H = rat(1,1)` and
`T = rat(2,1),rat(3,1),rat(4,1),.Nums`. Substitution in the destination gives
mean `rat(10,4)` and result `rat(1024,1024) = 1`. Both Python implementations
return float `1.0`. A second substitution `[-2,0,2]` gives
`rat(108,81) = 4/3`, also agreeing with both Python implementations.
Reviewer-authored ground claims with those direct result terms exited 0 and
printed `#Top`.

Evidence:

- [`evidence/04_ground_spec.k`](evidence/04_ground_spec.k),
  [`evidence/04_claimProgram.mpy`](evidence/04_claimProgram.mpy), and
  [`evidence/04_adequacy_checks.sh`](evidence/04_adequacy_checks.sh).
- [`evidence/04_adequacy_checks.log`](evidence/04_adequacy_checks.log) records
  both executions, the exact comparison, concrete ground proof, and exits.

Stage 4 result: **pass** for program identity, control-flow pinning, and result
constraint. The unrestricted rational representation makes the intended-result
claim fail in Stage 5.

## 5. Rule-by-rule static soundness review

### Complete local syntax and declaration inventory

There are no generated helper K source files.

`MPY-SYNTAX` declares:

- `ModuleAst`: `Module(Stmts)`;
- list sorts `Stmts`, `Strings`, `Exprs`, and `CompFors`;
- metadata wrappers `Params(Strings)`, `CellVars(Strings)`, and
  `FreeVars(Strings)`;
- `Stmt`: `ImportFrom`, three-field `FuncDef`, five-field `FuncDef`, `Assign`,
  and `Return`;
- `Expr`: `Name`, `Int`, `Float`, `Bool`, `BinOp`, `Call`, and `ListComp`;
- `CompFor`: `CompFor(Expr,Expr,Exprs)`.

`SEMANTIC` declares:

- `Num`: constructor `rat(Int,Int)` and functions `addNum`, `subNum`,
  `divNum`, `absNum`, `sumNums`, `countNums`, `sumAbs`, and `asNum`;
- list sort `Nums`;
- `Value`: injected `Num`, `nums(Nums)`, and
  `comprehension(Expr,String,Nums,Env)`;
- `Env`: `emptyEnv` and `bind(String,Value,Env)`;
- functions `lookup`, `eval`, `sumValue`, `lenValue`, `absValue`, `subValue`,
  `divValue`, and `makeComp`;
- `Result`: `noResult` and `result(Value)`;
- control items `init`, `seekTarget`, `exec`, `setVar`, and `finish`.

`VERIFICATION` adds exactly two function declarations:
`solutionProgram : ModuleAst` and `mathMAD(Nums) : Num`.

There are 18 local `[function]` declarations in total. There are no `[total]`,
`[functional]`, `[simplification]`, `[concrete]`, priority, `owise`, `opaque`,
`anywhere`, or macro declarations. Consequently there are no local
simplification rules, priority rules, or opaque symbols to account for.
Partial functions visibly get stuck outside their modeled cases.

The configuration has only `<k>`, `<env>`, and `<result>` under `<mad>`. The
submitted program needs no heap, allocation, I/O, exception, or call stack.

### Used-construct coverage

Every constructor in `solution.mpy` is declared and covered on its actual path:

| Submitted construct | Declaration and behavior |
|---|---|
| `Module`, `ImportFrom`, five-field `FuncDef` | module/statement syntax; rules R1–R3 |
| `Params`, `CellVars`, `FreeVars` | metadata syntax; target matching in R3 |
| `Assign`, `Return` | statement syntax; R7–R10 |
| `Name` | expression syntax; R13 and R11–R12 |
| `BinOp("/")`, `BinOp("-")` | expression syntax; R15–R16 and numeric dispatch |
| `Call(sum)`, `Call(len)`, `Call(abs)` | expression syntax; R17–R19 |
| `ListComp`, `CompFor`, `Bool(true)` | expression/comprehension syntax; R20–R21 and R27 |

`Float`, generic `Bool` evaluation, other operators, other calls, other
comprehension filters, and generic Python functions are unmodeled but unused.
Under the generated-semantics boundary, that minimal unused-construct coverage
is not a defect.

### Exhaustive rule inventory and decision

The following inventory accounts for all 39 rules in `semantic.k` and both
rules in `verification.k`.

| ID | Source | Rule role | Decision |
|---|---|---|---|
| R1 | `semantic.k:82` | `init(Module(...),ARGS)` starts module search | Sound for the configured entry mechanism; preserves continuation and other cells. |
| R2 | `:83` | Skip `ImportFrom` | Sound for the actual side-effect-free `typing.List` import in this model. |
| R3 | `:85` | Select exact target name/parameter and install `numbers` | Sound for the submitted module; binding, body, and environment are pinned. |
| R4 | `:89` | Skip three-field functions | Constructor-disjoint from R3; unused but sound as search. |
| R5 | `:91` | Skip other five-field functions under name disequality | Guard makes it disjoint from R3; sound as search. |
| R6 | `:96` | Consume empty statement list | Sound sequencing base case. |
| R7 | `:97` | Evaluate assignment RHS, then continue | Sound for actual pure expression; captures the pre-assignment environment. |
| R8 | `:100` | Prepend binding | Sound newest-binding/shadowing update. |
| R9 | `:102` | Evaluate `Return`, discard remaining statements | Correct abrupt-return behavior for this function body. |
| R10 | `:104` | Store result and consume computation | Sound when `<result>` is initially `noResult`, as the configuration and claim require. |
| R11 | `:108` | Lookup newest matching binding | Sound. |
| R12 | `:109` | Recurse past a nonmatching binding | Sound; guard excludes R11 overlap. |
| R13 | `:114` | Evaluate `Name` via lookup | Sound for the actual bound names. |
| R14 | `:115` | Evaluate integer literal as denominator-one rational | Sound; unused by submitted expressions. |
| R15 | `:116` | Evaluate subtraction operands and dispatch | Structurally sound; final numeric fidelity depends on R30 and the later absolute-value rules. |
| R16 | `:118` | Evaluate division operands and dispatch | Structurally sound on the target path; zero-divisor behavior depends on R31. |
| R17 | `:120` | Evaluate unary `sum` call | Sound for the actual pure argument. |
| R18 | `:121` | Evaluate unary `len` call | Sound for the actual list value. |
| R19 | `:122` | Evaluate unary `abs` call | Correct dispatch shape, but its observable result inherits the R32/R33 failure. |
| R20 | `:123` | Build a true-filter comprehension with lexical environment | Sound for the exact submitted comprehension. |
| R21 | `:126` | Require a `nums` iterable and retain the environment | Sound for the actual `numbers` binding. |
| R22 | `:127` | Sum a numeric list via `sumNums` | Sound delegation. |
| R23 | `:128` | Length of a numeric list via `countNums` | Sound delegation. |
| R24 | `:129` | Numeric absolute-value dispatch | Its result inherits the concrete R32/R33 unsoundness. |
| R25 | `:130` | Numeric subtraction dispatch | Sound delegation. |
| R26 | `:131` | Numeric division dispatch | Sound delegation on the nonempty entry path. |
| R27 | `:136` | Fuse `sum(abs(x-center) for x in list)` into `sumAbs` | A result-bearing operational bridge, fully constrained by recursive R38/R39 rather than an oracle. It is mathematically the submitted fold when binder `X` and center variable `M` differ, as the real AST fixes `"x"` and `"mean"`. The rule lacks an `X =/=String M` guard and would mishandle a different program where they coincide; that is a reuse/scope gap, not an unsoundness finding on this submitted program's input domain. |
| R28 | `:140` | Project a numeric value | Sound on the target path. |
| R29 | `:143` | Rational addition by cross multiplication | Correct for nonzero denominators, including negative ones. |
| R30 | `:145` | Rational subtraction by cross multiplication | Correct for nonzero denominators, including negative ones. |
| R31 | `:147` | Rational division by cross multiplication | Correct only for a nonzero divisor. It lacks an exception/zero guard; `nums()` concretely returns `rat(0,0)` instead of Python's exception. Empty is outside the entry claim, so this is an adequacy gap rather than the decisive witness. |
| R32 | `:149` | `absNum` when numerator is negative | **Unsound on the formal entry domain.** It assumes the denominator is positive; the concrete witness below exercises it and produces a false result. |
| R33 | `:151` | `absNum` when numerator is nonnegative | **Unsound on the formal entry domain.** It makes the same unasserted denominator-sign assumption; the same witness exercises it. |
| R34 | `:154` | Empty numeric sum is zero | Sound. |
| R35 | `:155` | Recursive numeric sum | Sound and descending on the list, subject to R29's nonzero-denominator interpretation. |
| R36 | `:156` | Empty count is zero | Sound. |
| R37 | `:157` | Recursive count | Sound, descending, and produces a positive count for `nums(H,T)`. |
| R38 | `:158` | Empty absolute-deviation sum is zero | Sound base case. |
| R39 | `:159` | Recursive absolute-deviation sum | Correct fold structure and descending; its values inherit R32/R33's false absolute values. |
| V1 | `verification.k:8` | Expand `solutionProgram` to the submitted constructor tree | Sound definitional abbreviation; no opaque or fresh value. |
| V2 | `verification.k:29` | Define `mathMAD` using `sumAbs`, `sumNums`, `countNums`, and `divNum` | Syntactically total over finite `Nums` in the used path and not opaque, but its claimed mathematical interpretation is false wherever R32/R33 are false. It repeats the flawed operational helpers rather than independently establishing mathematical MAD. |

Evaluation is deterministic on the target path. The only apparent rule
overlaps are disjoint by constructor, literal function name, or explicit
guards: R3/R5, R11/R12, the three builtin-call rules, the two `sumValue`
shapes, and R32/R33. Recursion in lookup and the three list folds descends.
There are no priorities capable of hiding another target-path rule.

### Required false-conclusion witness

The claim's `nums(H,T)` pattern is satisfied by:

```text
H = rat(3,-1)
T = rat(1,-1), .Nums
```

The denominators are nonzero, and these terms denote the ordinary rationals
`-3` and `-1`. Their mean is `-2`; their true mean absolute deviation is `1`.

The candidate semantics derives center `rat(-4,2) = -2`. For the first
deviation, R30 produces `rat(2,-2) = -1`; R33 sees the nonnegative numerator
and incorrectly leaves the negative value unchanged. For the second deviation,
R30 produces `rat(-2,-2) = +1`; R32 sees the negative numerator and
incorrectly changes it to `rat(2,-2) = -1`. The final average is therefore
`-1`.

Fresh execution of the actual submitted `solution.mpy` returns:

```text
<result> result ( rat ( -8 , 8 ) ) </result>
```

The independent `fractions.Fraction` oracle returns `+1` and asserts that
value. This is a concrete false conclusion enabled by both inventoried
`absNum` rules on a state satisfying the entry precondition. No candidate
compiled artifact participates.

Evidence:

- [`evidence/05_static_inventory.sh`](evidence/05_static_inventory.sh) and
  [`evidence/05_static_inventory.log`](evidence/05_static_inventory.log)
  enumerate the sources, all 39+2 rules, all attributes, and counts.
- [`evidence/05_unsound_witness.sh`](evidence/05_unsound_witness.sh),
  [`evidence/05_negative_denominator_oracle.py`](evidence/05_negative_denominator_oracle.py),
  and [`evidence/05_unsound_witness.log`](evidence/05_unsound_witness.log)
  preserve the exact witness, independent oracle, fresh K command, outputs,
  and exit statuses.

Stage 5 result: **fail**. R32/R33 are materially unsound for a formally admitted
rational input, and V2 shares rather than discharges that flaw.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present or trusted. The reviewer created a
new ground claim for the satisfying documented input while changing only the
result-bearing destination from the true value `rat(1024,1024)` to the false
value `rat(0,1)`.

`kprove --dry-run` parsed and built the mutation successfully with exit 0. The
actual proof exited 1 with `WarnStuckClaimState`; the residual final
configuration contains the real `result(rat(1024,1024))`, which does not unify
with the false destination. This is the expected unmet result obligation, not
a parser failure, missing import, timeout, or unrelated crash.

Evidence:

- [`evidence/06_spec_vacuity.k`](evidence/06_spec_vacuity.k) is the preserved
  mutation.
- [`evidence/06_nonvacuity.sh`](evidence/06_nonvacuity.sh) and
  [`evidence/06_nonvacuity.log`](evidence/06_nonvacuity.log) record the dry run,
  proof, exit 1, stuck diagnostic, residual configuration, and harness success.

Stage 6 result: **pass**. The positive claim is result-constraining and
non-vacuous. This does not repair an unsound semantic theory.

## 7. Proven versus assumed accounting

### What the successful reachability proof actually establishes

Under the candidate's generated K rewrite theory, starting with
`init(solutionProgram,nums(H,T))`, empty environment, and no result, symbolic
execution reaches `.K`, binds `numbers` and the theory's computed `mean`, and
returns the theory's `mathMAD(H,T)` for every nonempty syntactic `Num` list.
It also establishes the exact final environment shown in the destination.

The proof does **not** establish that:

- every admitted `rat(A,B)` is interpreted correctly as a mathematical
  rational;
- `mathMAD` equals mathematical mean absolute deviation over the claim's whole
  domain;
- exact-rational execution matches CPython binary floating-point behavior;
- empty input raises the real program's exception;
- NaN, infinity, overflow, rounding, or arbitrary Python values are modeled.

### Trust and assumption ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K parser, compiler, LLVM/Haskell backends, reachability prover | Executes and proves all claims | Ordinary toolchain trust boundary; version and fresh commands are recorded. |
| Builtin `Int`, `Bool`, `String`, list, arithmetic, and comparison operations | Support every semantic rule | Ordinary low-level trusted primitives. |
| Candidate-generated operational semantics R1–R39 | Defines the language being proved | Must be validated here because no reference semantics exists. R32/R33 fail that validation materially. |
| `solutionProgram` equation V1 | Pins the proof to the submitted constructor tree | Acceptable definitional abbreviation, statically and dynamically checked. |
| Comprehension fusion R27 plus recursive R38/R39 | Replaces per-element comprehension execution with a fold that affects the final result | No opaque oracle: the value is recursively fixed. Hand validation supports the exact target pattern (`x` distinct from `mean`), but the rule is not generally reusable when binder and center coincide. Its final values still depend on invalid R32/R33. |
| `mathMAD` V2 | Supplies the postcondition's result | A definitional summary, not an independent theorem connecting execution to ordinary mathematics. It shares the flawed helpers and therefore cannot justify the advertised interpretation. |
| Rational representation invariant | Needed by R32/R33 | Illegitimately assumed. No syntax restriction, `requires`, guard, normalization rule, or connection theorem imposes a positive denominator. This missing invariant is the decisive failure. |
| Nonzero-divisor/exception behavior | Needed for Python fidelity | Not modeled. Nonempty claim inputs make count nonzero, but the broader language model returns `rat(0,0)` on empty input. |
| Trusted translator regeneration | Connects `solution.py` to `solution.mpy` | Byte identity is strong artifact evidence, but not part of the K theorem. |
| Canonical-vs-candidate differential corpus | Supports Python implementation fidelity | 217 finite observations with zero mismatches; not a universal proof and not a semantics connection theorem. |
| Exact-rational-to-Python-float bridge | Needed to lift the K theorem to the annotated `List[float]` function | Informal and incomplete. Normal tested values agree, but rounding and exceptional behavior are outside the K theorem. |

There are no opaque symbols, unconstrained fresh values, proof-local lemmas,
simplification rules, priority rules, or totality declarations. Differential
testing and the successful mutation are properly treated as supporting
evidence, not substitutes for semantic soundness.

### Gate and decision summary

- Real-program identity, control-flow pinning, result constraint, clean
  reconstruction, and non-vacuity pass.
- Real-program semantic soundness fails because R32/R33 produce a false result
  for a concrete state satisfying the entry precondition.
- Intent adequacy also has narrower limitations: exact rationals replace
  Python floats, and empty-input exception behavior is not modeled.
- Reproducibility is adequate; all reviewer-authored scripts and bounded logs
  are preserved under `evidence/`.

Because a material unsound semantic rule makes the advertised mathematical
postcondition false on the formal entry domain, the reconstructed `#Top` is not
a legitimate partial-correctness proof of the real generated program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
