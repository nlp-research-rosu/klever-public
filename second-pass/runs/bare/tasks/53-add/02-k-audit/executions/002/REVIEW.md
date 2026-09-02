# Independent adversarial review: HumanEval 53-add

The candidate contains a legitimate proof of the generated program. I rebuilt
both execution and proof definitions from source, reproduced the one target
claim as `#Top`, mechanically pinned the claim to the trusted translation of
`solution.py`, reviewed every local K declaration and rule, and observed the
expected failures for separate body-sensitivity and false-postcondition
mutations. The formal domain is all K mathematical integers, which covers the
source contract's integer domain rather than a finite or bounded subset.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, condition `bare`, and `semantics_mode =
GENERATED_SEMANTICS`. I used its `container_paths`; I did not attempt to use its
host provenance paths.

The campaign object in `/audit-input.json` is structurally identical to
`/audit-campaign-lock.json`, whose independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
the declared value. The mounted run, task, stage result, invocation, metrics,
usage, generation prompt, last message, output log, trusted inputs, and every
file named by the stage result's evidence map are regular files and match their
recorded hashes. The sole structured trace is a valid 180-line JSONL file; its
file hash matches both the result and invocation records. The independently
reimplemented pipeline tree digest is
`5b06d62f4bc782c19b65b5f092889fe98bb4ec7024271f620164ca4fb34f051e`,
matching `usage.json`.

The candidate tree contains only regular files and real directories. Its
independent pipeline tree digest is
`9c33318a75c7541848b7803292fc4fcf6c41c8d455349a2bf93a966fb2f268e6`,
matching both the retained-workspace hash in `invocation.json` and the
workspace hash in `generation-result.json`. The evidence log also gives
independent SHA-256 values for every candidate file.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`. As required
for generated-semantics mode, neither `/reference/reference-semantics` nor
`/candidate/reference-semantics` exists. There is therefore no supplied or
hidden semantics baseline to compare. The absent historical
`runtime-metrics.json` is permitted by this legacy-selected layout and is not a
defect. The present `usage.json`, `legacy-metrics.json`, and
`legacy-run-input.json` were also parsed and hash-checked.

Evidence: [integrity script](/audit-output/evidence/stage1_integrity.py) and
[integrity log](/audit-output/evidence/stage1_integrity.log). The old generation
trace and its `KPROVE_PASSED` marker were inspected only as untrusted historical
claims and did not contribute to the verdict.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: for two integer arguments `x` and `y`, return
their sum. Its examples require `add(2, 3) == 5` and `add(5, 7) == 12`.
The trusted canonical implementation is `return x + y`
(`/reference/canonical.py:13`). The candidate implementation is the same
straight-line expression (`/candidate/solution.py:1-2`); it has no branches,
loops, mutation, exceptions on intended integer inputs, or meaningful empty
input case.

I copied the source artifacts to a fresh directory and ran:

```text
python3 /tmp/audit-work/53-add-audit-002/py2mpy.py /tmp/audit-work/53-add-audit-002/solution.py > /tmp/audit-work/53-add-audit-002/regenerated.solution.mpy
cmp /tmp/audit-work/53-add-audit-002/regenerated.solution.mpy /tmp/audit-work/53-add-audit-002/solution.mpy
```

The command exited 0, establishing byte identity with the submitted
`solution.mpy`. See
[solution_regeneration.log](/audit-output/evidence/solution_regeneration.log).

The independent differential script imports the trusted canonical and scratch
generated modules. It checked the two documented examples, zero and signed
boundaries, cancellation, values crossing a machine-word boundary,
arbitrary-precision values, a 9-by-9 grid, and 5,000 deterministic generated
pairs up to 1,024 bits. All 5,093 non-example pairs and both examples matched.
There are zero conditional branch boundaries to cover. See
[differential_test.py](/audit-output/evidence/differential_test.py) and
[differential_test.log](/audit-output/evidence/differential_test.log).

## 3. Clean proof reconstruction

