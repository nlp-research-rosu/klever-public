# Independent adversarial audit: 160-do-algebra

The candidate's files reconstruct and its result claim is discriminating, but
the submission does not contain a legitimate proof of the real program
execution. The decisive defect is at Gate A: two exact, task-specific rules in
`semantic.k` replace the whole `for` loop and the final `eval` with the desired
input-to-result summary, while `verification.k` defines the postcondition as an
alias of that same summary. There is no lower-level execution semantics or
independent K connection claim establishing either bridge. Thus `#Top` proves
the theorem only after the substantive correctness fact has already been
assumed as generated semantics.

This finding does **not** allege that the arithmetic equations are false on a
normally returning intended-domain input. I found no such counterexample.
Following the required witness rule, I classify the missing universal
execution connection as a proof/evidence gap and an illegitimate trust
boundary, not as a false-equation claim. The gap is nevertheless fatal because
it is the exact program-execution fact the proof was required to establish.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount
`/reference/reference-semantics` is absent, as required. There is no mode/mount
contradiction and hence no infrastructure breach. See
[01-integrity.log](/audit-output/evidence/01-integrity.log).

The following required candidate artifacts are present as ordinary files, not
symlinks: `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`,
`semantic.k`, `verification.k`, and `spec.k`. The candidate also contains
ordinary-file `prove.sh` and `mutation-spec.k`, plus one ordinary JSONL
structured trace. No candidate-built definition or cache was present or
reused. The scratch copies used for the audit are byte-identical to the
candidate sources; see
[15-scratch-source-identity.log](/audit-output/evidence/15-scratch-source-identity.log).

The prompt and translator pass byte-integrity checks:

- `/candidate/prompt.py` equals `/reference/prompt.py`, SHA-256
  `edeaa3bb46a2a49ef15270a996f764af73cfe463c3480bc5bcae8f04332c3620`.
- `/candidate/py2mpy.py` equals `/reference/py2mpy.py`, SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- Those hashes also agree with the corresponding untrusted claims in
  `run-input.json`.

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the structured trace only as generation claims.
They claim a prior successful build, `#Top`, and a failed candidate mutation.
None of those results was accepted or reused. Bounded excerpts and the exact
untrusted claims are in
[02-untrusted-generation-claims.log](/audit-output/evidence/02-untrusted-generation-claims.log).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says that `do_algebra(operator, operand)` receives at
least one operator from `{"+", "-", "*", "//", "**"}` and at least two
non-negative integer operands, with exactly one more operand than operator. It
must construct the infix expression in list order and return Python's
evaluation of that expression, including Python precedence, left
associativity for the additive/multiplicative groups, and right associativity
for exponentiation. The documented example is
`2 + 3 * 4 - 5 == 9`.

`/candidate/solution.py` uses the same algorithm as
`/reference/canonical.py`: stringify the first operand, append each operator
and subsequent operand using `zip`, then call `eval`. The omitted reference
docstring does not affect behavior.

I regenerated the constructor program from the scratch copy of `solution.py`
with the trusted `/reference/py2mpy.py`. The regenerated file and submitted
`solution.mpy` are byte-identical, both with SHA-256
`50f14d35a32dd3cecaa364bcf76152b345d15e00607da2efe8767b736109f2f0`;
see [03-retranslate.log](/audit-output/evidence/03-retranslate.log).

The independent differential driver is
[differential_test.py](/audit-output/evidence/differential_test.py), and the
complete generated input list is
[differential-inputs.json](/audit-output/evidence/differential-inputs.json).
It imports the trusted canonical and scratch candidate modules independently.
The 2,232 cases include the documented example, minimum-length cases, all five
operators, zero and `0 ** 0`, division by zero, every one-operator combination
over operands `0..4`, every two-operator combination over operands `0..3`,
500 deterministic longer generated expressions, all precedence/associativity
boundaries, and two explicitly labeled out-of-domain empty boundaries.

The result was zero mismatches:

- 1,973 matching integer returns;
- 258 matching `ZeroDivisionError` outcomes;
- one matching `IndexError` for empty operands.

