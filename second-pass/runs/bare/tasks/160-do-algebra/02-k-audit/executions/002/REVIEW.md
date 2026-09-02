# Independent adversarial audit: 160-do-algebra

## Executive conclusion

The candidate Python implementation is faithful to the trusted canonical
implementation on the stated ordinary behavior, `solution.mpy` is an exact
trusted translation, and a clean reconstruction makes the submitted K claims
print `#Top`. The proof is nevertheless not legitimate.

The generated semantics does not execute the submitted assignment, lookups,
`str` calls, slice, `zip`, loop iterations, tuple bindings, concatenations, or
`eval`. Four task-shaped operational rules recognize the exact AST and replace
those operations with a raw-input summary. The return rule emits
`pyEval(ALLOPS, ALLINTS)`, while the postcondition defines `expected` to be the
same `pyEval` term. There is no bridge-free semantics or connection theorem
establishing that the skipped source execution produces this value.

This is not merely a missing explanatory lemma:

1. On the contract-valid witness `operator=["+"]`,
   `operand=[10**4300, 0]`, both trusted and candidate Python raise
   `ValueError` while converting the 4301-digit integer with `str`; the K
   semantics bypasses that operation and returns the integer normally.
2. An audit-only opposite interpretation `pyEval(_OS,_IS) => 0` still proves
   the unchanged universal entry claim with `#Top`. On the prompt input, that
   altered K execution returns 0 while trusted Python returns 9. This
   demonstrates that claim closure follows the shared execution/postcondition
   symbol rather than independently validating the result.
3. On the smaller contract-valid input `operator=["//"]`,
   `operand=[1,0]`, Python raises `ZeroDivisionError` and concrete K execution
   fails at `parseMul`, yet a ground reachability claim to the same undefined
   `expected` summary prints `#Top`.

The fresh false-result mutation does fail correctly. Thus the theory
discriminates between concrete result constants after accepting its summary,
but this does not repair the circular and behaviorally false source-to-summary
bridge.

All commands and actual statuses are indexed in
[evidence/COMMANDS.md](/audit-output/evidence/COMMANDS.md).

## 1. Input and provenance integrity

### Declared layout and semantics boundary

`/audit-input.json` declares:

- problem `160-do-algebra`;
- generation condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- `mount_reference_semantics: false`.

`/reference/reference-semantics` is absent, as this mode requires. I did not
search for or infer a hidden reference semantics. The candidate's own
`semantic.k` is therefore the language definition audited in stages 3–5.

Every launcher-required file for `legacy-selected-stage1` is present, readable,
regular, and not a symlink:

- `/audit-input.json`, `/audit-campaign-lock.json`;
- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`;
- `/generation-evidence/metrics.json`;
- `/generation-evidence/usage.json` (present and inspected);
- `/generation-evidence/codex-last.txt`;
- `/generation-evidence/codex-output.log`;
- `/generation-evidence/prompt.txt`;
- the JSONL below `/generation-evidence/codex-trace/`;
- `/reference/canonical.py`, `/reference/prompt.py`,
  `/reference/py2mpy.py`;
- the `/candidate` mount.

Historical `runtime-metrics.json` is absent. That is permitted for this legacy
layout and was not reconstructed or counted as a defect.

### Hash and campaign checks

The campaign object in `/audit-input.json` is JSON-equal to
`/audit-campaign-lock.json`. Its lock SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the recorded value.

Every recorded per-file SHA-256 checked in `audit-input.json` matches the
mounted bytes, including the run, task, invocation, stage result, metrics,
usage, prompt, Codex output, last message, canonical source, trusted prompt,
and translator. The sole trace JSONL has SHA-256
`31dae6143689e63cdfda1867d310701448f395adb11bcd21460b688e3cb60a50`,
matching `generation-result.json`.

Using the installed pipeline tree-digest implementation, the mounted candidate
hash is
`01ec6934c0c2f36093e36fad65747de5cd194eacc48c2277ce2af978abc110a7`.
That exactly matches both the stage result's and invocation's retained
workspace hash. The independently computed trace-tree hash is
`7490e7856ca9e6d83da53d560fb3fca0b52c4612d01f2be4b2853fb82eab48ca`,
matching `usage.json`'s `source_trace_sha256`.

`audit-input.json` also contains launcher aggregate fields
`candidate_tree_sha256=92edd...` and
`generation_codex_trace_sha256=2ed2...`; their hashing serialization is not
declared and is different from the installed pipeline tree serialization.
The content-level hashes and the independent standard pipeline cross-record
hashes above all agree, so this is recorded as a hash-method distinction, not
evidence of a changed mount.

Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
mounted versions. No candidate, reference, or generation-evidence entry is a
symlink. Complete results are in
[stage1-integrity.log](/audit-output/evidence/stage1-integrity.log) and
[stage1-candidate-files-sha256.log](/audit-output/evidence/stage1-candidate-files-sha256.log).

### Generation records

The structured trace contains 146 valid JSON records. The audit parser read
every record and inventoried 20 tool calls and 20 outputs. The generation
records claim a successful positive proof and an expected failed mutation;
those claims were not trusted. They were independently reconstructed below.
See [trace_summary.py](/audit-output/evidence/trace_summary.py) and
[stage1-trace-summary.log](/audit-output/evidence/stage1-trace-summary.log).

Stage 1 result: **PASS**. There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt requires two lists:

- `operator` contains at least one member of `{"+", "-", "*", "//", "**"}`;
- `operand` contains non-negative integers and has one more member than
  `operator`;
- the function constructs the corresponding unparenthesized expression and
  returns Python's evaluation, including Python precedence and associativity.

The prompt does not exclude zero divisors or bound integer size. Consequently,
some stated-domain inputs raise during source execution rather than return a
value. A faithful semantics must preserve that distinction or explicitly state
and justify a narrower normal-return domain.

### Implementation and translation

The candidate body is the canonical body apart from non-semantic formatting
and omission of the canonical docstring:

```python
expression = str(operand[0])
for oprt, oprn in zip(operator, operand[1:]):
    expression += oprt + str(oprn)
return eval(expression)
```

The trusted translator was run from scratch:

```sh
python3 /tmp/audit-work/160-do-algebra/reference/py2mpy.py \
  /tmp/audit-work/160-do-algebra/candidate/solution.py \
  > /tmp/audit-work/160-do-algebra/regenerated-solution.mpy
cmp /tmp/audit-work/160-do-algebra/regenerated-solution.mpy \
  /tmp/audit-work/160-do-algebra/candidate/solution.mpy
```

Both files have SHA-256
`50f14d35a32dd3cecaa364bcf76152b345d15e00607da2efe8767b736109f2f0`;
`cmp` exited 0. See
[stage2-translation.log](/audit-output/evidence/stage2-translation.log).

### Independent differential test

[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted canonical and candidate entry points independently and compares either
the typed return value or exception type. It covers:

- 14 explicit documented, minimum-shape, zero, associativity, precedence,
  exception, and long-loop cases;
- all operator sequences of lengths 1 and 2 with operands in `0..4`;
- all operator sequences of length 3 with operands in `0..2`;
- 500 seeded cases of lengths 3–10 over `+`, `-`, `*`, and `//` with operands
  in `0..20`.

Actual result: 13,889 cases, 11,804 returns, 2,085 matching exceptions, zero
mismatches, exit 0. See
[stage2-differential.log](/audit-output/evidence/stage2-differential.log).
This is finite implementation-fidelity evidence, not a K proof.

Stage 2 result: **PASS** for submitted implementation and translation fidelity.

## 3. Clean proof reconstruction

All candidate sources were copied to
`/tmp/audit-work/160-do-algebra/candidate`. No candidate-compiled definition or
cache was present or reused.

### Fresh definitions

The concrete definition was built from `semantic.k`:

```sh
kompile semantic.k --backend llvm \
  --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/160-do-algebra/concrete-kompiled
```

The proof definition was independently built from `verification.k`:

```sh
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/160-do-algebra/proof-kompiled
```

Both exited 0. Logs:
[stage3-kompile-concrete.log](/audit-output/evidence/stage3-kompile-concrete.log)
and [stage3-kompile-proof.log](/audit-output/evidence/stage3-kompile-proof.log).

### Positive claims

The unmodified aggregate command

```sh
kprove spec.k \
  --definition /tmp/audit-work/160-do-algebra/proof-kompiled \
  --spec-module SPEC
```

printed `#Top` and exited 0. I then copied the same six claims into
[audit-labeled-spec.k](/audit-output/evidence/audit-labeled-spec.k), adding only
labels, and selected each claim independently. All six printed `#Top` and
exited 0:

1. universal entry claim;
2. prompt example;
3. right-associative exponentiation;
4. floor-division precedence;
5. multiplication precedence;
6. left-associative subtraction.

See [stage3-kprove-all.log](/audit-output/evidence/stage3-kprove-all.log) and
[stage3-kprove-individual.log](/audit-output/evidence/stage3-kprove-individual.log).

### Generated-semantics concrete execution

Fresh `krun` executions returned the same normal values as Python for:

- prompt case: 9;
- minimum subtraction `0 - 1`: -1;
- `0 ** 0`: 1;
- `2 ** 3 ** 2`: 512;
- `20 // 3 // 2`: 3.

For `[1,0]` with `["//"]`, concrete K exited 113 with a residual
`parseMul(Op("//",...), Num(1,Num(0,...)))`; both Python implementations raise
`ZeroDivisionError`. K does not model the exception as a language result.
See [stage3-concrete-execution.log](/audit-output/evidence/stage3-concrete-execution.log).

Stage 3 result: **PASS** for mechanical clean reconstruction. A reconstructed
`#Top` is only closure under this candidate-generated theory.

## 4. Adequacy and real-program pinning

### Entry precondition in plain language

The universal entry claim quantifies an operator spine `OS`, first operand
`FIRST`, and remaining operands `REST`. It requires:

- `aligned(OS, REST)`: one remaining operand per operator;
- every operator in `OS` is one of the five prompt operators;
- `FIRST` and every member of `REST` are non-negative.

It requires at least one operand but does not require a non-empty operator
list. This over-approximates the source domain by also allowing one operand and
no operator; it does not narrow away the prompt's ordinary valid shapes. It
also fails to restrict zero divisors or source operations that may raise.

### Entry postcondition in plain language

The claim says the exact module term followed by `invoke` reaches
`answer(expected(OS, Num(FIRST,REST)))`, while the expression cell changes from
`noText` to `builder(original operators, original operands, .Ops, .Ints)`.
`expected(OS,IS)` immediately rewrites to `pyEval(OS,IS)`.

This is syntactically result-bearing, but semantic lines 82–84 directly produce
the same `pyEval` term; therefore the postcondition is not an independent
characterization of the actual returned value.

### Program identity

[program_term_compare.py](/audit-output/evidence/program_term_compare.py)
tokenizes balanced constructor terms and mechanically compares:

- trusted-regenerated `solution.mpy`;
- the `Module(...)` executed by the entry claim;
- the `Module(...)` defined by `solutionProgram`.

All three have 139 constructor tokens and are identical. See
[stage4-program-term.log](/audit-output/evidence/stage4-program-term.log).

Thus the claim pins the submitted AST. The defect is how the generated
semantics executes that AST, not substitution of another AST.

An audit body mutation changed the loop-body constructor from appending
`oprt + str(oprn)` to appending only `str(oprn)`. Its dry-run built
successfully, and its proof exited 1 with `WarnStuckClaimState` at the changed
`For` term. This confirms source-term sensitivity of the task-shaped matching
rule. See
[audit-body-mutation-spec.k](/audit-output/evidence/audit-body-mutation-spec.k),
[stage4-body-mutation-dry-run.log](/audit-output/evidence/stage4-body-mutation-dry-run.log),
and
[stage4-body-mutation-proof.log](/audit-output/evidence/stage4-body-mutation-proof.log).

### Satisfiable precondition and substitution

The prompt state

```text
OS    = Op("+", Op("*", Op("-", .Ops)))
FIRST = 2
REST  = Num(3, Num(4, Num(5, .Ints)))
```

satisfies all three predicates. A fresh witness spec proved those predicates
reduce to true and proved the ground execution reaches `answer(9)`. Trusted
canonical and candidate Python also return 9. See
[audit-witness-spec.k](/audit-output/evidence/audit-witness-spec.k) and
[stage4-satisfying-witness.log](/audit-output/evidence/stage4-satisfying-witness.log).

Stage 4 result: **FAIL for semantic adequacy**, despite passing constructor
identity. The exact AST is present, but its material operations and control
effects are bypassed.

## 5. Rule-by-rule static soundness review