I copied only the candidate's source files and the trusted inputs into the
previously unused `/tmp/audit-work/53-add-audit-002`. I did not copy or use
candidate-built definitions, caches, or `prove.sh`. K 7.1.293 was already
installed independently; `kup` was absent, which is allowed by the live Kit
path when the installed tools run
([tool versions](/audit-output/evidence/toolchain_versions.log),
[kup check](/audit-output/evidence/kup_presence.log)).

Fresh builds:

```text
kompile --backend llvm semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition concrete-kompiled
kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition proof-kompiled
```

Both exited 0. See
[build_concrete.log](/audit-output/evidence/build_concrete.log) and
[build_proof.log](/audit-output/evidence/build_proof.log).

Fresh concrete runs of the actual `solution.mpy` produced:

| `ARG1`, `ARG2` | K result | Python canonical/generated |
|---|---:|---:|
| `2`, `3` | `5` | `5` / `5` |
| `0`, `0` | `0` | `0` / `0` |
| `-8`, `3` | `-5` | `-5` / `-5` |
| `2^128`, `-2^128` | `0` | `0` / `0` |
| `2^63-1`, `1` | `2^63` | `2^63` / `2^63` |

The exact `krun` commands and complete bounded configurations are in
[krun_example.log](/audit-output/evidence/krun_example.log),
[krun_zero.log](/audit-output/evidence/krun_zero.log),
[krun_signed.log](/audit-output/evidence/krun_signed.log),
[krun_cancellation.log](/audit-output/evidence/krun_cancellation.log), and
[krun_unbounded.log](/audit-output/evidence/krun_unbounded.log). The matching
Python calls are recorded in
[python_concrete_oracle.log](/audit-output/evidence/python_concrete_oracle.log).

`spec.k` contains exactly one target claim. I independently ran:

```text
kprove spec.k --definition proof-kompiled --spec-module SPEC
```

It printed `#Top` and exited 0. See
[positive_claim.log](/audit-output/evidence/positive_claim.log).

## 4. Adequacy and real-program pinning

The entry claim at `/candidate/spec.k:6` has no `requires` clause. In plain
language its precondition is:

- `X` and `Y` are arbitrary K `Int` values;
- `<k>` contains the exact translated `add` module followed by invocation of
  `"add"` with `pyInt(X)` and `pyInt(Y)`;
- environment and function map are empty, and result is initially zero.

Its postcondition is:

- computation is empty;
- the environment contains the two argument bindings;
- the function map contains the exact loaded `add` binding and body; and
- result is exactly `X +Int Y`.

The result is not fresh or unconstrained, and there is no implication that
weakens equality. The state is satisfiable: `X = 2`, `Y = 3` gives the exact
initial configuration created by `krun`; execution reaches result `5`, as do
both Python implementations.

The submitted translation and the program inside the claim were tokenized as
constructor trees. Both are exactly:

```text
Module(FuncDef("add", Params("x", "y"),
  Return(BinOp("+", Name("x"), Name("y")))))
```

Trusted regeneration was byte-identical first, so this is a mechanical
source-to-claim pin rather than a visual resemblance. The claim then executes
`load(...)` and `invoke(...)`; no helper claim or summary replaces the body.
See [check_program_pinning.py](/audit-output/evidence/check_program_pinning.py)
and [program_pinning.log](/audit-output/evidence/program_pinning.log).

For independent body sensitivity, I changed the program term actually executed
by a ground claim to `Return(Name("x"))`, updated its function binding
consistently, and retained the original expected addition result for
`X = 2, Y = 3`. The mutation passed `kprove --dry-run` (exit 0), then the proof
exited 1 at a reachable final configuration with `result = 2` against the
required `5`. This is not a mutation of an ignored external Python file.
Artifacts:
[spec-body-mutation.k](/audit-output/evidence/spec-body-mutation.k),
[dry run](/audit-output/evidence/body_mutation_dry_run.log), and
[failed proof](/audit-output/evidence/body_mutation_proof.log).

There are no loops or helper claims to align with control flow. The claim covers
all mathematical integers, not examples, fixed sizes, bounded magnitudes, or
bounded unrollings.

## 5. Rule-by-rule static soundness review