The command, exit 0, selected concrete outcomes, and mismatch count are in
[04-differential.log](/audit-output/evidence/04-differential.log). This is
strong finite evidence that the submitted Python implementation matches the
trusted canonical; it is not evidence that the generated K execution bridges
are universally valid.

## 3. Clean proof reconstruction

All work occurred in `/tmp/audit-work`. Only candidate source files were
copied. No compiled candidate artifact was available or used. The installed
tools are K `v7.1.293` and Python `3.10.12`; see
[00-tool-versions.log](/audit-output/evidence/00-tool-versions.log).

Fresh builds succeeded:

- LLVM concrete definition from `semantic.k`:
  `kompile semantic.k --backend llvm --main-module SEMANTIC
  --syntax-module MPY-SYNTAX --output-definition
  semantic-llvm-kompiled`, exit 0
  ([05-build-concrete.log](/audit-output/evidence/05-build-concrete.log)).
- Haskell proof definition from `verification.k`:
  `kompile verification.k --backend haskell --main-module VERIFICATION
  --syntax-module MPY-SYNTAX --output-definition
  verification-haskell-kompiled`, exit 0
  ([06-build-proof.log](/audit-output/evidence/06-build-proof.log)).

The exact submitted `spec.k` was then proved. `kprove` exited 0 and printed
`#Top`; see
[07-kprove-all-candidate-claims.log](/audit-output/evidence/07-kprove-all-candidate-claims.log).
To ensure no positive claim was hidden by an aggregate invocation, I made a
label-only reviewer copy,
[spec-labeled.k](/audit-output/evidence/spec-labeled.k), and selected each
claim independently. The universal entry claim and all five ground evaluator
claims each exited 0 and printed `#Top`; see
[08a](/audit-output/evidence/08a-kprove-entry.log),
[08b](/audit-output/evidence/08b-kprove-prompt-example.log),
[08c](/audit-output/evidence/08c-kprove-right-power.log),
[08d](/audit-output/evidence/08d-kprove-floor-precedence.log),
[08e](/audit-output/evidence/08e-kprove-multiply-precedence.log), and
[08f](/audit-output/evidence/08f-kprove-left-subtraction.log).

Fresh concrete execution produced the same values as Python on normally
returning checks:

- documented example: `9`;
- minimum `0 + 0`: `0`;
- `0 ** 0`: `1`;
- right-associated `2 ** 3 ** 2`: `512`;
- mixed all-level expression: `36`;
- out-of-contract empty-operator/single-operand input: `7`.

The exact logs are
[09a](/audit-output/evidence/09a-krun-example.log),
[09b](/audit-output/evidence/09b-krun-min-add.log),
[09c](/audit-output/evidence/09c-krun-zero-power-zero.log),
[09e](/audit-output/evidence/09e-krun-right-power.log),
[09f](/audit-output/evidence/09f-krun-all-levels.log), and
[09g](/audit-output/evidence/09g-krun-no-op-one-operand.log).

The boundary behavior exposes a language-model limitation. Python raises
`ZeroDivisionError` for `7 // 0`; the K LLVM evaluator instead exits 113 with a
stuck `parseMul(...)` function
([09d-krun-floor-zero.log](/audit-output/evidence/09d-krun-floor-zero.log)).
For empty operands, Python raises `IndexError`; K stops with the unexecuted
assignment at the front of `<k>`
([09h-krun-empty-operands.log](/audit-output/evidence/09h-krun-empty-operands.log)).
The latter input is outside the stated domain. Division by zero is not
excluded by the written prompt, although both real Python implementations
raise rather than return.

Therefore clean reconstruction itself passes: sources build and every
positive claim closes. A successful reconstruction is only verification under
the candidate theory, not validation of that theory.

## 4. Adequacy and real-program pinning

### Entry claim

The precondition at `/candidate/spec.k:34` means:

1. `OS` contains exactly as many operators as `REST` contains operands;
2. every operator is one of the five allowed strings;
3. the first operand and every element of `REST` are non-negative K integers.

