# Independent adversarial audit: 55-fib

## Audit outcome

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted translated program for integer inputs `N >= 0`, under its
generated K semantics. Fresh builds and proofs succeeded without using any
candidate-compiled definition. The exact translated program is pinned by the
entry claim, its recursive body executes under the operational rules, and the
result is constrained to a recursively defined Fibonacci function.

The verdict is `CONCERNS / LEGIT`, rather than an unqualified pass, because the
generated semantics-to-Python bridge remains an audited but informal language
model. In particular, it models unbounded normal recursive calls and does not
model CPython recursion limits or exceptions. This does not enable a false
returned value on the stated domain and does not invalidate the
partial-correctness theorem, but it limits what may be claimed about literal
CPython execution for very large inputs.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent (including as a symlink), exactly as
this mode requires. There is no contradictory trusted mount and therefore no
infrastructure breach. See `evidence/01-provenance.log`.

### Required inputs and artifact types

The candidate contains regular files for:

- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and a
  structured JSONL generation trace;
- `prompt.py`, `py2mpy.py`, `solution.py`, and `solution.mpy`;
- `semantic.k`, `verification.k`, and `spec.k`.

No required source artifact is missing, mistyped, or symlinked. The prompt and
translator compare byte-for-byte with the trusted mounts:

| Artifact | SHA-256 | Result |
|---|---|---|
| trusted and candidate `prompt.py` | `b99ee738edd1466c976259cf4271917d52d9a0df5220d566646b476a4400a336` | identical |
| trusted and candidate `py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | identical |

`run-input.json` identifies problem `55-fib`, condition `bare`, and
`semantics: false`, consistent with generated rather than supplied semantics.
`metrics.json` claims generation exit 0; `codex-last.txt` and
`codex-output.log` claim two positive `#Top` results and a rejected mutation.
Those were treated only as claims. A bounded extraction is in
`evidence/01-untrusted-claims.log`.

The structured trace is a regular 286,328-byte, 159-line JSONL file with
SHA-256
`a01fb391b6ac530464b7c00853038a169d3b54150700c48c13116d8151ea0546`.
It records the construction and prior commands, but none of its results were
used as proof evidence. See the reviewer-authored parser and output at
`evidence/trace_summary.py` and `evidence/01-trace-summary.log`.

The candidate also contains extra generated evidence: `__pycache__`, three
`*-kompiled` trees, `spec.json`, logs, and a candidate mutation. These are not
source-integrity failures, but all were excluded from reconstruction. There is
no candidate `PROOF.md`; it was not a required proof source and its absence did
not prevent direct inspection.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and intended domain

The trusted prompt says that `fib(n)` returns the nth Fibonacci number and gives
`fib(10) = 55`, `fib(1) = 1`, and `fib(8) = 21`. The trusted canonical program
defines:

- `F(0) = 0`;
- `F(1) = 1`;
- `F(n) = F(n-1) + F(n-2)` otherwise.

The natural intended domain, and the formal domain used by the proof, is the
nonnegative integers. The canonical implementation does not terminate
normally on negative integers.

The submitted `solution.py` uses `if n <= 1: return n`, otherwise the same two
recursive calls. This is extensionally identical to the canonical program for
all `n >= 0`. It intentionally behaves differently outside that domain:
`solution.fib(-1)` returns `-1`, while the canonical implementation reaches
`RecursionError`.

### Trusted regeneration

The trusted translator was run against the scratch copy of `solution.py`.
Fresh output and submitted `solution.mpy` both have SHA-256
`f0b3bfa90a88ce6cdfe7aaed7d6cce9463433792a6efbdb09677369f13c301e1`;
`cmp` exited 0. Exact commands and statuses are in
`evidence/02-regenerate.log`.

### Independent differential test

`evidence/differential_test.py` independently loads
`/tmp/audit-work/trusted/canonical.py` and
`/tmp/audit-work/src/solution.py`. It covers:

- all three documented examples;
- `0`, both sides of the `n <= 1` boundary, and the first recursive cases;
- every integer from 0 through 20;
- seeded generated values from 0 through 25;
- representative values 25 and 30.

