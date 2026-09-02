# Independent adversarial review: 62-derivative

## Executive decision

The candidate contains a freshly reproducible, non-vacuous reachability proof
of the exact translated program **for the generated semantics' executable
integer-list fragment**. The program macro is mechanically identical to
`solution.mpy`; all claims close from fresh source builds; the mathematical
summary is connected to actual helper execution; changing the executed helper
body invalidates the proof; and a false postcondition is rejected.

It is not a proof over the material source-contract domain. The trusted prompt
declares only `xs: list` and describes polynomial coefficients without an
integer-only condition. Both trusted and generated Python execute successfully
on non-integer numeric coefficients. For example, both return
`[1.5, -4.0]` on `[0.0, 1.5, -2.0]`. The K runtime has no `FloatV`, and even a
representable boolean-coefficient list gets stuck at
`#bin("*", IntV(1), BoolV(true))` although Python returns `[1, 0, 3]`.
Consequently, the formal theorem has a normal, intended derivative result only
for `IntV` coefficients. For other admitted `Value` terms,
`#differentiate` may merely expose an unreduced `#bin` inside the destination.

That is a materially narrowed HumanEval source-contract domain. The benchmark
prompt expressly maps such a Kit `SOUND-BUT-LIMITED` result to a failed,
non-legitimate candidate rather than to a legitimate concern.

## 1. Input and provenance integrity

The declared layout is `legacy-selected-stage1`, the condition is `bare`, and
the rendered mode is `GENERATED_SEMANTICS`
(`/audit-input.json`). The mounted campaign lock is structurally identical to
the `audit_campaign` object and its SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.

I read the required launcher records:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- all 255 JSONL records in the sole structured trace under
  `/generation-evidence/codex-trace/`.

The optional `usage.json` is present and reports `COMPLETE`.
`runtime-metrics.json` is absent, as permitted for this historical
`legacy-selected-stage1` layout; it was not reconstructed. The extra imported
`legacy-run-input.json` and `legacy-metrics.json` were also inspected.
Generation records report a successful prior run, but none was treated as
proof evidence.

Independent checks found:

- every launcher-recorded ordinary file hash matches its mounted file;
- the trace file hash
  `45242a53099a23f0602aec57820eed116861b2b94545d69f76f22d3ba2759ff0`
  matches both invocation and result manifests;
- an independent implementation of the pipeline tree digest gives
  `e75e096e49fc8c0f8830d30638f6d40a71e28e8e9c891b104fccf5f98641b9d9`
  for `/candidate`, matching both retained-workspace manifest fields;
- the corresponding trace tree digest is
  `7dbed00a38175b843cc20eb9bc0c80f1b06ff9297c1a594678ac0998aa8fd80b`,
  matching `usage.json`;
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
- `/candidate/py2mpy.py` is byte-identical to
  `/reference/py2mpy.py`;
- all required candidate artifacts are regular files, and there are no
  symlinks in candidate, trusted-reference, or generation-evidence trees.

The generated-semantics boundary is intact:
`/reference/reference-semantics` does not exist, and the corresponding trusted
and candidate reference-semantics hash fields are null. I did not seek or infer
a hidden baseline.

Evidence:
[provenance checker](evidence/01_provenance.py),
[provenance log](evidence/01_provenance.log),
[generation-record reader](evidence/01_generation_records.py), and
[generation-record log](evidence/01_generation_records.log).
There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

`/reference/prompt.py:3-10` says that `xs` is a list of coefficients for

`xs[0] + xs[1] * x + xs[2] * x^2 + ...`

and requires the derivative coefficients in the same representation. Thus a
normally returning result is

`[1 * xs[1], 2 * xs[2], ..., (len(xs)-1) * xs[-1]]`.

The empty and singleton results are empty. The examples require
`[3,1,2,4,5] -> [1,4,12,20]` and `[1,2,3] -> [2,6]`.
The prompt gives no coefficient subtype and no length bound.

The trusted canonical at `/reference/canonical.py:7-16` implements that
formula with `enumerate(xs)` and slicing. The candidate
`/candidate/solution.py:1-9` discards the constant coefficient and uses a
structurally recursive helper carrying the current degree. The algorithms are
extensionally equal while the recursion completes.

### Translation identity and differential evidence

Running the trusted translator on the scratch copy of `solution.py` produced a
file byte-identical to submitted `solution.mpy` (both commands exit 0). The
independent differential script imports the trusted canonical and the
candidate by separate paths. It exercised:

- both documented examples;
- empty, singleton, and first recursive-step boundaries;
- all coefficient tuples over `{-2,0,3}` through length six;
- negatives, zeros, booleans, floats, and arbitrarily large integers;
- 1,000 deterministically generated lists of lengths 0 through 80.

All 2,102 safe-depth cases matched. This is finite evidence, not a universal
proof. On the unbounded length-1,500 input, the canonical returned 1,499
coefficients while the recursive candidate raised `RecursionError`. That is a
real implementation/source discrepancy and a generated-semantics resource
abstraction; it is not used as a substitute for the K proof. Because the task
asks for partial correctness, the primary rejection below is the value-domain
gap, not lack of a termination theorem.

Evidence:
[fidelity commands](evidence/02_fidelity.sh),
[differential program](evidence/02_differential.py), and
[fidelity log](evidence/02_fidelity.log).

## 3. Clean proof reconstruction

I copied only source artifacts to
`/tmp/audit-work/reconstruction-62`; no candidate kompiled directory or cache
was copied. K version 7.1.293 was available. From source I built:

- an LLVM definition from `semantic.k`, with main module `MPY` and syntax
  module `MPY-SYNTAX`;
- a Haskell definition from `verification.k`, with main and syntax module
  `VERIFICATION`.

Fresh `krun` executions matched independent Python on seven integer-list cases:
empty, singleton, the first nonempty boundary, both examples, negative
coefficients, and very large integers. All executions exited 0.

The fresh positive proof results were:

| Target selection | Result | Exit |
|---|---:|---:|
| all claims in `SPEC` | `#Top` | 0 |
| `helper-correct` | `#Top` | 0 |
| `derivative-empty` | `#Top` | 0 |
| `helper-correct,derivative-nonempty` | `#Top` | 0 |

The last selection retains the nonempty claim's explicit helper dependency.
The KORE produced by parsing `solution.mpy` and expanding macros is byte-equal
to the KORE produced by expanding `solutionProgram`; `cmp` exits 0.

The authoritative clean transcript, including exact commands and all statuses,
is [03_reconstruct_clean.log](evidence/03_reconstruct_clean.log), generated by
[03_reconstruct_clean.sh](evidence/03_reconstruct_clean.sh).

For transparency, two superseded reviewer attempts remain in evidence.
`03_reconstruct.log` used an incorrectly double-escaped reviewer regex and
therefore failed to parse visibly correct `IntV` output. After that checker was
fixed, `03_reconstruct-rerun.log` obtained `#Top` for the combined, helper, and
empty targets but I interrupted an isolated nonempty selection that had omitted
its dependency. Neither is candidate evidence. The dependency-closed clean run
above supersedes both.

## 4. Adequacy and real-program pinning

### Claims in plain language

`helper-correct` (`/candidate/spec.k:9-19`) has no side condition. For every
finite K `Values` sequence `CS`, every mathematical integer `N`, and every
continuation `K`, calling the exact submitted `derivative_helper` closure on
`ListV(CS), IntV(N)` reaches
`ListV(#differentiate(N, CS))` and then preserves `K`.

`derivative-empty` (`/candidate/spec.k:23-30`) says that running the exact
program on `ListV(.Values)` reaches the empty runtime list.

`derivative-nonempty` (`/candidate/spec.k:32-40`) says that running the exact
program on any `ListV(C0, CS)` discards `C0` and reaches
`ListV(#differentiate(1, CS))`.

All preconditions are satisfiable. Concrete witnesses include:

- helper: `N=2`, `CS=(IntV(5),IntV(7),.Values)`, `K=.K`, whose integer result
  is `[10,21]`;
- empty entry: `[]`, whose result is `[]`;
- nonempty entry: `[3,1,2,4,5]`, whose result is `[1,4,12,20]`.

These results agree with both trusted and generated Python, as recorded in
Stages 2 and 3.

### Program identity

`solutionProgram` expands to the complete two-function constructor tree in
`/candidate/verification.k:13-33`. The constructor tree contains the exact
binding names, parameters, slice operations, branch, multiplication, recursive
call, and degree increment in submitted `solution.mpy`. The trusted
regeneration and fresh expanded-KORE comparison mechanically establish
identity. The translator's omission of Python annotations is typing-only and
is demonstrated by the trusted regeneration, rather than assumed.

The helper claim begins from a call against `solutionFuns`, the collection of
the exact function bodies, and executes the actual helper under `semantic.k`.
There is no rule replacing that call with `#differentiate`. The latter occurs
only as the destination summary.