Because the operand cell is `Num(FIRST, REST)`, at least one operand is
required. The formal precondition does not enforce the prompt's stricter
"at least one operator / at least two operands" condition: `.Ops` paired with
`.Ints` is admitted. That is a sound domain extension for this implementation,
not a false restriction.

The postcondition says that the exact program term followed by `invoke`
reaches `answer(expected(OS, Num(FIRST, REST)))`; the operator and operand
cells remain unchanged, while the abstract expression cell changes from
`noText` to a `builder` carrying the original lists and no remaining elements.

The normalized `Module(...)` in the entry claim and the `solutionProgram`
helper both exactly match the trusted-regenerated `solution.mpy`, with equal
normalized SHA-256 values. See
[program_pinning.py](/audit-output/evidence/program_pinning.py) and
[13-program-pinning.log](/audit-output/evidence/13-program-pinning.log).
Thus there is no substituted-program defect.

A state satisfying every entry precondition is:

```text
OS   = Op("+", Op("*", Op("-", .Ops)))
FIRST = 2
REST = Num(3, Num(4, Num(5, .Ints)))
```

Here `aligned` is true, every operator is valid, and every operand is
non-negative. The fresh ground witness closes with `#Top` in
[14-precondition-witness.log](/audit-output/evidence/14-precondition-witness.log).
Substituting this state into `expected` yields `9`; the K concrete execution,
trusted canonical, and submitted Python all return `9`.

The source term is body-sensitive in a narrow syntactic sense. I changed the
loop body to append `oprn + 1`; Python then returns `16` on the prompt input,
while the trusted translation stops at the changed `For` because the
candidate's exact loop rule no longer matches. See
[body-mutation.py](/audit-output/evidence/body-mutation.py),
[12a](/audit-output/evidence/12a-body-mutation-python.log),
[12b](/audit-output/evidence/12b-body-mutation-translate.log), and
[12c](/audit-output/evidence/12c-body-sensitivity-krun.log).
This establishes exact syntax pinning, but not the semantic correctness of the
summary used when that syntax does match.

### Five ground claims

The remaining claims do not execute `solution.mpy`. Each starts with
`check(expected(...))` and constrains the corresponding ground evaluator value:
prompt example `9`, right-associated exponentiation `512`, floor-division
precedence `4`, multiplication precedence `14`, and left-associated
subtraction `5`. They are useful evaluator checks but are not additional
source-program theorems.

### Material adequacy defect

`/candidate/verification.k:30-31` defines
`expected(OS, IS) => pyEval(OS, IS)`. The source return rule at
`/candidate/semantic.k:82-84` produces
`answer(pyEval(ALLOPS, ALLINTS))`. Thus the purported independently visible
postcondition is definitionally the exact same symbol placed in the result by
the operational rule. The entry proof does not connect evaluation of the
constructed `expression` to `expected`; it receives that equality from the
generated semantics.

Likewise, `/candidate/semantic.k:64-80` does not execute the `zip` loop or the
`AugAssign`. On the guard `aligned(OS, IS)`, it consumes the complete `For` in
one step and merely changes the pending fields of `builder` to empty. There is
no loop-head semantics, invariant claim, variable environment, string state,
per-iteration update, or auxiliary execution theorem.

These are the substantive program-defined computations. Treating them as
semantic axioms and using the same `pyEval` in the postcondition is circular
with respect to the requested correctness theorem.

## 5. Rule-by-rule static soundness review

The complete numbered sources, trusted Python AST, and machine-generated
declaration index are preserved in
[10-static-source-inventory.log](/audit-output/evidence/10-static-source-inventory.log).

### Syntax and configuration inventory

All local syntax declarations are accounted for:

- `MPY-SYNTAX`: `Pgm/Module`; statement, string, parameter, and expression
  lists; `Bound` with `NoBound`; expression constructors `Name`, `Int`,
  `Call`, `Subscript`, `Slice`, `TupleExpr`, and `BinOp`; statement
  constructors `FuncDef`, `Assign`, `For`, `AugAssign`, and `Return`; recursive
  `Ops`/`Op` and `Ints`/`Num`; and `ops`/`ints` input wrappers.