The complete lexical inventory is preserved in
[static_inventory.log](/audit-output/evidence/static_inventory.log), produced by
[static_inventory.py](/audit-output/evidence/static_inventory.py). Candidate
local K files are exactly `semantic.k`, `verification.k`, and `spec.k`; there
are no helper K files.

### Declarations and configuration

The seven local syntax declarations contain sixteen productions:

| Sort | Productions | Use |
|---|---|---|
| `Pgm` | `Module(Stmt)` | Used |
| `Stmt` | `FuncDef(String, Params, Stmt)`, `Return(Expr)` | Both used |
| `Params` | exactly two strings | Used |
| `Expr` | `Int(Int)`, `Name(String)`, `BinOp(String, Expr, Expr)` | `Name` and `BinOp` used; `Int` unused by the submitted program |
| `PyVal` | `pyInt(Int)` | Used |
| `Function` | `function(String, String, Stmt)` | Used |
| `KItem` | `load`, `invoke`, `bind`, `eval`, `plusLeft`, `plusRight`, `finishReturn` | All exercised by submitted execution |

There are no local `[function]`, `[total]`, `[functional]`,
`[simplification]`, priority, or opaque declarations. `verification.k`
(`/candidate/verification.k:3-4`) only imports `SEMANTIC`: it defines zero
rules, claims, functions, lemmas, or bridges. `spec.k` contributes only the one
entry claim.

The configuration (`/candidate/semantic.k:33-39`) has exactly the state this
program needs: computation, current bindings, loaded function map, and integer
result. `$PGM` is parsed as the submitted program; `$ARG1` and `$ARG2` are
unbounded K integers. Empty maps prevent stale binding ambiguity. Heap, I/O,
exceptions, allocation, and a call stack are unnecessary for this one
capture-free, side-effect-free, single-expression function.

### Ordinary semantic rules

All eleven rules are ordinary operational rules; none is a proof-only
extension.

| # | Rule at `semantic.k` | Static judgment |
|---:|---|---|
| 1 | `41`, `load(Module(S)) => S` | Faithfully schedules the sole module statement. No result is fabricated. |
| 2 | `43-44`, `FuncDef` | Stores the exact name, two parameters, and body in an initially empty function map. |
| 3 | `46-48`, `invoke` | Requires an exact matching function binding, binds already-evaluated arguments left-to-right, then schedules that stored body. A wrong function name visibly remains stuck rather than using a name oracle. |
| 4 | `50-51`, `bind` | Performs standard K Map update. For valid translated parameters `"x"` and `"y"` and an empty initial map, it creates the expected distinct bindings. |
| 5 | `53`, `Return(E)` | Schedules evaluation of the real return expression followed by result storage. In the admitted source grammar the function body is a single statement, so no later source statement or caller continuation is skipped or incorrectly retained. |
| 6 | `55`, `eval(Int(I))` | Truthfully injects a source integer literal as `pyInt(I)`. It is unused by the submitted body but was separately concretely exercised with result `7`. |
| 7 | `57-58`, `eval(Name(X))` | Requires and returns the value at the actual environment key. It cannot invent an absent binding. |
| 8 | `60-61`, `eval(BinOp("+", ...))` | Selects only the used `+` operator and begins left-operand evaluation. Other operator strings do not silently receive addition semantics. |
| 9 | `63-64`, `plusLeft` | After the left side is an integer, saves it and evaluates the right side, preserving Python's left-to-right order. |
| 10 | `66-67`, `plusRight` | Computes the saved left integer plus the right integer using trusted K `+Int`; operand order and value are correct. This is the low-level primitive modeled by the source operation, not a task-specific oracle. |
| 11 | `69-70`, `finishReturn` | Writes the computed integer to the result cell and removes the return marker. It does not guess or abstract the value. |

The rule fronts are non-overlapping on reachable terms: the three `eval` cases
have distinct constructors; staging markers distinguish the arithmetic and
return steps; map keys are unique. No priorities are needed. No recursive
equations, totalization guards, or simplification interactions exist. The
function name negative run leaves `invoke("add", ...)` stuck after loading only
`"other"`, confirming binding sensitivity
([krun_binding_negative.log](/audit-output/evidence/krun_binding_negative.log)).
Separate concrete fixtures also exercised the unused `Int` rule and direct
parameter lookup
([krun_int_constructor.log](/audit-output/evidence/krun_int_constructor.log),
[krun_parameter_binding.log](/audit-output/evidence/krun_parameter_binding.log)).

