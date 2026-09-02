# Independent adversarial audit: 63-fibfib

The candidate contains a legitimate partial-correctness proof of the submitted
generated program. I independently rebuilt the generated language definition,
executed the submitted MPY program, reconstructed both reachability claims, tied
the entry claim's macro to the submitted MPY AST, reviewed every local rule, and
rejected a fresh false result obligation. No candidate-built definition, cache,
trace, prose conclusion, or prior `#Top` was used as proof evidence.

## 1. Input and provenance integrity

### Semantics boundary

The rendered mode is `GENERATED_SEMANTICS`, and
`/reference/reference-semantics` does not exist. This is the required mount
state. I did not search for or infer a hidden reference semantics. The
candidate's own `semantic.k` and `verification.k` are audited below.

### Required artifacts and trusted identity

All of the following candidate artifacts are regular, non-symlink files:

- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`;
- `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`;
- `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`.

There are no missing or mistyped required source artifacts and no candidate
source symlinks. The candidate prompt is byte-identical to
`/reference/prompt.py`, and the candidate translator is byte-identical to
`/reference/py2mpy.py`:

- prompt SHA-256:
  `3f6b45cdf3c576835537ba1cce2414a28f96b7a82157533ba221807ea2aa6147`;
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

`run-input.json` names `63-fibfib`, condition `bare`, and records those same
trusted hashes. Its `semantics: false` field is consistent with “no supplied
semantics,” hence with the rendered generated-semantics mode.

The top-level extra directories are `__pycache__/`, `codex-trace/`, and
`semantic-kompiled/`. The first and third are generated caches/build products;
the structured trace is required untrusted generation evidence. None is a
source dependency. I excluded the candidate's entire `semantic-kompiled/` tree
from reconstruction. There are no extra candidate K helper source files.

The structured trace has one JSONL file, 181 valid JSON records, and no malformed
line. `metrics.json`, `codex-last.txt`, `codex-output.log`, and the trace claim
that generation exited 0 and that the original proof printed `#Top`. I treated
all of those statements solely as untrusted historical claims.

Evidence:

- `evidence/stage1_integrity.sh`
- `evidence/stage1_integrity.log`
- `evidence/scratch_copy.log`

Stage 1 result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt defines the nonnegative FibFib sequence:

- `F(0)=0`;
- `F(1)=0`;
- `F(2)=1`;
- for `n>=3`, `F(n)=F(n-1)+F(n-2)+F(n-3)`;
- compute the `n`th element efficiently.

The trusted canonical implementation is the direct recursive realization of
those equations. The intended domain is nonnegative integers: the three base
cases and “nth sequence element” establish that domain, the formal claim uses
`N>=0`, and the canonical implementation does not terminate on negative input.

The submitted `solution.py` maintains `(a,b,c)=(F(i),F(i+1),F(i+2))`, initially
`(0,0,1)`. Each loop iteration simultaneously changes that triple to
`(b,c,a+b+c)` and increments `i`; after `n` iterations it returns `a`. This is
`O(n)` time and `O(1)` auxiliary space.

### Trusted regeneration

Running the trusted translator from the scratch copy regenerated
`solution.mpy` byte-for-byte. Both files have SHA-256
`4ae5eadda2bc9e05737c549a4ae38413d20a0bd9a520a71bf1100855124657f0`;
`cmp` and `diff` both exited 0.

### Independent differential test

`evidence/differential_test.py` imports the trusted canonical entry point and
the submitted generated entry point independently. It covers:

- documented examples `1,5,8`;
- the zero-iteration/empty case `0`;
- every canonical and loop branch frontier `0,1,2,3,4`;
- the dense prefix `0..15`;
- 20 generated values in `0..20` using seed `630063`;
- representative larger values `18,20,22`.

After de-duplication, all 21 tested values matched. Representative results were
`F(0)=0`, `F(2)=1`, `F(5)=4`, `F(8)=24`, `F(20)=35890`, and
`F(22)=121415`. There were zero mismatches and exit status was 0.

Evidence:

- `evidence/stage2_fidelity.sh`
- `evidence/stage2_fidelity.log`
- `evidence/differential_test.py`

Stage 2 result: **PASS**.

## 3. Clean proof reconstruction

### Isolation and builds

I copied only candidate source artifacts to `/tmp/audit-work/rebuild`; no
candidate-compiled definition or cache was copied. The live K toolchain is
version `v7.1.293`.

Two fresh definitions were built:

| Purpose | Exact command | Result |
|---|---|---|
| Concrete LLVM semantics | `kompile --backend llvm semantic.k --main-module FIBFIB --syntax-module FIBFIB-SYNTAX --output-definition concrete-kompiled` | exit 0 |
| Haskell proof semantics | `kompile --backend haskell semantic.k --main-module FIBFIB --syntax-module FIBFIB-SYNTAX --output-definition proof-kompiled` | exit 0 |