- `SEMANTIC`: K items `invoke`, `exec`, and `answer`; abstract text
  `noText`/`builder`; `ParseResult`/`parsed`; `Tokens`/`tokens`; Boolean
  function `aligned`; parser functions `parsePow`, `powCombine`, `powerPass`,
  `powerNext`, `powerCons`, `parseMul`, `mulPass`, `mulNext`, and `mulCons`;
  integer functions `addPass`, `pyEval`, `afterPower`, `afterMul`, and
  `powNat`.
- `VERIFICATION`: `solutionProgram`; integer function `expected`; K items
  `check`/`checked`; and Boolean functions `validOps`, `validOperator`, and
  `nonNegative`.

The configuration contains `<k>`, `<operators>`, `<operands>`, and
`<expression>`. There is no environment, call stack, iterator, heap, exception
cell, or ordinary Python string value. That absence is central: calls,
parameter binding, slicing, `zip`, string conversion, loop iteration,
augmentation, `eval`, and exceptions cannot execute generically.

The trusted-translated program uses every declared source constructor listed
above except none: its `Module`, `FuncDef`, `Params`, `Assign`, `Name`,
`Call`, `Subscript`, `Int`, `For`, `TupleExpr`, `Slice`, `NoBound`,
`AugAssign`, `BinOp`, and `Return` are all declared. Coverage is syntactically
complete, but operational behavior is supplied only by exact whole-statement
patterns.

There are no local `[functional]`, `[simplification]`, `[concrete]`, priority,
`owise`, or opaque-symbol declarations. The only `[total]` declarations are
`aligned`, `validOps`, `validOperator`, and `nonNegative`. No rule-overlap is
hidden by priorities.

### `semantic.k` rules

Every local rule is inventoried below.

- Lines 53-54: an exact `do_algebra(operator, operand)` definition followed by
  `invoke` becomes `exec(BODY)`. It preserves the continuation and other
  cells. This is a sound dispatch step for the one supported entry shape,
  though it assumes the external configuration cells already represent
  parameter binding.
- Lines 56-62: the exact first assignment becomes a `builder` containing the
  complete input lists plus their pending tails. On a nonempty operand list,
  this is a plausible abstract summary of
  `expression = str(operand[0])`; it does not execute lookup, indexing,
  `str`, allocation, or assignment.
- Lines 64-80: the exact complete `For` is removed in one step whenever
  `aligned(OS, IS)` holds, and pending data becomes empty. This is an
  operational bridge over the property-bearing loop, not a low-level
  semantics for `For`, `zip`, tuple binding, `AugAssign`, or strings. It has
  no bridge-free connection claim over its complete match domain.
- Lines 82-84: the exact return is replaced by
  `answer(pyEval(ALLOPS, ALLINTS))`. This bypasses lookup of `expression` as a
  Python string and execution of `eval`; it obtains the result from the
  original lists stored in `builder`. This is the task's desired result
  summary and has no independent K connection claim.
- Lines 88, 89, 90, and 91: `aligned` respectively handles both-empty,
  both-nonempty recursion, operators-empty/integers-nonempty, and
  operators-nonempty/integers-empty. The cases are exhaustive, disjoint, and
  structurally descending; `[total]` is justified.
- Lines 99, 100-101, 102-103, 104-105, 106-107, and 108-109:
  `parsePow` handles the final atom, right-recursive `**`, and stopping before
  each of `+`, `-`, `*`, and `//`. These constructor/operator cases are
  disjoint. On aligned valid-operator inputs they implement the intended
  right-associative power grouping.
- Lines 110-111: `powCombine` applies `powNat` to the recursively parsed
  exponent and preserves the unconsumed suffix. This is mathematically sound
  for non-negative exponents.
- Lines 118, 119-120, 121-122, and 123-124: `powerPass`, the final and
  nonfinal `powerNext` cases, and `powerCons` recursively rebuild the token
  lists after collapsing powers. Their recursion consumes at least one
  non-power-separated group on aligned valid inputs.