The machine-extracted starting inventory is
[stage5-rule-inventory.log](/audit-output/evidence/stage5-rule-inventory.log).
There are 36 local rules in `semantic.k`, 13 in `verification.k`, and six
claims in `spec.k`.

### Syntax and configuration inventory

All local syntax declarations are:

| File/lines | Declaration(s) | Review |
|---|---|---|
| `semantic.k:5` | `Pgm ::= Module(Stmts)` | Matches the translated module. |
| `semantic.k:6-9` | `Stmts`, comma-separated `Strings`, `Params`, comma-separated `Exprs` lists | Sufficient for the submitted term. |
| `semantic.k:11` | `Bound ::= Expr \| NoBound` | Covers the submitted slice bounds. |
| `semantic.k:12-18` | `Name`, `Int`, `Call`, `Subscript`, `Slice`, `TupleExpr`, `BinOp` expressions | Exactly the expression constructors used by `solution.mpy`. |
| `semantic.k:20-24` | `FuncDef`, `Assign`, `For`, `AugAssign`, `Return` statements | Exactly the statement constructors used by `solution.mpy`. |
| `semantic.k:26-29` | `Ops`, `Ints`, `OpList`, `NumList` | Audit-specific encodings for input cells; not translated Python values or bindings. |
| `semantic.k:38-40` | `invoke`, `exec(Stmts)`, `answer(Int)` | Task-specific control/result forms. |
| `semantic.k:42-43` | `noText`, `builder(Ops,Ints,Ops,Ints)` | Summary marker, not an expression string. |
| `semantic.k:87` | `aligned(Ops,Ints) [function,total]` | Shape predicate. |
| `semantic.k:95-97` | `parsed`; `parsePow`, `powCombine` functions | Power-pass helper forms. |
| `semantic.k:113-116` | `tokens`; `powerPass`, `powerNext`, `powerCons` functions | Power-pass reconstruction. |
| `semantic.k:127` | `parseMul` function | Multiplicative-pass helper. |
| `semantic.k:139-141` | `mulPass`, `mulNext`, `mulCons` functions | Multiplicative-pass reconstruction. |
| `semantic.k:151` | `addPass` function | Additive fold. |
| `semantic.k:158-160` | `pyEval`, `afterPower`, `afterMul` functions | Result-bearing evaluator summary. |
| `semantic.k:165` | `powNat` function | Natural exponentiation helper. |
| `verification.k:8` | `solutionProgram [function]` | Exact source-term macro. |
| `verification.k:30` | `expected [function]` | Alias to the result-bearing `pyEval` symbol. |
| `verification.k:35` | `check(Int)`, `checked(Int)` | Ground-claim harness. |
| `verification.k:38,42,55` | `validOps`, `validOperator`, `nonNegative`, all `[function,total]` | Preconditions. |

The configuration has only `<k>`, `<operators>`, `<operands>`, and
`<expression>`. There is no environment/binding cell, value domain for lists
or strings, function/call stack, return frame, exception state, allocation, or
observable error cell. No local declaration or rule uses `[functional]`,
`[simplification]`, `[concrete]`, `priority`, or `owise`; there are no explicit
opaque declarations. Partial helper functions can leave unreduced terms on
uncovered inputs.

The submitted constructor inventory maps mechanically to syntax:

```text
Module -> Pgm
FuncDef/Assign/For/AugAssign/Return -> Stmt
Params -> Params
Name/Int/Call/Subscript/Slice/TupleExpr/BinOp -> Expr/Bound
```

Parsing coverage therefore passes. Execution coverage does not.

### Operational rules (`semantic.k:53-84`)

1. **Line 53, module dispatch.** It recognizes the exact function name and
   parameters and changes `Module(FuncDef(...,BODY)) ~> invoke` to
   `exec(BODY)`. This is a task-specific invocation convention but preserves
   the body.

2. **Lines 56-62, assignment bridge.** It matches the exact assignment AST
   but never evaluates the operand lookup or `str`. Instead it reads the
   separate input cells and writes
   `builder(OS,all operands,OS,remaining operands)`. It ignores every possible
   lookup, conversion, binding, and exception effect. This is an operational
   bridge, not a semantics rule for `Assign`, `Name`, `Subscript`, `Int`, or
   `Call`.