There is no collection-valued “empty” input; the scalar analogue is the zero
base case. The run tested 24 distinct intended-domain inputs with zero
mismatches and exited 0. The negative out-of-domain difference was recorded
separately. See `evidence/02-differential.log`.

## 3. Clean proof reconstruction

Only the source files `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, and `spec.k` were copied to `/tmp/audit-work/src`. Trusted
inputs were copied separately. No candidate definition, cache, `spec.json`, or
proof log was copied or referenced.

The installed K toolchain reports version `v7.1.293`.

### Fresh concrete definition and execution

The concrete semantics was compiled from `semantic.k` with the LLVM backend:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/semantic-llvm-kompiled
```

It exited 0; see `evidence/03-kompile-semantic-llvm.log`.

The reviewer-authored `evidence/semantic_differential.py` then ran the actual
submitted `solution.mpy` for `N = 0, 1, 2, 3, 8, 10`. Every `krun` exited 0,
ended with the correct integer in `<k>`, restored the empty environment, and
agreed with both Python implementations. These cases exercise the true and
false `if` branches, function loading, lookup, comparison, both subtraction
arguments, recursive calls, addition, and returns. See
`evidence/03-semantic-differential.log`.

The first reviewer harness run had an over-escaped regex and falsely reported
that it could not parse otherwise-correct raw outputs. That harness error is
preserved transparently at
`evidence/03-semantic-differential-parser-bug.log`; the one-character regex
correction and successful rerun are the evidence used here.

### Fresh proof definition and positive claims

The proof definition was independently compiled with the Haskell backend:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/verification-haskell-kompiled
```

It exited 0; see `evidence/03-kompile-verification-haskell.log`.

Positive proof results:

| Target | Command scope | Exit | Output | Evidence |
|---|---|---:|---|---|
| `SPEC.fib-invoke` | selected independently | 0 | `#Top` | `evidence/03-kprove-fib-invoke.log` |
| all claims, including `SPEC.fib-module` | full `SPEC`, no trust flag | 0 | `#Top` | `evidence/03-kprove-full-spec.log` |

As a separate compositional diagnostic, the module claim also closed with
`#Top` when both labels were loaded and the already independently proved
`fib-invoke` label was marked trusted for that run; see
`evidence/03-kprove-fib-module-with-proved-helper.log`. This diagnostic is not
the basis for acceptance—the authoritative full-spec run used no trust flag
and proved both claims.

Selecting only `SPEC.fib-module` filters out its supporting invocation claim
and led to unproductive recursive unfolding. The auditor interrupted that
diagnostic; it is not counted as success or candidate failure. Its exact
command and enclosing status 130 are recorded in
`evidence/03-kprove-fib-module-alone-status.txt`.

## 4. Adequacy and real-program pinning

### Claims in plain language

`fib-invoke` has these conditions and effects:

- Precondition: `N >= 0`; the function map consists exactly of `"fib"` bound to
  the submitted parameter name and submitted body. The caller argument cell,
  caller environment, and continuation `REST` are arbitrary.
- Postcondition: the invocation produces `fibMath(N)` immediately before the
  same `REST`; it preserves the argument and function map and restores the
  caller environment.

`fib-module` says:

- Precondition: `N >= 0`; `<arg>` is `N`; `<env>` and `<functions>` are empty;
  `<k>` contains the exact translated module.
- Postcondition: `<k>` contains `fibMath(N)`, the environment is empty, and the
  function map contains the exact loaded `fib` body.

Both are all-path reachability claims and therefore partial-correctness
statements under this workflow; they do not establish termination.

### Exact program identity

The module term in `fib-module` has the same `FuncDef`, parameter, comparison,
branch bodies, operators, recursive call order, and constants as
`solution.mpy`. The only surface normalization needed for a standalone parser
comparison is that the claim spells the generated list unit as `.Stmts`,
whereas a concrete `.mpy` file represents the same empty list by an empty
field. After that grammar normalization, fresh `kast --output json` results are
byte-identical with SHA-256
`1b9b63c99bf7b93e06c46018aa2fb7eb9c3fceb846541b4833ecf948c3453141`.
See `evidence/claim-program.mpy`,
`evidence/pinning_check.sh`, and
`evidence/04-parsed-program-pinning.log`.

