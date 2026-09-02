# Independent adversarial audit: 49-modp

## Executive decision

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the exact submitted `solution.mpy` under its generated semantics and the formal
domain `n >= 0` and `p > 0`. A clean source-only rebuild succeeded, all six
positive claims closed independently with exit status 0 and `#Top`, a body
mutation invalidated the claimed result, and a fresh off-by-one postcondition
mutation built but failed with the expected unmet implication.

The result is `CONCERNS / LEGIT`, not `PASS`, for two material but
legitimacy-preserving limitations:

1. The trusted canonical implementation and the generated program disagree at
   `(n, p) = (0, 1)`, which satisfies the formal entry precondition. The
   canonical loop returns `1`; the candidate, K semantics, and the literal
   mathematical value of `2^0 mod 1` return `0`.
2. The generated semantics is a narrow entry-function harness and its unguarded
   `pow` rule is faithful to Python only on the claimed positive-modulus domain.
   For the excluded input `(2, -5)`, K returns `4` while Python returns `-1`.

These are intent/domain and modeling-boundary concerns. No local rule enables a
false conclusion for an input satisfying the target theorem's precondition,
and no candidate-built definition or claimed trace was trusted.

## 1. Input and provenance integrity

### Rendered-mode boundary

The task is `GENERATED_SEMANTICS`. `/reference/reference-semantics` does not
exist, while `/reference` contains exactly the three trusted regular files
`canonical.py`, `prompt.py`, and `py2mpy.py`. This is consistent with the
rendered mode, so there is no infrastructure breach and the candidate may be
judged. See `evidence/01_integrity.log`.

### Required artifacts and trusted-file comparisons

The following candidate artifacts are present as regular files:

- `run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and the JSONL structured trace;
- `prompt.py`, `py2mpy.py`, `solution.py`, and `solution.mpy`;
- `semantic.k`, `verification.k`, `spec.k`, and executable `prove.sh`.

There are no missing, mistyped, or symlinked required artifacts. The candidate
`prompt.py` is byte-identical to `/reference/prompt.py`, and candidate
`py2mpy.py` is byte-identical to `/reference/py2mpy.py`; both `cmp` commands
exited 0. Exact types, modes, hashes, comparisons, and the mode-boundary check
are in `evidence/01_integrity.log`.

The candidate has additional generated entries:
`verification-kompiled/`, `__pycache__/`, `codex-trace/`, and generation
logs/metrics. They are not source integrity failures, but all compiled/cache
content was treated as untrusted and excluded from reconstruction. There is no
candidate `PROOF.md` or `spec-vacuity.k`; neither was a required generation
deliverable, and stage 6 uses a reviewer-authored mutation.

### Untrusted generation claims

`run-input.json` claims the bare/generated-semantics condition and records
prompt/translator hashes matching the trusted files. `metrics.json` claims an
exit-0, non-timeout generation. `codex-last.txt`, `codex-output.log`, and the
174-record JSONL trace claim a successful `kprove` run. Those files were read
only as claims. `evidence/01_untrusted_claims.log` records their hashes, sizes,
record-type inventory, relevant candidate commands, and bounded claimed
outputs. None contributes to the verdict without fresh reconstruction.

Stage 1 result: integrity passes; no infrastructure error.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The prompt's literal contract is: for integer parameters `n` and `p`, return
`2^n` modulo `p`; its five examples are `(3,5)->3`,
`(1101,101)->2`, `(0,101)->1`, `(3,11)->8`, and
`(100,101)->1`.

The trusted canonical implementation initializes `ret = 1`, then performs
`ret = (2 * ret) % p` once for every element of `range(n)`. The candidate
instead implements:

```python
def modp(n: int, p: int):
    return pow(2, n, p)