- Lines 128, 129-130, 131-133, 134-135, and 136-137: `parseMul` handles a final
  atom, left-fold multiplication, guarded division, and stopping before `+`
  or `-`. The cases are disjoint. On the intended non-negative operand domain,
  powered atoms and multiplicative accumulators are non-negative, so K
  `/Int` agrees with Python `//` whenever the divisor is nonzero. A zero
  divisor has no rule, causing the observed stuck evaluator rather than a
  Python exception.
- Lines 142, 143-144, 145-146, and 147-148: `mulPass`, the final and nonfinal
  `mulNext` cases, and `mulCons` recursively rebuild the additive token list.
  The same aligned-input descent argument applies.
- Lines 152, 153-154, and 155-156: `addPass` returns the last value or
  left-folds addition/subtraction. These are ordinary integer equations and
  are disjoint on valid remaining operators.
- Lines 161, 162, and 163: `pyEval`, `afterPower`, and `afterMul` compose the
  power, multiplicative, and additive passes. These equations define the
  result summary; they do not establish its connection to execution of the
  source loop and Python `eval`.
- Lines 166 and 167-168: `powNat(_, 0) = 1` and the positive-exponent recursive
  case are disjoint and strictly decrease the exponent. They correctly model
  non-negative integer exponentiation. Negative exponents remain undefined,
  which is outside the prompt domain and cannot arise inside a power group
  from non-negative source operands.

The arithmetic function family has no detected false conclusion on a normally
returning intended input. Its partial functions are appropriately not marked
`[total]`. The finite K runs exercise zero and positive exponent cases, all
five operators, every precedence level, and both empty/nonempty alignment
boundaries. The narrower exception gap is stated above rather than mislabeled
as arithmetic unsoundness.

### `verification.k` rules

- Lines 9-24: `solutionProgram` expands to the exact trusted-translated
  program. It is a truthful nullary definitional abbreviation.
- Line 31: `expected(OS, IS) => pyEval(OS, IS)` is total as a syntactic alias
  over its arguments, but it supplies no independent property definition.
  Because the source return bridge already emits `pyEval`, this creates a
  circular result dependency.
- Line 36: `check(I) => checked(I)` is a harmless one-step test harness. It
  does not execute the source program.
- Lines 39 and 40: `validOps` handles empty and nonempty lists and descends
  structurally.
- Lines 43, 44, 45, 46, and 47 return true for each allowed operator.
  Lines 48-53 return false only under the conjunction excluding all five.
  The fallback guard is disjoint from every positive case and covers every
  other K string; `[total]` is justified.
- Lines 56 and 57-58: `nonNegative` handles empty and nonempty integer lists
  and descends structurally; `[total]` is justified.

### Claims and dependency experiment

`spec.k` contains exactly six claims: one universal entry claim and the five
ground `check(expected(...))` claims described in stage 4. There are no loop
claims, invariants, helper reachability claims, or connection theorems.

To identify the proof dependency rather than trusting comments, I removed only
the whole-loop and return/eval summaries in a scratch copy. The resulting
definition still builds
([semantic-without-execution-summaries.k](/audit-output/evidence/semantic-without-execution-summaries.k),
[16a-build-without-execution-summaries.log](/audit-output/evidence/16a-build-without-execution-summaries.log)).
The isolated entry proof then fails at the real translated `For` term with
`WarnStuckClaimState`; see
[16b-entry-proof-without-execution-summaries.log](/audit-output/evidence/16b-entry-proof-without-execution-summaries.log).

This experiment does not claim that removing language rules should leave a
proof. It establishes the relevant dependency: there is no lower-level
execution path or auxiliary K theorem behind the summaries. All entry-claim
closure beyond the first assignment comes directly from those two
task-specific rules. They therefore cross the acceptable low-level semantics
boundary and smuggle the correctness conclusion into the theory.

Gate A fails for that reason. Syntax pinning and finite agreement do not supply
the required universal execution connection.

## 6. Fresh non-vacuity test

I inspected but did not reuse `/candidate/mutation-spec.k`. The fresh reviewer
mutation is
[audit-vacuity.k](/audit-output/evidence/audit-vacuity.k). It uses the exact
program and the satisfying intended-domain input
`operators = ["+"]`, `operands = [1, 2]`, but changes the required result from
the demonstrably true `3` to `4`.