The generated semantics deliberately requires and imports `verification.k`, so
both fresh definitions contain its macros and mathematical specification
function. As established in Stage 5, none of those symbols occurs in or
rewrites the concrete submitted MPY execution.

### Positive proof claims

The unchanged all-claims command was:

`kprove spec.k --definition proof-kompiled --spec-module FIBFIB-SPEC`

It printed exactly `#Top` and exited 0. This reconstructs the candidate's actual
two-claim proof set independently.

I also separated the claims:

- `--claims FIBFIB-SPEC.loop-invariant` printed `#Top` and exited 0.
- After that helper was independently established, targeting
  `program-correct` with both claims retained and
  `--trusted FIBFIB-SPEC.loop-invariant` printed `#Top` and exited 0.

The `--trusted` use is only modular proof staging: the same loop claim was
proved in the immediately preceding independent command, and the unchanged
all-claims command proves the complete set without adding a trusted label.

As a diagnostic, filtering to `program-correct` alone also filtered out its loop
circularity, so the prover unrolled the unbounded symbolic loop. I interrupted
that diagnostic after 60 seconds (exit 130). It is not a positive proof command
and is not treated as a candidate failure. The successful unchanged all-claims
run and the separately proved-helper run are the relevant results.

### Fresh concrete execution

The LLVM definition executed the actual submitted `solution.mpy` at
`N=0,1,2,3,5,8,10,15,20`. Every `krun` exited 0 with empty `<k>`. Every result
matched both the trusted canonical Python and submitted Python implementations;
there were zero mismatches.

Evidence:

- `evidence/stage3_llvm_build.log`
- `evidence/stage3_haskell_build.log`
- `evidence/stage3_kprove_all.log`
- `evidence/stage3_kprove_loop_invariant.log`
- `evidence/stage3_kprove_program_with_proven_helper.log`
- `evidence/stage3_filtered_entry_diagnostic.txt`
- `evidence/k_concrete_compare.py`
- `evidence/stage3_concrete_compare.log`

Stage 3 result: **PASS**.

## 4. Adequacy and real-program pinning

### Plain-language claims

`program-correct` starts with:

- the complete `fibfibProgram` AST followed by `invoke(N)`;
- an empty environment and result cell `0`;
- precondition `N>=0`.

It requires termination with empty computation, result `F(N)`, and the exact
final environment:

- `a=F(N)`;
- `b=F(N+1)`;
- `c=F(N+2)`;
- `i=N`;
- `n=N`.

Thus the returned value is fixed; it is not a fresh variable, tautology, or
one-way implication.

`loop-invariant` starts at the real while-loop control point followed by the
actual terminal `Return(Name("a"))`, empty statement tail, and `finish`.
Its precondition is `0<=I<=N`, with
`a=F(I), b=F(I+1), c=F(I+2), i=I, n=N`. It requires the same exact final
environment as the entry claim and fixes the result to `F(N)`. This is the
control point produced by the concrete while rule after a true iteration; it
does not summarize a substituted loop or omit a continuation.

### Actual submitted-program identity

The proof writes the program as the `fibfibProgram` macro rather than reading a
file at proof time. I independently parsed and macro-expanded:

1. the trusted-regenerated submitted `solution.mpy`; and
2. the claim term `fibfibProgram`.

Their KORE files are byte-identical, both 3,146 bytes, with SHA-256
`c4a554fe1c9fdf9cf8e55a400ab532fc86e251d055391fe903aa7256cbd57652`.
Therefore the `<k>` claim executes the exact submitted AST.

### Satisfiable ground witnesses

For the entry claim, `N=5` satisfies `N>=0`. Its realizable initial state is
`fibfibProgram ~> invoke(5)`, empty map, result `0`; the claimed final state has
`a=4,b=7,c=13,i=5,n=5,result=4`.

For the loop claim, `I=2,N=5` satisfies `0<=I<=N`. A realizable invariant state
is `a=1,b=1,c=2,i=2,n=5`, with any starting result (the ground witness uses
123), followed by the exact loop/return continuation. It reaches
`a=4,b=7,c=13,i=5,n=5,result=4`.

The fresh two-claim ground spec printed `#Top` and exited 0. Substituting `N=5`
into the return obligation yields 4, and both Python implementations return 4.

Evidence:

- `evidence/stage4_pinning.sh`
- `evidence/stage4_pinning.log`
- `evidence/stage4_submitted_program.kore`
- `evidence/stage4_claim_program_macro.kore`
- `evidence/spec-ground.k`

Stage 4 result: **PASS**.

## 5. Rule-by-rule static soundness review

The complete source listing, Python AST inventory, and fully expanded local-rule
decision record are preserved in:

- `evidence/stage5_source_inventory.log`;
- `evidence/stage5_rule_inventory.md`.

### Syntax, cells, and construct coverage

The local AST syntax declares:

- `Module`, statement lists, `FuncDef`, `Assign`, `While`, `Return`;
- `Params` and string lists;
- `Name`, `Int`, `BinOp`, `Compare`, `TupleExpr`;
- expression and comparison-operator lists plus `CmpOp`.

The runtime syntax declares the twelve continuations `invoke`, `finish`,
`assignTo`, `binRhs`, `applyBin`, `compareRhs`, `applyCompare`,
`tupleSecond`, `tupleThird`, `tupleStore`, `whileDecision`, and `returnValue`.
`Int` and `Bool` are results. The configuration contains precisely computation,
environment map, and returned result.

Every submitted MPY construct maps to a declaration and operational rule:
module/function entry, ordered statements, integer/name evaluation, scalar
assignment, three-way tuple assignment, integer `+`, one-link integer `<`,
while, and terminal return. Missing translator constructs are unused and would
fail parsing or get stuck; no rule fabricates behavior for them.

There are no local opaque symbols, priority rules, `owise` rules,
simplification rules, `concrete` rules, or `functional` declarations. The
`symbol(name)` AST attributes are constructor labels, not opaque values.

### All 23 operational rules

| Rules | Decision |
|---|---|
| O1 | Matches the exact single `fibfib(n)` module and invocation, installs `n`, then executes the actual `BODY`; it does not supply a summary result. Sound entry-call model for this submitted program. |
| O2-O3 | Decompose a nonempty statement list into head then tail and consume the empty list. Sound sequential control. |
| O4-O5 | Evaluate integer literals and read initialized integer map bindings. Sound on all reachable program states. |
| O6-O8 | Evaluate binary operands left-to-right and apply `+Int` only for `"+"`. This is the only submitted binary operator; unsupported ones stop. |
| O9-O11 | Evaluate a single comparison left-to-right and apply `<Int` only for `"<"`. This is exactly the submitted guard. |
| O12-O13 | Evaluate scalar RHS before updating the named map binding. Sound Python name assignment for the used integer values. |
| O14-O17 | Evaluate all three tuple RHS expressions left-to-right before any store, then update targets left-to-right. This preserves Python's simultaneous RHS evaluation and the alias-sensitive rotation `(a,b,c)=(b,c,a+b+c)`. |
| O18-O20 | Evaluate the while guard; on true execute body and reconstruct the identical while term; on false consume it. The reconstructed term is the loop claim's real circularity point. |
| O21-O23 | Evaluate the return expression and consume only the exact terminal empty-list/`finish` continuations while updating `<result>`. The two terminal forms have non-unifiable left sides and identical effects; neither accepts or discards an arbitrary suffix. |

The rules preserve the complete state footprint. The program uses no heap,
allocation, I/O, exception, closure, nested call, or other observable state.
Evaluation order, map changes, loop control, and the return continuation are all
explicit. No operational bridge preempts or skips the property-bearing tuple
update or loop.

### All six verification rules and attributes

| Rule | Decision |
|---|---|
| V1 `loopCondition` | Macro-expands to the exact submitted `i<n` AST. |
| V2 `loopBody` | Macro-expands to the exact tuple update followed by `i=i+1`. |
| V3 `fibfibProgram` | Macro-expands to the full submitted AST; byte-identical expanded KORE is recorded in Stage 4. |
| V4 | `fibfibMath(N)=0` for `N<=1`. |
| V5 | `fibfibMath(2)=1`. |
| V6 | For `N>=3`, the exact three-predecessor recurrence. |

`fibfibMath` is declared `[function,total]`. V4-V6 give disjoint, exhaustive
integer guards `N<=1`, `N=2`, and `N>=3`; V6 strictly descends. Its negative
extension is not connected to either theorem because both claim domains are
nonnegative. On the formal domain, it is exactly the prompt's recurrence.
Therefore this is a truthful definitional specification function, not an
unconstrained oracle. It never replaces execution of the submitted program.

`semantic.k` imports this verification module, but the concrete submitted term
contains none of `fibfibProgram`, `loopCondition`, `loopBody`, or
`fibfibMath`; the first three are compile-time macros and the last rewrites only
explicit `fibfibMath` terms in specifications. This import cannot bypass
concrete program execution.

### Overlap, sensitivity, and unsoundness decision

The guarded `fibfibMath` rules do not overlap. The ordinary rules are
front-term distinct on reachable configurations. The return variants are
distinct exact continuations. Map updates, comparisons, and arithmetic defer to
standard K built-ins.