3. **Lines 64-80, loop bridge.** It matches the complete submitted `For` AST
   and, if only the raw list shapes align, changes the summary's remaining
   lists directly to empty. It does not execute slicing, `zip`, iteration,
   tuple assignment, local-name lookups, operator-string concatenation,
   operand conversion, or `AugAssign`. The rule has no bridge-free connection
   theorem. Its state footprint is the `<expression>` summary only; all source
   local binding and exception state is absent.

4. **Lines 82-84, return/eval bridge.** It matches the submitted return and
   rewrites directly to `answer(pyEval(ALLOPS,ALLINTS))`. It does not evaluate
   the constructed string or model Python `eval`, normal return, or exceptions.
   Its `_REST` discards remaining internal statements, as a return should, but
   there is no call frame whose unwind is validated. Most importantly,
   `verification.k:31` defines the target `expected` by exactly the same
   `pyEval` symbol.

These three result-relevant bridges have no fixed-semantics execution beneath
them: removing them leaves no rules at all for the used Python operations.
Therefore no independent universal connection theorem can be constructed from
this definition.

**Concrete false-conclusion witness for the assignment/return bridges.**
`operator=["+"]`, `operand=[10**4300,0]` satisfies `aligned`, `validOps`,
`nonNegative`, and the prompt's minimum sizes. Under the audited Python 3.10.12
environment, `sys.int_info.default_max_str_digits` is 4300. Both trusted and
candidate Python raise `ValueError` at `str(operand[0])`. Fresh K execution
exits 0 and contains `answer(10**4300)`. The bridge has fabricated a normal
result after skipping a real exceptional operation. The bounded evidence is
[large_integer_witness.sh](/audit-output/evidence/large_integer_witness.sh) and
[stage5-large-integer-witness.log](/audit-output/evidence/stage5-large-integer-witness.log).

**Small exception/control witness.** For `operator=["//"]`,
`operand=[1,0]`, both Python implementations raise `ZeroDivisionError`, and
fresh concrete K cannot reduce `parseMul`. Nevertheless, the exact ground
entry claim to
`answer(expected(Op("//",.Ops),Num(1,Num(0,.Ints))))` prints `#Top`, because
the return bridge and postcondition expose the identical unreduced summary
term. See
[audit-divzero-summary-spec.k](/audit-output/evidence/audit-divzero-summary-spec.k)
and
[stage5-divzero-summary-proof.log](/audit-output/evidence/stage5-divzero-summary-proof.log).

### Mathematical helper rules (`semantic.k:87-168`)

Every rule is enumerated below.

| Lines | Rules | Static result |
|---|---|---|
| 88–91 | Four `aligned` cases: empty/empty true, cons/cons recursion, and the two mismatched cases false | Disjoint, exhaustive over `Ops × Ints`, structurally descending, and truthful. `[total]` is justified. |
| 99 | `parsePow(.Ops, Num(I,.Ints))` | Correct terminal case on aligned input. |
| 100–101 | leading `**` recurses and later combines | Consumes an operator/operand pair and implements right association. |
| 102–109 | four stop rules for `+`, `-`, `*`, `//` | Disjoint and correct delimiters on valid operators. |
| 110–111 | `powCombine(I,parsed(J,...))` uses `powNat(I,J)` | Correct on the reachable non-negative exponent domain. |
| 118 | `powerPass -> powerNext(parsePow(...))` | Administrative composition. |
| 119–120 | terminal `powerNext` | Rebuilds the singleton reduced stream. |
| 121–122 | nonterminal `powerNext` | Preserves the delimiter and recursively processes its tail. |
| 123–124 | `powerCons` | Reconstructs one reduced value/operator pair. |
| 128 | terminal `parseMul` | Correct terminal case on the power-reduced aligned stream. |
| 129–130 | multiplication fold | Correct left-associative integer multiplication. |
| 131–133 | division fold guarded by nonzero divisor | Correct for the reachable non-negative integer operands; zero leaves the function undefined rather than modeling Python's exception. |
| 134–137 | stop at `+` or `-` | Correct multiplicative delimiters. |
| 142 | `mulPass -> mulNext(parseMul(...))` | Administrative composition. |
| 143–144 | terminal `mulNext` | Correct singleton stream. |
| 145–146 | nonterminal `mulNext` | Preserves the additive delimiter and recurses on its tail. |
| 147–148 | `mulCons` | Reconstructs one reduced group. |
| 152 | terminal `addPass` | Correct terminal value. |
| 153–154 | addition fold | Correct and structurally descending. |
| 155–156 | subtraction fold | Correct left-associative subtraction. |
| 161 | `pyEval -> afterPower(powerPass(...))` | Defines the result summary; it is not a source-execution connection. |
| 162 | `afterPower -> afterMul(mulPass(...))` | Correct phase composition. |
| 163 | `afterMul -> addPass(...)` | Correct phase composition. |
| 166 | `powNat(_,0) -> 1` | Correct, including `0**0` as Python evaluates it. |
| 167–168 | positive exponent recursion | Correct and numerically descending when `E>0`; negative exponents remain outside this helper's defined domain. |