The mutation parses and compiles to KORE successfully under `kprove --dry-run`,
exit 0
([11a-vacuity-dry-run.log](/audit-output/evidence/11a-vacuity-dry-run.log)).
The real proof exits 1 with `WarnStuckClaimState`; the residual is
`answer(3)` while the destination requires `answer(4)`
([11b-vacuity-proof.log](/audit-output/evidence/11b-vacuity-proof.log)).
This is the expected unmet result obligation, not a parser failure, missing
import, timeout, or unrelated crash.

The entry result is therefore syntactically constrained and the positive proof
is not vacuous in the ordinary false-postcondition sense. This does not cure
the Gate A defect: the constrained value is still supplied by the
execution-bypassing `pyEval` bridge.

## 7. Proven versus assumed accounting

What the successful reachability proof establishes, precisely, is:

> In the candidate theory, for an exact constructor term matching
> `solution.mpy`, an input representation satisfying `aligned`, `validOps`,
> and `nonNegative` rewrites through the candidate's exact macro rules to
> `answer(pyEval(OS, Num(FIRST, REST)))`, with the expression summary marked
> complete. Five selected ground `pyEval` terms reduce to 9, 512, 4, 14, and 5.

It does not independently establish that executing the Python assignment,
`zip` loop, string concatenation, and `eval` produces that `pyEval` value.

The trust/assumption ledger is:

| Boundary | Dependents | Assessment |
|---|---|---|
| K parser, Haskell/LLVM backends, reachability engine, and imported `INT`, `STRING`, `BOOL`, list, and cell machinery | Every build, run, and proof | Ordinary toolchain trust boundary; acceptable for a K audit. |
| Trusted `py2mpy.py` faithfully maps the submitted Python AST to `solution.mpy` | Real-program identity | Trusted input plus byte-identity reconstruction; acceptable. |
| K integer `+Int`, `-Int`, `*Int`, `/Int`, comparisons, string equality, and Boolean conjunction | Arithmetic helpers and preconditions | Acceptable low-level primitives. `/Int` is used only with non-negative values on the intended normal path; zero division remains unmodeled. |
| External configuration cells are the bindings of `operator` and `operand` | All source operational rules | Informal representation assumption; no general name lookup/call binding semantics. Concerning but simple and exact for the initial configuration. |
| Lines 56-62 summarize indexing, `str`, allocation, and assignment as `builder` | Entry claim | Program-derived operational bridge with no lower-level execution or connection theorem. |
| Lines 64-80 summarize the whole `zip` loop and `AugAssign` in one step | Entry claim | Illegitimate Gate A boundary: this is a central program-defined computation, not an external primitive. Exact syntax matching and body sensitivity do not prove its value/state equivalence. |
| Lines 82-84 summarize `eval(expression)` as `pyEval` of original lists | Entry claim and returned value | Illegitimate result-bearing bridge. It bypasses the actual expression value and directly installs the task summary. |
| `expected = pyEval` | Universal postcondition and all ground claims | Circular with the preceding return bridge; it cannot independently justify that the source computation has the claimed meaning. |
| Arithmetic parser equations implement Python precedence/associativity | Meaning of `pyEval` | Static review found them mathematically correct for valid, aligned, non-negative, nonzero-divisor inputs. Concrete K checks and Python comparison are finite support, not a universal source-execution theorem. |
| Candidate Python matches trusted canonical | Natural-language implementation bridge | Supported on 2,232 differential cases with zero mismatches and by direct source inspection. It validates the Python implementation, not the K operational bridge. |
| Exception and resource behavior | Division by zero, empty operands, enormous powers | Not proved. K gets stuck where Python raises on division by zero; partial correctness for normal returns does not supply an exception-equivalence theorem. |

The candidate's prior prose, generation trace, concrete tests, and differential
results are not substitutes for the missing K connection. Because the core
loop/eval behavior is assumed in task-specific semantic rules and the
postcondition repeats the same summary, the reconstructed `#Top` is not a
legitimate proof of the real generated program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