As an operational/body-sensitivity test, I changed only the terminal source
return from `a` to `b`, translated it with the trusted translator, and ran it
under the fresh concrete definition at `N=5`. K returned 7 instead of the
original 4, and the mutated expanded AST no longer matched the claim macro
(`cmp` exit 1). Thus both execution and real-program pinning are sensitive to a
material body change.

I found no unsound local rule on the intended domain. Consequently there is no
claimed unsoundness requiring a false-conclusion witness. In particular, no
answer-encoding rule, execution bypass, result oracle, uncontrolled return, or
fabricated used construct is present.

Evidence:

- `evidence/stage5_rule_inventory.md`
- `evidence/stage5_source_inventory.log`
- `evidence/stage5_body_sensitivity.sh`
- `evidence/stage5_body_sensitivity.log`
- `evidence/stage5_solution_return_b.py`
- `evidence/stage5_solution_return_b.mpy`

Stage 5 result: **PASS**.

## 6. Fresh non-vacuity test

I created a new scratch spec that changes the entry result from
`fibfibMath(N)` to the false obligation `fibfibMath(N)+1`, while leaving the
real environment postcondition and loop helper intact.

The mutation first built successfully:

`kprove spec-vacuity-audit.k --definition proof-kompiled --spec-module FIBFIB-SPEC-VACUITY-AUDIT --dry-run`

It exited 0 and emitted a valid `kore-exec` proof command. The actual proof
command then exited 1 with `WarnStuckClaimState` at the mutated entry claim. The
residual is the expected unmet implication:

`fibfibMath(N) +Int 1 #Equals fibfibMath(N)`.

This is not a parser error, missing import, timeout, or unrelated crash. The
claim reached empty `<k>`, the correct final environment, and actual result
`fibfibMath(N)` before failing only the changed result constraint.

`N=5` is a satisfying witness: the precondition holds, both Python
implementations return 4, and the mutation demands 5.

Evidence:

- `evidence/spec-vacuity-audit.k`
- `evidence/stage6_nonvacuity.sh`
- `evidence/stage6_nonvacuity.log`

Stage 6 result: **PASS**.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the audited generated semantics and standard K mathematical primitives:
for every mathematical integer `N>=0`, if execution of the exact submitted MPY
program reaches termination from its configured empty environment, then it ends
with empty computation, returns the recurrence-defined FibFib value `F(N)`, and
has `a=F(N), b=F(N+1), c=F(N+2), i=N, n=N`.

The loop claim establishes the corresponding execution fact from every
invariant state `0<=I<=N`. The proof is a partial-correctness proof; it does not
claim a separate K termination theorem.

### Trust ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K compiler, Haskell prover, LLVM runtime, and reachability calculus | All machine-checking and execution evidence | Standard unavoidable toolchain trust; fresh builds and independent runs reduce cache/provenance risk. |
| Imported K `INT`, `BOOL`, `MAP`, and generated list/parser machinery | Arithmetic, comparison, bindings, syntax lists | Acceptable low-level primitives. Their used operations have standard meanings and no task-specific result axiom. |
| Trusted `/reference/py2mpy.py` | Source-to-MPY syntax bridge | Explicit trusted input. Its output is byte-identical to submitted MPY, and used constructors were mapped exhaustively. |
| Generated semantics versus the used Python subset | Meaning of assignment, tuple evaluation, loop, and return | Audited rule-by-rule rather than assumed wholesale; elementary rules match Python order/control, are body-sensitive, and agree with both Python programs on boundary and normal runs. No opaque result bridge remains. |
| `fibfibMath` equations | Formal postcondition and invariant | Definitional mathematical specification, exhaustive and disjoint. It does not execute in place of program code. |
| Prompt/canonical recurrence bridge | Natural-language intent | The formal equations reproduce the prompt and canonical base/recurrence clauses verbatim in mathematical form. The finite differential run supports implementation alignment but is not treated as a universal proof substitute. |
| `fibfibProgram` macro-to-file equality | Real-program pinning | Independently established by trusted regeneration and byte-identical expanded KORE. A body mutation breaks the equality and changes execution. |

There are no opaque symbols, externally supplied result functions, empirical
oracles, unchecked operational bridges, proof-specific simplification axioms,
or unproved auxiliary reachability claims. Differential testing supports only
the executable bridges it sampled; the universal program result comes from the
K loop/entry proof plus the exact recurrence definition.

### Gate decisions

- Real-program soundness: **PASS**. Actual bodies execute; state/control are
  preserved; the proof is body-sensitive and result-constraining; non-vacuity
  succeeds.
- Intent adequacy: **PASS**. Domain, base cases, recurrence, implementation,
  translated AST, and formal result align.
- Trust and evidence auditability: **PASS**. All commands, exit statuses,
  bounded outputs, scripts, mutations, and finite input scopes are preserved
  and correctly classified.

The proof is therefore sound, pins the real generated program, and has no
material adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