```

The trusted translator independently regenerated
`/tmp/audit-work/fresh/regenerated-solution.mpy`. It was byte-identical to the
submitted `solution.mpy`; both have SHA-256
`a825c98c476440010d2cd0426d6678d654291cd8a82e6487eb331870fe5b6cf1`.
The command and exit-0 `cmp` are in `evidence/01_integrity.log`.

### Independent differential evidence

`evidence/02_differential.py` imports the trusted canonical entry point from
`/reference/canonical.py` and the copied generated entry point from
`/tmp/audit-work/fresh/solution.py`. Its exact inputs are preserved in
`evidence/02_inputs.json`:

- all five documented examples;
- zero/one loop boundaries and modulus boundaries;
- all 1,089 pairs with `0 <= n <= 32` and `1 <= p <= 33`;
- 750 deterministic generated pairs using seed `49_2026_07_23`;
- selected large-exponent and power-boundary cases.

After deduplication, 1,847 formal-domain inputs were compared. The harness
exited 1 because it intentionally treats any mismatch as failure. There was
exactly one mismatch:

```text
input:      (0, 1)
canonical:  1
candidate:  0
```

This is not an arithmetic error in `pow`: the canonical zero-iteration path
does not reduce its initial `1` modulo `p`. The candidate's result is the
literal mathematical residue. A separate reviewer-authored repeated
multiplication oracle starts at `1 % p`; it matched the candidate on all 1,847
inputs (`evidence/02_intent_oracle.log`). Thus the trusted prompt and trusted
canonical conflict at this boundary. The discrepancy must remain visible and
precludes `PASS`.

The differential log also records behavior outside the formal domain,
including negative exponents and zero/negative moduli. There are several
candidate/canonical divergences there. Because the prompt states no explicit
domain restriction while the formal claim requires `n >= 0` and `p > 0`, this
restriction is an intent-adequacy limitation rather than an implicit fact.

Stage 2 result: translation fidelity passes; candidate/canonical fidelity has
the documented `(0,1)` concern and excluded-domain limitations.

## 3. Clean proof reconstruction

Only the five candidate source artifacts `solution.py`, `solution.mpy`,
`semantic.k`, `verification.k`, and `spec.k` were copied to
`/tmp/audit-work/fresh`. Pairwise hashes and exit-0 `cmp` checks are preserved
in `evidence/03_source_identity.log`. No candidate `*-kompiled` directory was
copied or used.

The installed independently invoked tools report K version `v7.1.293`.

### Concrete definition and executions

The generated semantics was freshly compiled with:

```text
kompile /tmp/audit-work/fresh/semantic.k --backend llvm \
  --main-module MODP-SEMANTIC --syntax-module MODP-SYNTAX \
  --output-definition /tmp/audit-work/fresh/concrete-kompiled
```

The command exited 0. Fresh `krun` executions covered every prompt example,
zero/one boundaries, `p = 1`, a small composite case, and a large exponent.
All ten executions terminated with `.K`, set the expected `formals` cell, and
matched the copied generated Python function. Nine matched the canonical; the
only exception was `(0,1)`. Commands, complete bounded configurations, and
comparison records are in `evidence/03_concrete_compare_rerun.log`.

### Proof definition and every positive claim

The proof definition was freshly compiled with:

```text
kompile /tmp/audit-work/fresh/verification.k --backend haskell \
  --main-module MODP-VERIFICATION --syntax-module MODP-SYNTAX \
  --output-definition /tmp/audit-work/fresh/proof-kompiled
```

This exited 0. The original six-claim spec then exited 0 and printed `#Top`.
Because the candidate claims are unlabeled, the auditor also created six
single-claim files containing exact copies of the original claim bodies and
ran each independently. The general claim and each of the five ground claims
independently exited 0 and printed `#Top`. All exact commands and results are
in `evidence/03_build_and_prove.log`.

Stage 3 result: clean concrete reconstruction and all positive proof targets
pass.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

`spec.k` contains six entry claims:

1. General claim: starting with the exact translated `modp` program, input
   cells `N` and `P`, no formals, and no result, if `N >= 0` and `P > 0`, the
   computation is consumed, formals become `("n","p")`, and the result is
   exactly `expectedModp(N,P)`.
2. Five ground claims: the same exact program and initial cells produce,
   respectively, `3`, `2`, `1`, `8`, and `1` for the five prompt examples.
   These ground claims need no symbolic precondition.