A reviewer mutation changed the multiplication constructor in the actual
executed helper macro to addition. Its definition built successfully, but the
original multiplication summary failed with a
`WarnStuckClaimState` equality obligation between `#bin("+",...)` and
`#bin("*",...)`. Witness `N=2,C=5` gives 7 rather than 10. This confirms body
sensitivity:
[mutation source](evidence/verification-body-mutation.k),
[mutation claim](evidence/spec-body-mutation.k), and
[log](evidence/04_body_sensitivity.log).

### Adequacy defect

For integer coefficients, `#differentiate` is fully result-constraining:
`#bin("*",IntV(N),IntV(C))` reduces to `IntV(N *Int C)`.
For arbitrary `Value` coefficients admitted by the formal entry claim, the
summary can contain an unreduced `#bin`; the destination need not be a normal
Python result. Float coefficients cannot be represented at all.

[04_domain_gap.log](evidence/04_domain_gap.log) records:

- generated Python returns `[1,0,3]` on `[0,True,False,True]`;
- K concrete execution fails at
  `#bin("*",IntV(1),BoolV(true))`;
- generated Python returns `[1.5,-4.0]` on `[0.0,1.5,-2.0]`;
- parsing the corresponding runtime input fails because `FloatV` has no
  declaration.

The trusted canonical agrees with generated Python on these cases in Stage 2.
This is a material input/result-domain restriction, not merely a missing
unused language construct.

## 5. Rule-by-rule static soundness review

The exhaustive source listing and declaration index are in
[05_static_inventory.log](evidence/05_static_inventory.log). The only local K
files are `semantic.k`, `verification.k`, and `spec.k`.

### Syntax, configuration, attributes, and construct coverage

`MPY-SYNTAX` declares:

- `Module`, juxtaposed statement lists, `FuncDef`, `Return`, and `If`;
- parameter, string, expression, comparison-operator, and bound lists;
- `Int`, `Bool`, `Str`, `Name`, `ListExpr`, `BinOp`, `Compare`, `Call`, and
  `Subscript`;
- expression indices, `Slice`, and `NoBound`.

`MPY` declares `IntV`, `BoolV`, `StrV`, `ListV`, `NoneV`, finite `Values`,
closures, `#prepend`, execution terms, and the sole `<mpy><k>...</k></mpy>`
configuration. A bindings map and function map are passed explicitly inside
terms. No heap, allocation identity, output, exception, or mutable state cell
is present; none is observable in the submitted pure integer program.

Every constructor in `solution.mpy` is covered:

| Submitted constructor | Declaration and behavior |
|---|---|
| `Module`, `FuncDef`, `Params` | `semantic.k:6,10,14`; collection/binding at 78-89 |
| `Return`, `If` | declarations 11-12; execution 94-123 |
| `Int`, `Name`, `ListExpr`, `BinOp` | declarations 18,21-23; evaluation 126-132 |
| `Compare`, `CmpOp("==",...)` | declarations 24,28-29; used empty-list branches 110-119 |
| `Call` | declaration 25; call/argument rules 88-89,96-104,135-144 |
| index zero and slice `[1:]` | declarations 26,31-33; rules 137-140,163-165 |
| integer `+`, integer `*`, list `+` | rules 147-152 |

The local `[function]` declarations are `#run`, `#choose`, `#eval`, `#bin`,
`#equal`, `#head`, `#tail`, `#evalArgs`, `#concat`, `#collect`, `#bind`, and
proof-local `#differentiate`. There are three `[macro]` declarations. There
are no local `[total]`, `[functional]`, `[simplification]`, `[priority]`,
`[owise]`, `[trusted]`, or concrete-priority declarations; no opaque symbols;
and no local lemmas beyond the three reachability claims.

### All 41 semantic rules