I found no false arithmetic equation on the intended normal-return,
non-negative operand paths. The non-`[total]` helpers are partial, with
disjoint concrete operator cases. The problem is not that these recursive
equations calculate the displayed small examples incorrectly; it is that
their value is installed as the program result without executing or connecting
the property-bearing source operations.

### Verification rules (`verification.k:8-58`)

All 13 rules are:

| Lines | Rule(s) | Classification and result |
|---|---|---|
| 9–24 | `solutionProgram => Module(FuncDef(...))` | Definitional macro; constructor-equal to `solution.mpy`. Truthful. |
| 31 | `expected(OS,IS) => pyEval(OS,IS)` | Definitional alias, but circular as the independent postcondition because the operational return rule produces the same symbol. |
| 36 | `check(I) => checked(I)` | Ordinary ground-proof harness. It does not itself assert a result. |
| 39 | `validOps(.Ops) => true` | Correct base case. |
| 40 | recursive `validOps` | Correct and descending. |
| 43–47 | five accepted `validOperator` literals | Correct and pairwise disjoint. |
| 48–53 | guarded fallback `validOperator(O) => false` | Guard excludes every accepted literal, so it is disjoint and completes the String domain. |
| 56 | `nonNegative(.Ints) => true` | Correct base case. |
| 57–58 | recursive `nonNegative` | Correct and descending. |

The declared `[total]` verification functions (`validOps`, `validOperator`,
`nonNegative`) have exhaustive, consistent equations. `solutionProgram` and
`expected` each have one equation covering their nullary or constructor
signature. There are no proof-local lemmas, simplifications, priority rules,
or opaque symbols.

### Claims (`spec.k`)

The first claim is the universal entry theorem analyzed above. The other five
are ground evaluator examples. They correctly constrain those five values but
are finite tests expressed as reachability claims. They cannot supply the
missing universal source-to-summary connection.

### Result-bearing abstraction and opposite interpretation

The complete dependence is:

```text
exact Return(eval(expression))
    -- semantic.k:82-84 -->
answer(pyEval(raw operator cell, raw operand cell))

entry postcondition
    -- verification.k:31 -->
answer(pyEval(the same raw operator/operand terms))
```

There is no independently modeled `eval` execution between these nodes.

For the required opposite-interpretation check, I changed only
`semantic.k:161` from the candidate evaluator entry to the deliberately false
equation `pyEval(_OS,_IS) => 0`, rebuilt from source, and selected the unchanged
universal entry claim. It still printed `#Top`. Concrete mutated K returned 0
on the prompt case while trusted Python returned 9. See
[oracle-mutation.patch](/audit-output/evidence/oracle-mutation.patch),
[stage5-oracle-mutation-build.log](/audit-output/evidence/stage5-oracle-mutation-build.log),
[stage5-oracle-mutation-proof.log](/audit-output/evidence/stage5-oracle-mutation-proof.log),
and
[stage5-oracle-mutation-witness.log](/audit-output/evidence/stage5-oracle-mutation-witness.log).

This mutation does not claim that the candidate's actual recursive arithmetic
equations equal zero. It is a value-sensitivity witness showing that the entry
proof does not establish those equations' connection to program execution:
execution and specification move together under the wrong interpretation.

Stage 5 result: **FAIL**. The generated semantics contains unjustified,
result-bearing operational bridges and is concretely false over the declared
source domain.

## 6. Fresh non-vacuity test

The candidate's `mutation-spec.k` was inspected only as untrusted evidence. I
created a distinct mutation,
[audit-vacuity.k](/audit-output/evidence/audit-vacuity.k), on the satisfying
minimum-shape input:

```text
operator = ["-"]
operand  = [0, 1]
false target = answer(0)
actual result = -1
```

The mutation changes the result-constraining obligation, not the program term.
Its `kprove --dry-run` exited 0, establishing successful parse/build against
the clean proof definition. The real proof exited 1 with
`WarnStuckClaimState`; the residual visibly contains `answer(-1)` against the
false `answer(0)` target. This is the expected unmet obligation, not a parser
error, timeout, or unrelated crash.

Evidence:
[stage6-vacuity-dry-run.log](/audit-output/evidence/stage6-vacuity-dry-run.log)
and
[stage6-vacuity-proof.log](/audit-output/evidence/stage6-vacuity-proof.log).

Stage 6 result: **PASS** for ground result non-vacuity. This does not cure the
source-execution soundness failure.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the candidate-generated K theory, for constructor lists satisfying its
shape, operator, and non-negativity predicates, the exact submitted
`Module(FuncDef(...)) ~> invoke` term reaches
`answer(pyEval(OS,IS))`. It also establishes five ground calculations of the
candidate's recursive `pyEval` equations.

Operationally, this theorem closes because:

1. the exact assignment AST is replaced by a `builder` summary copied from
   external input cells;
2. the exact loop AST marks that summary consumed without iterating;
3. the exact return AST emits `pyEval` directly;
4. the target's `expected` rewrites to the same `pyEval`.

That is a proof about the candidate's task-specific abstraction, not a
partial-correctness proof of real Python execution.

### Trust ledger

| Boundary | Effect | Assessment |
|---|---|---|
| K 7.1.293 compiler, Haskell/LLVM backends, and built-in `INT`, `STRING`, `BOOL` equations | Parsing, rewriting, integer arithmetic | Ordinary low-level toolchain trust; acceptable. |
| Trusted `py2mpy.py` | Source-to-constructor syntax | Byte-regenerated and mechanically compared; acceptable. |
| External `<operators>` and `<operands>` cells as function arguments | Supplies raw inputs without an environment/call semantics | A possible invocation abstraction, but no binding theorem is given. Concerning alone; material when combined with skipped execution. |
| Assignment bridge (`semantic.k:56-62`) | Replaces lookup, indexing, and `str` | Illegitimate. No connection theorem; concrete 4301-digit `ValueError` witness. |
| Loop bridge (`semantic.k:64-80`) | Replaces slice, `zip`, iteration, bindings, concatenation | Illegitimate. No underlying rules or universal connection theorem. |
| Return bridge (`semantic.k:82-84`) | Replaces `eval`, exceptions, and return with `pyEval` | Illegitimate and circular with `expected`; division-zero and opposite-interpretation witnesses. |
| Recursive `pyEval` helper equations | Idealized integer precedence evaluator | Static mathematics and finite concrete tests support ordinary normal values, but they are not a bridge-free theorem about the source execution. |
| Python differential test | Candidate source vs trusted canonical on 13,889 cases | Strong finite implementation evidence only; it does not validate K semantics universally. |
| Fresh K concrete cases | Candidate K arithmetic vs Python on five normal cases | Finite evidence only; the large/exception witnesses expose the language-model gap. |
| Fresh false-result mutation | Shows a ground wrong result is rejected | Confirms local result discrimination after accepting `pyEval`; not source-to-summary soundness. |

### Gate accounting

- Gate A, real-program soundness: **FAIL**. Program-defined material operations
  are skipped, the result abstraction is circular, and concrete intended-domain
  witnesses disagree with source execution.
- Gate B, intent adequacy: **FAIL**. The semantics has no exception behavior
  and cannot represent the full stated non-negative-integer domain faithfully.
  Treating it as an idealized normal-only domain would materially narrow the
  HumanEval source contract and therefore maps to `FAIL / NOT_LEGIT`, not a
  concern.
- Gate C, trust and evidence: **PASS as an audit record**. The reconstructed
  commands, finite tests, mutations, and limits are preserved. This cannot
  override Gates A and B.

### Decision

The candidate has real source fidelity, real `#Top` outputs, exact AST pinning,
and a discriminating ground postcondition. It fails the decisive semantic
soundness requirement: the proof obtains its universal result by bypassing
the real property-bearing execution and sharing a result summary between the
operational rule and postcondition. The required verdict is therefore
`FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