The destination result is not a fresh variable, existential, implication-only
condition, or unconstrained cell. `expectedModp(N,P)` rewrites to the concrete
K term `2 ^%Int N P`. The fresh off-by-one failure in stage 6 further confirms
that this equality is a real obligation.

### Exact program identity and flow

Whitespace-normalized `solution.mpy` is:

```text
Module(FuncDef("modp",Params("n","p"),Return(Call(Name("pow"),Int(2),Name("n"),Name("p")))))
```

That exact normalized term occurs six times in `spec.k`, once in each claim
(`evidence/04_static_inventory.log`). The claim does not replace it with a
helper invocation or summary term. The `Module/FuncDef` rule exposes its
actual `Return` body; the `Return` rule evaluates the actual expression before
writing the result.

There are no loop or helper claims. The generated implementation has no loop;
the loop exists only in the separate trusted canonical implementation.

The semantics uses an entry-harness convention: a top-level `FuncDef` is
treated as invocation of the sole submitted function with the external
`<n>`/`<p>` input cells. This is not literal CPython module execution, which
would merely create a function object. For this exact two-parameter, one-return
program it binds the two source formals and executes the source body, but the
convention is an explicit trust/model boundary.

### Satisfiable states and concrete substitutions

The general precondition is satisfiable, for example with the exact initial
configuration at `N = 3`, `P = 5`; K, generated Python, and canonical Python
all return `3`. Each ground claim's exact initial configuration is also
realizable, as demonstrated by independent proof runs and the differential
examples. Substitution into the five ground destinations agrees with both
Python implementations.

The additional satisfying state `N = 0`, `P = 1` is important:
`expectedModp(0,1)`, generated Python, and concrete K all equal `0`, while the
canonical equals `1`. The formal theorem pins the generated program here; it
does not prove equivalence to the canonical implementation.

A separate body-sensitivity mutation changed source base `2` to `3`. At
`N = 1`, `P = 5`, both mutated Python and concrete K returned `3`; the
unchanged destination requiring `2` built successfully but failed with a
stuck final configuration (`evidence/05_06_sensitivity_and_vacuity.log`).
This rules out body-insensitive or substituted-program closure.

Stage 4 result: real-program pinning and result constraint pass; the entry
harness and canonical boundary remain concerns.

## 5. Rule-by-rule static soundness review

### Complete local declaration inventory

`semantic.k` declares:

- `Expr`: `Int(Int)`, `Name(String)`, and four-position
  `Call(callee,arg1,arg2,arg3)`;
- `Params`: exactly two strings;
- `Stmt`: `Return(Expr)` and `FuncDef(String,Params,Stmt)`;
- `Program`: `Module(Stmt)`;
- state data `Formals`: `noFormals` or `formals(String,String)`;
- state data `Result`: `noResult` or `result(Int)`;
- the `[function]` symbol
  `evalInt(Expr,String,String,Int,Int)`;
- configuration cells `<k>`, `<n>`, `<p>`, `<formals>`, and `<result>`.

`verification.k` adds the `[function]` symbol
`expectedModp(Int,Int)`. There are no local `[total]`, `[functional]`,
`[simplification]`, `[concrete]`, priority, `owise`, `anywhere`, opaque
oracle, allocation, exception, or auxiliary-claim declarations. There are no
generated helper K files. The mechanical counts and exact source lines are in
`evidence/04_static_inventory.log`.

Every submitted syntax construct is covered:

| Submitted construct | Declaration and behavior |
|---|---|
| `Module` | `Program` production; module-entry rule |
| `FuncDef` | `Stmt` production; module-entry rule |
| `Params("n","p")` | `Params` production; stored in `<formals>` |
| `Return` | `Stmt` production; return rule |
| `Call` | `Expr` production; `pow` evaluation rule |
| `Name("pow")` | `Name` production; exact callee match |
| `Name("n")` | first-formal lookup rule |
| `Name("p")` | guarded second-formal lookup rule |
| `Int(2)` | literal evaluation rule |

All constructs were exercised by each successful concrete execution. Missing
semantics for unused Python/MPY constructs is therefore not a defect in this
generated-semantics mode.