| Lines | Inventoried rule(s) | Decision |
|---|---|---|
| 78 | `#run(Module(SS),ARG)` | Correctly selects global `derivative` and packages the single argument for this submitted module. Program-specific, not a general module semantics. |
| 80-82 | `#collect` empty/`FuncDef` step | Disjoint base and descent equations; they construct the two exact global closures. |
| 84-86 | `#bind` empty/cons step | Disjoint and descending; exact for the submitted arities. Mismatched arity stops visibly. |
| 88-89 | `#call` closure lookup | Uses the selected map binding, binds arguments, and retains the complete function map. No body bypass occurs. |
| 94-95 | return of `ListExpr` | Evaluates the returned list and correctly discards the post-return statement suffix. |
| 96-97 | return of direct named call | Evaluates actual arguments and executes the selected closure. Exact for `derivative`'s return. |
| 98-105 | return of list plus recursive call | Exposes the real recursive call and then prepends the evaluated singleton. This reverses the general Python operand schedule, but the submitted left operand is pure integer multiplication/subscript with no state or exception in the modeled domain; fixed and summarized results coincide there. It is not evidence for reuse as a general Python rule. |
| 106 | `#prepend` | Concatenates the already computed singleton to the recursive result and preserves the arbitrary continuation. |
| 110-114 | empty-list `If` | Exact constructor split for `xs == []`; the actual then branch returns. |
| 115-119 | nonempty-list `If` | Disjoint complement of the prior rule; the actual else branch returns. |
| 120 | empty statement execution | Correct implicit `NoneV` return. |
| 122 | `#choose(true,...)` | Selects the then branch. |
| 123 | `#choose(false,...)` | Selects the else branch; disjoint from line 122. |
| 126 | integer literal | Exact `Int` to `IntV`. |
| 127 | boolean literal | Exact `Bool` to `BoolV`. |
| 128 | string literal | Exact `Str` to `StrV`. |
| 129 | name lookup | Returns the exact map binding; no free oracle. |
| 130 | list literal | Evaluates all elements into a finite `ListV`. |
| 131-132 | binary-expression dispatch | Evaluates operands and dispatches to `#bin`; exact for the pure submitted operands. |
| 133-134 | equality dispatch | Evaluates both sides and calls `#equal`; used only for list versus empty list. |
| 135-136 | named call expression | Evaluates arguments and executes the bound global closure. |
| 137-138 | subscript zero | Evaluates the receiver and uses the nonempty `#head`; actual use is guarded by the nonempty branch. |
| 139-140 | slice `[1:]` | Evaluates the receiver and applies `#tail`, exactly the only slice used. |
| 142 | empty argument list | Correct base equation. |
| 143-144 | argument-list step | Structurally descending and exact for pure submitted arguments. |
| 147 | integer addition | K mathematical integer addition matches Python integer addition. |
| 148 | integer multiplication | K mathematical integer multiplication matches Python integer multiplication. |
| 149 | list addition | Dispatches to sequence concatenation. |
| 151 | empty-left concatenation | Mathematical sequence identity. |
| 152 | cons-left concatenation | Structurally descending and order-preserving. |
| 156 | integer equality | Correct same-type integer equality. |
| 157 | boolean equality | Correct same-type boolean equality. |
| 158 | string equality | Correct same-type string equality. |
| 159 | empty/empty list equality | Correct and used. |
| 160 | nonempty/empty list equality | Correct and disjoint. |
| 161 | empty/nonempty list equality | Correct and disjoint. Nonempty/nonempty equality is intentionally unmodeled and unused. |
| 163 | nonempty head | Returns the first value. |
| 164 | empty tail | Models `[][1:] == []`. |
| 165 | nonempty tail | Models `xs[1:]`; disjoint from line 164. |

The specialized `If` rules discard any following `REST`, and the specialized
list-plus-call rule is not a reusable full Python evaluation-order semantics.
In the actual constructor tree, both branches return, `REST` is empty, and the
left list element is pure. I therefore record the over-broad reuse limitation
but do not label these rules unsound for the submitted integer program: there
is no satisfying intended integer input on which they enable a false result.

### All five verification rules and three claims

| Lines | Extension | Classification and decision |
|---|---|---|
| `verification.k:13` | `solutionProgram` macro rule | Compile-time naming macro; expanded KORE is mechanically identical to submitted `solution.mpy`. |
| `verification.k:14` | `solutionFuns` macro rule | Names collection of the exact function list; no execution is skipped. |
| `verification.k:15-33` | `solutionFunctions` macro rule | Exact constructor tree. Body-sensitivity mutation confirms the theorem depends on its multiplication node. |
| `verification.k:41` | empty `#differentiate` | Definitional-summary base equation; mathematically true. |
| `verification.k:42-43` | nonempty `#differentiate` | Definitional-summary step; disjoint, structurally descending, and exact for `IntV` coefficients through semantic rule 148. Partial/stuck for other runtime values. |
| `spec.k:9-19` | `helper-correct` | Bridge-free execution/summary connection claim over the exact helper, map, arguments, continuation, and sole state cell. |
| `spec.k:23-30` | empty entry | Exact entry execution for the empty finite list. |
| `spec.k:32-40` | nonempty entry | Exact entry execution and helper dependency for a cons list. |

`#differentiate` is result-bearing but not an opaque oracle. Its exhaustive
empty/cons equations determine it, and `helper-correct` connects that summary
to fixed generated-semantics execution without an operational rewrite from
`#call` to the summary. The body mutation rejects an opposite implementation,
and the result mutation in Stage 6 rejects an opposite degree interpretation.