The earlier attempt to feed the internal `.Stmts` spelling directly to the
concrete-program parser failed visibly and is preserved at
`evidence/04-parsed-program-pinning-internal-unit.log`; it was a parser-layer
distinction, not a term mismatch.

### Control-flow and result constraint

The module claim does not substitute a mathematical program. It starts with
the submitted `Module` term, loads the submitted function body, executes
`topCall`, evaluates the body, and reaches `fibMath(N)`. `verification.k`
contains no rule that rewrites `Module`, `invoke`, `Call`, or the body to
`fibMath`; the connection is the reachability claim itself.

`fibMath(N)` is not a free result variable or opaque oracle. Its two equations
fix its value on every integer `N >= 0`, and the postcondition uses equality by
reachability to that term, not a one-way predicate.

Concrete satisfying states were independently checked in
`evidence/ground-witnesses.k`:

- Invocation witness: `N = 2`, `<arg> = 99`, caller environment
  `"saved" |-> 7`, the exact function map, and continuation
  `evalRight("+", Int(10))`. The ground proof reaches `11`, showing both result
  use and continuation preservation.
- Module witness: `N = 8`, empty initial maps, and the exact module. The ground
  proof reaches `21`.

Both ground claims closed together with exit 0 and `#Top`; see
`evidence/04-ground-witnesses.log`. The independent Python differential gives
`fib(2) = 1` and `fib(8) = 21` for both implementations.

## 5. Rule-by-rule static soundness review

### Local declarations and construct coverage

`semantic.k` declares:

- `Program`: `Module(Stmts)`;
- `Stmts`: an empty-separated list of `Stmt`;
- `Stmt`: `FuncDef`, `If`, and `Return`;
- `Params`: one string parameter;
- `Expr`: `Int`, `Name`, `BinOp`, `Compare`, and one-argument `Call`;
- `CmpOp`: an operator string and right expression;
- `Function`: parameter string and body;
- runtime K items `exec`, `topCall`, `eval`, `evalRight`, `applyBin`,
  `finishCompare`, `applyCompare`, `prepareCall`, `invoke`, `functionEnd`,
  `makeReturn`, `returned`, and `finishIf`.

The configuration has exactly the needed state: `<k>`, input `<arg>`, local
`<env>`, and `<functions>`. There is no heap, allocation, I/O, or mutation in
the submitted program.

Every constructor in `solution.mpy` maps to one of these declarations:
`Module`, list sequencing, `FuncDef`, `Params`, `If`, `Compare`, `CmpOp("<=")`,
`Name`, `Int`, `Return`, `BinOp("+")`, `BinOp("-")`, and `Call`. No used
construct is fabricated or left unmodeled.

There are no local priority rules, simplification rules, `total` declarations,
`functional` declarations, trusted attributes, or opaque syntax symbols in
`semantic.k`. Cell-free operational source rules are compiled by K into rules
whose redex is at the head of `<k>`; they do not rewrite function bodies stored
inside `<functions>`. The compiled contexts for all source locations are
recorded in `evidence/05-compiled-rule-contexts.log`.

### Exhaustive operational rule inventory

All 24 source rules were reviewed:

| ID | Source | Rule and judgment |
|---|---|---|
| S1 | `semantic.k:52` | `Module(SS)` schedules `exec(SS)` then `topCall`; correct module/load order for this entry harness. |
| S2 | `:54` | Empty `exec` becomes `.K`; correct list base case. |
| S3 | `:55` | Nonempty `exec` schedules head statement then tail; correct left-to-right statement order. |
| S4 | `:57-59` | A fresh `FuncDef` inserts its parameter/body into `<functions>` and consumes the statement; guard is true for the actual empty map. |
| S5 | `:61-62` | `topCall` calls the intended `"fib"` entry with `<arg>`; a task-specific entry harness, not an answer oracle. |
| S6 | `:64` | `eval(Int(I))` returns the same unbounded integer; correct. |
| S7 | `:65-66` | `eval(Name(X))` retrieves `X |-> I` from `<env>`; correct for the only local name `"n"`. |
| S8 | `:68-69` | A binary operation evaluates the left operand first; matches Python order. |
| S9 | `:70-71` | After the left integer, evaluates the right operand and retains the left value/operator; correct. |
| S10 | `:72` | Applies integer addition as `I +Int J`; correct. |
| S11 | `:73` | Applies integer subtraction as `I -Int J`; correct operand order. |
| S12 | `:75-76` | Comparison evaluates the left operand first; correct. |
| S13 | `:77-78` | Then evaluates the right operand and retains the left value/operator; correct. |
| S14 | `:79` | `"<="` becomes `I <=Int J`; correct. |
| S15 | `:81` | A true condition executes only the then-statements; correct. |
| S16 | `:82` | A false condition executes only the else-statements; correct. |
| S17 | `:84` | `If` evaluates its test before selecting a branch; correct. |
| S18 | `:86` | A direct named call evaluates its argument before call preparation; correct for the actual unshadowed global `fib`. |
| S19 | `:87` | A completed integer argument becomes `invoke(F,I)`; correct. |
| S20 | `:89-91` | Invocation looks up the exact function, saves the entire caller environment in `functionEnd`, and installs the singleton parameter binding; correct for this one-parameter body. |
| S21 | `:93` | `Return(E)` evaluates `E` before returning; correct. |
| S22 | `:94` | A returned integer is wrapped as `returned(I)`; correct control marker. |
| S23 | `:95` | `returned(I)` skips the remaining `exec` sequence of the current function; correct return behavior and it leaves later `functionEnd`/caller continuation intact. |
| S24 | `:96-97` | At `functionEnd`, unwraps the integer and restores the saved environment; correct call/return state restoration. |

These rules are deterministic on the submitted term. The `true`/`false`,
`"+"`/`"-"`, and empty/nonempty cases are disjoint. The function-definition
guard prevents overlapping duplicate insertion. There are no priorities whose
preemption needs justification.

The model uses a separate textual function namespace and does not generally
model Python rebinding, closures, multiple parameters, fall-through returns,
or arbitrary call targets. Those constructs are absent from this exact
program; minimal generated-semantics coverage is therefore sufficient. Normal
recursive calls preserve the function map, evaluate the left recursive call
before the right, restore each caller environment, and do not allocate or
mutate observable state.

### Verification extension inventory

`verification.k` adds exactly one function declaration and two rules:

| ID | Source | Rule and judgment |
|---|---|---|
| V1 | `verification.k:6` | `fibMath(Int) : Int [function]`; result-bearing but not opaque and not an operational rewrite of program syntax. |
| V2 | `:8-9` | `fibMath(N) => N` when `0 <= N <= 1`; true Fibonacci base equation. |
| V3 | `:10-11` | `fibMath(N) => fibMath(N-1) + fibMath(N-2)` when `N > 1`; true recurrence and strictly descending on the used integer domain. |

The guards are disjoint and cover every `N >= 0`. No equation applies to
negative integers, so the function is intentionally partial outside the
theorem domain. There is no `[total]` claim, simplification rule, priority, or
overlap. The recurrence is ordinary mathematics, not a smuggled operational
shortcut: concrete execution under `semantic.k` never produces `fibMath`.

The independently closed `fib-invoke` claim is the universal connection
theorem from the exact program-defined invocation to `fibMath(N)`, including
caller environment and arbitrary continuation. The full module theorem then
connects the exact translated module to the same value. Distinct ground
outcomes and the false opposite obligation were checked in Stages 4 and 6.

No local rule was judged unsound, so there is no claimed-unsound rule requiring
a false-conclusion witness. The narrower evidence gap is language-model
adequacy: the generated rules do not constitute a machine-checked universal
equivalence theorem to all CPython runtime behavior, especially recursion
limits and exceptions.

The complete numbered source and declaration inventory is preserved in
`evidence/05-static-inventory.log`.