### Every local rule

| Rule | Class and complete effect | Judgment |
|---|---|---|
| `evalInt(Int(I),...) => I` | Definitional literal rule; ignores irrelevant environment positions and changes no cell. | Sound. |
| `evalInt(Name(X),X,...,N,...) => N` | First-formal lookup. | Sound for the positional entry environment. |
| `evalInt(Name(Y),X,Y,...,P) => P requires X =/=String Y` | Second-formal lookup. The guard prevents overlap with the first-formal rule. | Sound; exact source formals are distinct. |
| `evalInt(Call(Name("pow"),BASE,EXP,MOD),...) => evalInt(BASE,...) ^%Int evalInt(EXP,...) evalInt(MOD,...)` | Result-bearing external-primitive bridge for Python's unshadowed built-in `pow`. It recursively evaluates proper subexpressions and changes no state cell. | Sound on `EXP >= 0`, `MOD > 0`; over-broad outside that domain. No side-effect ordering issue exists for the exact literal/name arguments. |
| `<k> Module(FuncDef(_F,Params(X,Y),BODY)) => BODY </k>` with `noFormals => formals(X,Y)` | Operational entry-harness rule. The `<k>` cell is exact, so it admits no trailing continuation; it writes only `<formals>`. | Sound as the selected entry convention for the exact submitted program, but not a general CPython module-definition semantics. Ignoring `_F` is harmless because every claim pins `"modp"`. |
| `<k> Return(E) => .K </k>` with `noResult => result(evalInt(...))` | Exact-context return rule. It reads `<n>`, `<p>`, and `<formals>`, writes only `<result>`, preserves inputs/formals, and has no continuation to discard. | Sound for the modeled pure return. |
| `expectedModp(N,P) => 2 ^%Int N P` | Definitional mathematical summary; it does not replace program execution. | Sound on every target claim's safe domain and ground inputs. |

### Overlap, totality, control, and state

The `Int`, `Name`, and `Call` constructors are disjoint. The two `Name` rules
cannot disagree because the second requires distinct formals. The recursive
`evalInt` call descends to proper expression subterms. Neither local function
is marked `total`; unsupported expressions or unsafe hooked arithmetic are
allowed to remain visibly stuck rather than receiving a fabricated result.

There are no competing operational rules or priorities. Both operational
`<k>` matches are exact rather than framed with `...`, so neither can discard
an arbitrary continuation. Inputs are read but never mutated; formals and
result each transition once from their explicit empty constructor. No heap,
allocation, output, exception, or call stack is needed by the exact safe-domain
source body.

The standard `INT`, `BOOL`, and `STRING` modules are imported. The installed K
domain documentation identifies integers as arbitrary precision and documents
`A ^%Int B C` as equivalent to `(A ^Int B) %Int C`, implemented by the
`INT.powmod` hook (`evidence/04_builtin_boundary.log`). For nonnegative `N` and
positive `P`, this agrees with Python's three-argument `pow`.

The `pow` rule is deliberately not claimed sound over all K integers. A
preserved boundary witness shows K returns `4` while generated Python returns
`-1` at `(N,P)=(2,-5)` (`evidence/04_out_of_domain_boundary.log`). This input
does not satisfy `P > 0`, so the rule cannot enable a false target-theorem
conclusion on the formal domain. It is nevertheless an over-broad semantics
rule and reinforces the `CONCERNS` verdict. Negative exponents and zero moduli
are also outside the claim and are not modeled with Python's exception/inverse
behavior.

No rule was labeled materially unsound for the intended positive-modulus
theorem domain, so no on-domain false-conclusion witness is omitted. The
narrower evidence gaps are the entry-harness convention, hardwired built-in
name resolution, and excluded integer behaviors.

Stage 5 result: local rules are sound for the proved domain; generated
semantics is intentionally narrow and over-broad outside that domain.

## 6. Fresh non-vacuity test

The auditor created `evidence/06_spec-vacuity.k`, changing the general
destination to:

```text
result(expectedModp(N, P) +Int 1)
```