I make no rule-unsoundness finding, so there is no unsupported unsoundness
label requiring a false-conclusion witness. The decisive defect is adequacy:
the available value and multiplication rules do not cover the materially
broader source-contract inputs on which both Python implementations return.
The prose assertion at `/candidate/verification.k:37-38` that the residual
describes Python's nonnumeric stuck/error behavior is itself refuted by the
boolean witness in `04_domain_gap.log`, but that comment is not a K axiom.

## 6. Fresh non-vacuity test

The reviewer-authored
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k) leaves the actual
program unchanged and mutates the nonempty postcondition from
`#differentiate(1,CS)` to `#differentiate(2,CS)`. The precondition is
satisfiable. For ground input `[3,5]`, the program and original theorem return
`[5]`; the mutation demands `[10]`.

The exact results in [06_non_vacuity.log](evidence/06_non_vacuity.log) are:

- `kprove ... --dry-run`: exit 0, so the mutation parses and builds;
- live `kprove`: exit 1 with `WarnStuckClaimState`;
- the residual explicitly requires equality of
  `#bin("*",IntV(1),V)` and `#bin("*",IntV(2),V)`.

This is the expected unmet result obligation, not a parser error, missing
import, timeout, unrelated crash, or unreachable mutation. The wrapper exits 0
only after recognizing the expected proof failure.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the locally generated `MPY` theory:

1. the exact submitted constructor program loads its exact two closures;
2. for every finite K sequence `CS`, integer degree `N`, and continuation `K`,
   actual helper execution reaches the recursively defined
   `ListV(#differentiate(N,CS))` and preserves `K`;
3. the exact entry returns empty on an empty runtime list;
4. on a cons runtime list it discards the constant coefficient and reaches
   `ListV(#differentiate(1,CS))`;
5. when every member of `CS` is `IntV(C)`, that destination normalizes to the
   intended integer derivative coefficients.

It is a partial-correctness result. It does not prove CPython termination,
resource behavior, or the unrestricted prompt-level coefficient domain.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| K 7.1.293 parser, compiler, LLVM backend, Haskell backend, and reachability/circularity implementation | All builds and proof closure | Toolchain trust boundary; rebuilt from source artifacts and cross-checked with negative proofs. |
| Built-in `INT`, `BOOL`, `STRING`, `MAP`, K sequences, and cells | Values, arithmetic, bindings, control configuration | Standard low-level semantics trusted. Integer arithmetic is exact and appropriate for Python integers. |
| Trusted `py2mpy.py` | Source-to-constructor identity | Launcher hash and byte identity verified; submitted `.mpy` regenerated byte-identically. |
| Generated `semantic.k` | Entire Python-to-K meaning bridge | Not assumed wholesale: all local declarations/rules were inventoried and concrete integer executions were compared. It remains a program-specific fragment, not a complete Python semantics. |
| `solutionProgram`/`solutionFunctions`/`solutionFuns` | Real-program pinning | Compile-time macros, not opaque assumptions; expanded KORE equality and body mutation validate them. |
| `#differentiate` | Final result | Defined by terminating equations and connected to exact helper execution. No arbitrary interpretation remains for integer coefficients. |
| CPython/canonical differential tests | Implementation and semantic bridge on tested cases | Finite empirical evidence only; 2,102 Python comparisons and seven concrete K comparisons, with zero safe-fragment mismatches. |
| Unbounded K recursion versus CPython recursion limit | Termination/exception behavior | Informal resource abstraction. The length-1,500 divergence is recorded and excluded from the proved real-CPython behavior. |
| Missing numeric runtime values/operations | Final result on non-integer coefficients | Illegitimate as coverage of the full prompt domain. Floats are unrepresentable and representable booleans get stuck although both Python functions return. |

There are no candidate-declared trusted claims, opaque symbols, empirical
oracles embedded in rules, or proof rules that encode the task answer. The
differential and mutation evidence supports only the bridges stated above and
does not substitute for `kprove`.

### Gate accounting and decision

- Real-program soundness for the executable integer fragment: passes.
- Intent adequacy for the unrestricted prompt-level coefficient list: fails
  materially.
- Evidence auditability: passes; all reviewer scripts, exact commands,
  statuses, and bounded outputs are preserved under `/audit-output/evidence/`.

The integer-fragment theorem is honest partial progress, but the benchmark's
decision rule does not permit a materially narrowed source-contract theorem to
be reported as legitimate.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