## 6. Fresh non-vacuity test

The candidate's mutation was not reused. The auditor created
`evidence/spec-vacuity.k`, retaining the real invocation lemma and exact module
but changing the module result to `fibMath(N) +Int 1`.

This target is demonstrably false for the satisfying input `N = 0`: both the
real submitted Python program and `fibMath(0)` produce 0, while the mutation
requires 1.

Results:

- A fresh `kprove --dry-run` parsed and built the mutation successfully, exit
  0: `evidence/06-vacuity-dry-run.log`.
- Actual `kprove` exited 1 with `WarnStuckClaimState`, not a parser error,
  timeout, missing import, or unrelated crash. The residual states that
  `fibMath(N) +Int 1` does not equal the reached `fibMath(N)` under `N >= 0`:
  `evidence/06-vacuity-proof.log`.

This is meaningful result sensitivity and passes the non-vacuity gate.

## 7. Proven versus assumed accounting

### Precisely proven

Under the compiled generated semantics and K's reachability logic:

1. For every mathematical integer `N >= 0`, invoking the exact loaded
   submitted `fib` body from any caller environment and continuation is
   partially correct with result `fibMath(N)`, while restoring the caller
   environment and preserving the continuation and function map.
2. Starting with the exact submitted module term, input `N`, and empty maps,
   executing the module is partially correct with result `fibMath(N)` and the
   exact function body loaded.
3. On `N >= 0`, `fibMath` is fixed by the base values 0 and 1 and the standard
   Fibonacci recurrence.

The proof does not establish termination, runtime complexity, absence of
resource exhaustion, or behavior for negative integers.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K v7.1.293 compiler, LLVM/Haskell backends, reachability prover | Parsing, execution, and `#Top` soundness | Necessary low-level trust boundary; rebuilt independently. |
| Imported K `INT`, `BOOL`, and `MAP` modules | Arithmetic, comparison, booleans, environments | Acceptable standard primitives. |
| Trusted mounted prompt, canonical program, and translator | Natural-language oracle, reference implementation, Python-to-MPY syntax bridge | Authority supplied by the audit task; hashes checked. |
| Candidate-generated `semantic.k` | Complete execution model used by the theorem | Not blindly trusted: exhaustively reviewed and concretely reconstructed. Sound for every construct used by this program. |
| Separate function namespace and hard-coded `topCall("fib", ARG)` | Binding and entry selection | Acceptable for this exact unshadowed module; parsed program and exact mapping are pinned. Not a general Python semantics. |
| Unbounded K integers and unbounded normal call model | Values and control | Values match Python integers, but CPython recursion limits/exceptions are excluded. This is the principal documented concern. |
| `fibMath` equations | Final result meaning | Fully defined on the theorem domain by truthful, disjoint recurrence equations; not opaque or totalized outside the domain. |
| `fib-invoke` use by `fib-module` | Recursive program/result connection | Discharged by its independent `#Top` proof and by the no-trust full-spec run; not an unproved assumption. |
| English “nth Fibonacci” interpretation | Bridge from recurrence to human intent | Standard mathematical argument and structurally identical trusted canonical recurrence; finite testing supports but does not replace it. |
| Differential and ground tests | Fidelity evidence on selected inputs | Empirical support only, explicitly not a substitute for either reachability proof. |

### Gate assessment and decision

- Real-program soundness: **pass**. Bodies execute, state/control are
  preserved, `fibMath` is connected universally by the invocation claim, and
  the false result mutation is rejected.
- Intent adequacy: **pass with a documented modeling limitation**. The
  nonnegative domain and recurrence match the prompt/canonical intent, while
  negative inputs and runtime recursion failures are excluded.
- Auditability: **pass**. Source, commands, outputs, reviewer scripts,
  diagnostic failures, and statuses are preserved below `evidence/`.

The limitation does not make a false returned-value claim provable and does not
justify `FAIL / NOT_LEGIT`. It does prevent an unqualified claim that the K
model covers every exceptional behavior of literal CPython, so the appropriate
decision is `CONCERNS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