The internal representation retains the local environment after completion and
does not model arbitrary multi-statement/caller continuations. That is a
deliberately minimal language boundary, not a false conclusion for any
submitted-program execution on the intended input domain: the grammar admits
only one module statement and one function-body statement, and the contract
observes only the returned integer. I found no concrete or symbolic false
conclusion witness for any rule on that domain, so I do not label this scoped
omission unsound.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`. I created a fresh claim with the
same exact program, state, and unrestricted precondition, changing only the
result obligation from `X +Int Y` to `X +Int Y +Int 1`. It is demonstrably
false at the satisfying input `X = 2`, `Y = 3`: K and both Python
implementations return `5`, while the mutation requires `6`.

The exact checks were:

```text
kprove spec-vacuity-audit.k --definition proof-kompiled --spec-module SPEC-VACUITY-AUDIT --dry-run
kprove spec-vacuity-audit.k --definition proof-kompiled --spec-module SPEC-VACUITY-AUDIT
```

The dry-run exited 0, excluding a parse/import/build failure. The actual proof
exited 1 with `WarnStuckClaimState`; its residual has empty computation and
actual `result = X +Int Y`, and explicitly reports the failed equality with
`X +Int Y +Int 1`. Artifacts:
[spec-vacuity-audit.k](/audit-output/evidence/spec-vacuity-audit.k),
[vacuity_dry_run.log](/audit-output/evidence/vacuity_dry_run.log), and
[vacuity_proof.log](/audit-output/evidence/vacuity_proof.log).

This is independent of the Stage 4 body mutation: Stage 4 tests dependence on
the executed body; this stage tests whether the theorem constrains the result.

## 7. Proven versus assumed accounting

What the successful reachability proof establishes is:

> For every K integer `X` and `Y`, loading the exact submitted constructor term
> for `def add(x, y): return x + y` into the stated empty configuration and
> invoking its stored `"add"` binding reaches empty computation with result
> exactly `X +Int Y` (and the explicitly stated final environment and function
> map).

This is at least the requested partial-correctness result. Under the small,
deterministic semantics, the symbolic execution also reaches that final state
without a termination assumption.

Trust and evidence ledger:

| Boundary | Influence | Classification and support |
|---|---|---|
| K 7.1.293 compiler, LLVM/Haskell backends, and reachability engine | Parsing, execution, and proof checking | Necessary low-level checker trust; two fresh definitions and all recorded runs were made locally. |
| Imported K `Int` and `+Int` | Final result | Acceptable primitive trust. K mathematical integers match the source integer operation's unbounded arithmetic; normal, signed, cancellation, and large-value runs agree with both Python implementations. |
| Imported K `Map` lookup/update/matching | Binding, function selection, final environment | Acceptable state primitive trust; concrete positive and misbinding tests support the exact uses. |
| Trusted CPython-AST translator | Source-to-constructor syntax bridge | Launcher-designated trusted input, byte-checked against the candidate copy; fresh translation and mechanical constructor comparison pin its output to the theorem. |
| Generated K semantics-to-Python intent bridge | Meaning of module load, call, name lookup, return, and integer addition | Audited rule by rule rather than assumed wholesale. The bridge is direct for this six-constructor program and supported by independent differential and concrete tests. |
| Python canonical implementation | Differential oracle only | Trusted reference input. It supports program/intent comparison but is not used to close the K proof. |

There are no proof-local opaque symbols, result summaries, auxiliary lemmas,
operational bridges, task-answer rewrite rules, or external empirical oracles
inside the theorem. The finite differential tests support only the
Python/K-intent bridge; they are not treated as a universal proof. Universal
result correctness comes from the reconstructed K reachability claim over
symbolic `X` and `Y`.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C (trust and
reproducibility) all pass. The proof executes the real pinned body, covers the
full integer contract domain, constrains the result, uses only sound minimal
semantics for the exercised constructs, and is non-vacuous.

VERDICT: PASS
LEGITIMACY: LEGIT