The precondition is unchanged and satisfiable; at `N = 3`, `P = 5`, execution
returns `3` while the mutation requires `4`.

The mutation first passed `kprove --dry-run` with exit 0, establishing that it
parsed and built. The real proof then exited 1 with
`WarnStuckClaimState`. Its residual explicitly contains the unmet equality
`2 ^%Int N P +Int 1 #Equals 2 ^%Int N P` under `N >= 0` and `P > 0`.
This is the expected result-bearing failure, not a parser error, missing
import, timeout, or unrelated crash. The mutation, exact commands, statuses,
and complete bounded residual are preserved in
`evidence/05_06_sensitivity_and_vacuity.log`.

The separate base-3 mutation in the same evidence log is operational
sensitivity evidence and is not being reused as the false-postcondition test.

Stage 6 result: non-vacuity passes.

## 7. Proven versus assumed accounting

### Precisely established

Under the freshly compiled `MODP-VERIFICATION` theory, the reachability proof
establishes:

- for every K integer `N >= 0` and `P > 0`, execution of the exact submitted
  MPY term consumes `<k>`, records source formals `("n","p")`, preserves the
  input cells, and writes exactly `result(2 ^%Int N P)`;
- the same exact program reaches each of the five prompt-example results;
- the result depends on the submitted body and cannot be changed by one
  without invalidating the proof;
- the destination result is discriminating, as the off-by-one mutation fails.

This is a partial-correctness result under the generated K semantics. It is not
a proof of equivalence to all CPython behavior or to the trusted canonical on
all annotated integers.

### Trust ledger

| Boundary | Dependents and status |
|---|---|
| K compiler, parser, Haskell/LLVM backends, and reachability prover | All machine results depend on the installed K `v7.1.293` toolchain. This is the ordinary low-level proof checker boundary. |
| K `INT.powmod` and arbitrary-precision integer hooks | Both execution and `expectedModp` depend on this external primitive. It is acceptable as a fixed operation outside the program-defined body, but the theorem is interpretation-parametric in that hook; the local K documentation and concrete comparisons support, rather than prove, its mathematical implementation. |
| Python built-in binding and `pow(2,n,p)` behavior | `solution.py` contains no import, assignment, or parameter named `pow`, so CPython resolves the built-in. The K rule hardwires that resolution. K versus generated Python had zero mismatches on ten normal/boundary runs, including large integers and `p=1`; this finite evidence is not a universal connection theorem. |
| Entry-harness convention | The module rule models calling the sole two-argument function using `<n>` and `<p>`, not loading a Python module and creating a function object. It is adequate for the exact target invocation but concerning as a reusable language semantics. |
| Trusted translator | Byte identity independently connects `solution.py` to `solution.mpy`; this bridge is strong and reproducible. |
| Natural-language/canonical intent | The literal modular-arithmetic oracle supports the candidate on 1,847 inputs, but the trusted canonical disagrees at `(0,1)`, and the prompt does not state the formal sign restrictions. This is the principal intent-adequacy concern. |

Differential tests, concrete traces, K documentation, and informal arithmetic
support only the bridges named above. They are not substitutes for the
reachability proof. Conversely, `#Top` proves closure only under the supplied
theory and does not establish those external bridges by itself.

### Gate summary and verdict rationale

- Real-program soundness: passes. Exact source is pinned, all positive claims
  reconstruct, rules are on-domain sound, body sensitivity holds, and the
  false postcondition is rejected.
- Intent adequacy: limited. The formal domain is stronger than the unstated
  prompt domain, the canonical conflicts at an included boundary, and the
  entry harness is narrower than CPython.
- Trust/evidence auditability: passes with explicit finite-evidence limits.
  Every reviewer command, input set, mutation, status, and relevant bounded
  output is preserved below `/audit-output/evidence`.

`FAIL / NOT_LEGIT` is not warranted: the proof neither substitutes a program,
nor leaves the result free, nor uses a program-derived unconstrained oracle,
nor relies on an on-domain false semantic rule. `PASS / LEGIT` is too strong
because the canonical discrepancy and semantics/domain limits are material.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
