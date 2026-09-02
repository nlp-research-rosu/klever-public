# Independent adversarial review: 130-tri

This review treats every candidate artifact, generated trace, prior build, and
reported `#Top` as untrusted. I copied only source artifacts into
`/tmp/audit-work/130-tri`, rebuilt fresh LLVM and Haskell definitions, and kept
reviewer-authored tests and bounded logs in `/audit-output/evidence`.

The final judgment is **CONCERNS / LEGIT**. The reachability proof is
reproducible, non-vacuous, executes the exact submitted constructor tree, and
uses no result oracle or execution-bypassing rule. Its important limitation is
that `semantic.k` is a narrow, resource-unbounded, value-level model of this
program rather than a general CPython semantics. It proves mathematical
partial correctness of normal returned values; it does not establish that
CPython returns normally for every non-negative integer.

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`test ! -e /reference/reference-semantics` exited 0. The trusted reference mount
contains exactly `canonical.py`, `prompt.py`, and `py2mpy.py`; there is no
contradictory supplied semantics. There is therefore no infrastructure breach.

### Required artifacts and types

The candidate contains all generation deliverables:

- `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
  `prove.sh`;
- `prompt.py` and `py2mpy.py`;
- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and
  one structured JSONL generation trace.

No candidate symlinks, special files, or helper K files were found. The
candidate also contains two compiled-definition directories and `__pycache__`;
these are extra build products, not source-integrity failures, and were not
copied or reused. `PROOF.md` and a candidate vacuity spec are absent, but
neither was a required generation deliverable and neither absence substitutes
for this audit.

The structured trace has 173 valid JSON records. `run-input.json` identifies
problem `130-tri`, condition `bare`, and no supplied semantics. The metrics and
logs merely claim a successful generation; no verdict relies on those claims.

### Trusted-file comparisons

Candidate `prompt.py` is byte-identical to `/reference/prompt.py`:

`68f3722378473214d80f09420cfa3335984eccd0d4c15a0117985261d22fd01c`

Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`:

`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

Evidence: `evidence/00_environment_and_provenance.sh` and
`evidence/00_environment_and_provenance.log`. The isolated copy operation and
its exact file list are in `evidence/01_prepare_scratch.sh` and
`evidence/01_prepare_scratch.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a non-negative integer `n`, return the sequence prefix at indices `0`
through `n`, inclusive. The trusted prompt and canonical implementation fix:

- `t(0) = 1` (from the returned prefix and canonical base case);
- `t(1) = 3`;
- for even `i`, `t(i) = 1 + i / 2`;
- for odd `i >= 3`,
  `t(i) = t(i-1) + t(i-2) + t(i+1)`;
- the documented example is `tri(3) = [1, 3, 2, 8]`.

The trusted canonical implementation returns Python floats from index 2 onward
because it uses `/`, although all values are integral. The prompt describes
numbers and prints integral examples, so numeric equality is the material
contract; the type difference is recorded below.

### Submitted algorithm

`solution.py` recursively obtains the prefix through `n-1` and appends one
closed-form value:

- base `n = 0`: `[1]`;
- positive even `n`: `1 + n // 2`;
- positive odd `n`: `((n+1)//2) * ((n+5)//2)`.

For `n = 2k+1`, the odd expression is `(k+1)(k+3)`. This satisfies the
prompt's recurrence because

`(k+1) + k(k+2) + (k+2) = (k+1)(k+3)`.

Thus the different algorithm is value-correct over the mathematical
non-negative-integer domain.

### Translation identity

The trusted translator regenerated `solution.mpy` byte-for-byte. Both files
have SHA-256:

`22d6128fdbae80fa2d4785035d262da6050bbe91572a3a1b7825c8579fc85663`

Evidence: `evidence/02_program_fidelity.sh` and
`evidence/02_program_fidelity.log`.

### Independent differential test

`evidence/differential_tri.py` imports the isolated trusted canonical entry
point and submitted entry point without importing candidate tests or proof
equations. It covers:

- documented and branch-boundary inputs `0` through `10`;
- every integer `0` through `60`;
- 21 deterministic generated values through `297`;
- CPython recursion-limit probes `988, 995, 998, 999, 1000, 1001`.

Results:

- no numeric list mismatch on any input where the candidate returned;
- no mismatch against an independently coded integer closed form;
- canonical elements are a mix of `int` and `float` for every tested `n >= 2`,
  while the candidate elements are `int`;
- the submitted recursion returned through `n = 995` in this run, then raised
  `RecursionError` for `998, 999, 1000, 1001`; the iterative canonical returned.

The last point is a total-behavior limitation, not a wrong returned value. It
matters to the bridge from the mathematical proof to real CPython, but a
partial-correctness proof does not prove normal termination. Exact inputs,
summaries, and exit 0 are in `evidence/02_program_fidelity.log`.

## 3. Clean proof reconstruction

### Fresh builds

K version `v7.1.293` was independently available. I did not copy or reference
the candidate's `semantic-kompiled` or `verification-kompiled`.

From the isolated source copy I built:

- an LLVM concrete definition from `semantic.k`, main module
  `TRI-SEMANTIC`, syntax module `MPY-SYNTAX`;
- a Haskell proof definition from `verification.k`, main module
  `TRI-VERIFICATION`, syntax module `MPY-SYNTAX`.

Both `kompile` commands exited 0. Exact commands and statuses are in
`evidence/03_clean_reconstruction.sh` and
`evidence/03_clean_reconstruction.log`.

### Positive claims

I reconstructed each target claim in a small reviewer spec under
`evidence/positive-claims/` and ran it against the fresh Haskell definition:

| Claim | Preconditions | Result |
|---|---|---|
| exact `evalCall` interpreter claim | `N >= 0` | `#Top`, exit 0 |
| configured `run` entry, with its `evalCall` helper | `N >= 0` | `#Top`, exit 0 |
| `triValue(0) = 1` | none | `#Top`, exit 0 |
| `triValue(1) = 3` | none | `#Top`, exit 0 |
| even-value equation | `N >= 2`, even | `#Top`, exit 0 |
| odd recurrence | `N >= 3`, odd | `#Top`, exit 0 |

The mathematical claims emitted `WarnTrivialClaim` because the guarded
function equations simplify both sides before operational rewriting; they
still exited 0 with `#Top`. The exact submitted `spec.k` was also run unchanged
and exited 0 with `#Top`; see `evidence/03b_exact_submitted_spec.sh` and `.log`.

### Concrete generated-semantics execution

Fresh `krun` executions at `n = 0, 1, 2, 3, 6, 10` all exited 0 and returned,
respectively:

- `[1]`
- `[1, 3]`
- `[1, 3, 2]`
- `[1, 3, 2, 8]`
- `[1, 3, 2, 8, 3, 15, 4]`
- `[1, 3, 2, 8, 3, 15, 4, 24, 5, 35, 6]`

`evidence/compare_k_python.py` parses these fresh K results and compares them
programmatically with both Python implementations. All six comparisons are
equal. Commands and outputs are in
`evidence/04_semantics_python_comparison.log`.

That same probe exposes the execution-model boundary: at `n = 998`, fresh K
returns a list of length 999 ending in 500, while actual submitted CPython
raises `RecursionError`. This does not falsify any normal returned value, but
it prevents interpreting the proof as a total-correctness or full
CPython-exception theorem.

## 4. Adequacy and real-program pinning

### Entry and mathematical claims in plain language

1. `evalCall` claim: for any mathematical integer `N >= 0`, evaluating
   function `"tri"` in the exact `solutionProgram` constructor tree is
   partially correct with returned value `LVal(triPrefix(N))`.
2. `run` claim: the configured entry point for that same exact program and
   domain has the same returned value.
3. Base-zero claim: the mathematical element at index 0 is 1.
4. Base-one claim: the mathematical element at index 1 is 3.
5. Even claim: for every even `N >= 2`, the mathematical element is
   `1 + N/2`.
6. Odd claim: for every odd `N >= 3`, the mathematical element equals the sum
   of its two predecessors and its even successor.

The entry postconditions constrain the complete returned `IntSeq` to
`triPrefix(N)`. There is no right-only free result variable, tautological
implication, unconstrained oracle, or omitted return cell.

### Exact program identity

Using the fresh Haskell definition, I compared:

- KORE parsed from the trusted-regenerated submitted `solution.mpy`; and
- KORE obtained by macro-expanding `solutionProgram`.

They are exactly equal. Both `kast` commands and the equality check exited 0.
This is recorded as `ast_identity_status=0` in
`evidence/03_clean_reconstruction.log`. Consequently, the proof executes the
submitted `Module(FuncDef(...))` tree rather than a substituted algorithm.

The `evalCall` claim follows actual control flow into the recursive call at
`N-1`. Its circular reuse occurs only after semantic execution has reached the
smaller recursive invocation, so it is the proof's induction/circularity, not
an operational shortcut rule.

### Satisfiable entry states and ground substitution

Every precondition is satisfiable:

- entry and zero claims: `N = 0`, returned prefix `[1]`;
- base-one and odd implementation branch: `N = 1`, returned `[1, 3]`;
- even claim: `N = 2`, returned `[1, 3, 2]`;
- odd recurrence claim: `N = 3`, returned `[1, 3, 2, 8]`.

The fresh K runs, submitted Python, and trusted canonical agree numerically on
all four. The differential and K/Python comparison logs preserve these
substitutions.

### Adequacy conclusion

The theorem pins the real source constructor tree and its returned values
under the candidate's stated, narrow source-level semantics. It does not model
CPython recursion limits, exception states, object identity, or allocation.
Those omissions are unobservable for the contents of every normal return from
this pure program, but the recursion limit is reachable on the stated
non-negative domain. This is why the audit selects `CONCERNS`, not an
unqualified `PASS`.

## 5. Rule-by-rule static soundness review

There are no generated helper K files besides `semantic.k`. Full numbered
source and declaration extraction are preserved in
`evidence/05_static_inventory.log`.

### Syntax, configuration, and attributes

The complete local syntax inventory is:

- `Program`: `Module(Stmts)`;
- `Stmts`: separator-free K list of `Stmt`;
- `Stmt`: `FuncDef`, `If`, `Return`;
- `Strings`: comma-separated `String` list; `Params(Strings)`;
- `Exprs`: comma-separated `Expr` list;
- `CmpOps`: comma-separated `CmpOp` list;
- `Expr`: `Int`, `Name`, `BinOp`, `Compare`, `ListExpr`, `Call`;
- `CmpOp`: operator string plus comparator expression;
- `IntSeq`: `nil`, `cons(Int, IntSeq)`;
- `Value`: `IVal`, `BVal`, `LVal`;
- `Result`: `returned(Value)`, `fellThrough`;
- `KItem`: `run`, `evalCall`, `findCall`, `exec`, `doReturn`, `choose`,
  `afterBranch`, `evalExpr`, `binLeft`, `binRight`, `cmpLeft`, `cmpRight`,
  `singleton`, `callArg`, `callDone`;
- verification syntax: macro `solutionProgram`, functions `triValue(Int)` and
  `triPrefix(Int)`.

The configuration has only `<k> run($PGM, $N) </k>`. That is sufficient for
this pure program: it has one parameter, no assignment, mutation, globals,
I/O, alias-sensitive observation, heap access, or exceptions handled in the
source. Caller continuations carry the only needed call state.

Functions are `bin`, `append`, `triValue`, and `triPrefix`.
`solutionProgram` is a macro. There are no `[total]`, `[functional]`,
`[simplification]`, `[concrete]`, priority, `owise`, or opaque declarations or
rules.

### Mapping every used constructor

| Submitted construct | Declaration and behavior |
|---|---|
| `Module` | `Program` syntax; `evalCall` opens definitions |
| `FuncDef("tri", Params("n"), ...)` | `Stmt`/`Params`; two `findCall` rules |
| `If` | `exec(If...)`, two guarded `choose` rules, two `afterBranch` rules |
| `Return` | `exec(Return...)`, `doReturn` |
| `Int` | literal evaluation to `IVal` |
| `Name("n")` | parameter lookup to the current call integer |
| `BinOp` | left-to-right `binLeft`/`binRight`; integer/list equations |
| `Compare(..., CmpOp("==", ...))` | left-to-right compare and disjoint true/false rules |
| singleton `ListExpr` | evaluate element, construct one `cons` |
| one-argument `Call(Name("tri"), arg)` | argument first, function lookup, return to caller |
| operators `+,-,*,%,//` | exact equations listed below |

Every used form has both syntax and an applicable rule path. Broader unused
forms admitted by list syntax visibly get stuck rather than fabricating a
result.

### Operational rules: exhaustive adjudication

| ID / line | Rule | Decision |
|---|---|---|
| S1 / 63 | `run(P,N) => evalCall(P,"tri",N)` | Sound entry selection for the required entry point; preserves any framed continuation. |
| S2 / 65 | `evalCall(Module(DEFS),...) => findCall(...)` | Sound decomposition and retains the complete program for recursion. |
| S3 / 68 | matching `findCall(FuncDef(F,...),F,...) => exec(BODY,...)` | Sound for the exact one-parameter `tri`; parameter name is abstracted to the integer call context. |
| S4 / 70 | nonmatching definition skips when names differ | Sound linear lookup for the exact module; guard is disjoint from S3. |
| S5 / 74 | empty statements fall through | Sound. |
| S6 / 75 | `Return(E)` evaluates `E` then `doReturn`, discarding later statements | Sound abrupt return behavior. |
| S7 / 77 | value plus `doReturn` becomes `returned` | Sound. |
| S8 / 79 | `If` evaluates its condition before selecting a branch | Sound evaluation order. |
| S9 / 81 | true selects `THEN` | Sound. |
| S10 / 83 | false selects `ELSE` | Sound and disjoint from S9. |
| S11 / 85 | a branch return bypasses remaining statements | Sound return propagation. |
| S12 / 87 | a fall-through branch executes remaining statements | Sound. |
| S13 / 90 | integer literal becomes `IVal` | Sound. |
| S14 / 91 | `Name("n")` reads the current call integer | Sound for this exact binding; deliberately not general name lookup. |
| S15 / 92 | start binary expression with left operand | Sound left-to-right order. |
| S16 / 94 | after left value, evaluate right | Sound; saves the left value. |
| S17 / 96 | apply `bin` to left then right values | Sound operand order. |
| S18 / 99 | start a single `==` comparison with its left operand | Sound for the only submitted comparison shape. |
| S19 / 101 | evaluate comparator after integer left result | Sound. |
| S20 / 103 | equal integers yield true | Sound. |
| S21 / 105 | unequal integers yield false | Sound, exhaustive and disjoint from S20. |
| S22 / 108 | evaluate singleton-list element | Sound for every submitted `ListExpr`. |
| S23 / 110 | make `cons(I,nil)` | Sound returned-content model. |
| S24 / 112 | evaluate one call argument before lookup | Sound for the only submitted call shape. |
| S25 / 114 | integer argument invokes named function | Sound; the caller continuation remains behind `callDone`. |
| S26 / 116 | returned callee value resumes caller | Sound value/control behavior for this pure function. |
| S27 / 118 | integer `+` | Sound K/Python unbounded-integer correspondence. |
| S28 / 119 | integer `-` | Sound, including construction of the recursive `N-1`. |
| S29 / 120 | integer `*` | Sound. |
| S30 / 121 | integer `%` | Sound on the submitted path: non-negative dividend, divisor 2. It is not a complete Python modulo model for negative operands. |
| S31 / 122 | `//` represented by K `/Int` | Sound on every submitted path because operands are non-negative and divisor is 2. It is over-broad outside that domain. |
| S32 / 123 | list `+` becomes structural append | Sound for observable contents; allocation and identity are outside the model and unused. |
| S33 / 125 | `append(nil,YS) = YS` | True list equation. |
| S34 / 126 | `append(cons(X,XS),YS) = cons(X,append(XS,YS))` | True, structurally descending list equation. |

The concrete off-domain probe in
`evidence/07_off_domain_semantics_probe.log` shows S31 is not a general Python
floor-division rule: K evaluates modeled `-1 // 2` to 0 while Python evaluates
it to -1. No execution from an entry precondition `N >= 0` in the submitted
program reaches a negative floor-division operand, so this is not an
intended-domain false-conclusion witness and I do not label the entry theorem
unsound. It is a documented over-broad-semantics concern.

The `findCall`, name, list, and call rules are similarly purpose-scoped rather
than general Python: they abstract a single integer parameter, singleton
lists, and one-argument calls. Those restrictions exactly cover the submitted
tree; unused constructs need not be modeled in `GENERATED_SEMANTICS` mode.

The exception/resource limitation does have an intended-domain witness:
`N = 998` returns under K but raises `RecursionError` in this CPython
environment. This is caused by the configuration and call rules having no
bounded runtime stack or exception state. The review treats that as an
explicit abstraction boundary for partial correctness, not as evidence of a
wrong normally returned value. It would be illegitimate to cite this proof as
total correctness or full CPython behavioral equivalence.

### Verification rules: exhaustive adjudication

| ID / line | Rule | Classification and decision |
|---|---|---|
| V1 / 8 | `solutionProgram` macro expansion | Definitional syntax macro, not an operational bridge. Fresh KAST equality proves exact identity with `solution.mpy`. |
| V2 / 33 | even `triValue` equation | True for guarded non-negative even `N`; guard is disjoint from V3. |
| V3 / 35 | odd `triValue` equation | True closed form for guarded non-negative odd `N`; guard is disjoint from V2. |
| V4 / 39 | `triPrefix(0) = cons(1,nil)` | True base definition. |
| V5 / 40 | positive prefix appends `triValue(N)` to prefix `N-1` | True, strictly descending definition; guard is disjoint from V4. |

`triValue` is defined on all non-negative integers by the disjoint parity
rules and `triPrefix` is defined on all non-negative integers by the disjoint
zero/positive rules. Neither is marked total outside that domain.

These symbols do not replace `evalExpr`, `evalCall`, or another program
operation. They occur in the postcondition, while the entry claim separately
connects fixed operational execution of the exact body to their fully defined
values. Therefore they are definitional summaries, not opaque
program-derived oracles and not circular operational bridges.

### Claim inventory and soundness

The six claims are exactly the two entry/connection claims and four
mathematical facts described in stage 4. The odd recurrence is independently
valid by the algebra above. There are no proof-local simplification rules,
priority rules, assumed lemmas, or ordinary operational rules in `spec.k`.

No inventoried rule encodes a false task answer on the intended normal-return
path, bypasses the submitted body, or leaves a result-bearing symbol
unconstrained.

## 6. Fresh non-vacuity test

I did not rely on a candidate mutation artifact. The fresh
`evidence/spec-vacuity-audit.k` retains the successful `evalCall` helper but
changes the configured entry result from `triPrefix(N)` to
`triPrefix(N + 1)`.

This mutation is demonstrably false at the satisfiable entry `N = 0`:

- actual K/Python result: `[1]`;
- mutated obligation: `[1, 3]`.

Results:

- `kprove --dry-run` exited 0, proving the mutation parses and builds;
- actual `kprove` exited 1;
- output contains `WarnStuckClaimState`;
- the residual explicitly compares returned `triPrefix(N)` with the
  additional appended `triValue(N+1)` required by `triPrefix(N+1)`.

Thus the failure is the expected unmet result obligation, not a parser error,
missing import, timeout, or unrelated backend failure. Exact commands,
statuses, and the 838-byte residual are in
`evidence/06_fresh_nonvacuity.sh` and
`evidence/06_fresh_nonvacuity.log`.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Conditional on the fresh K definition and its audited rules, for every
mathematical integer `N >= 0`:

- normal operational execution of the exact submitted constructor program is
  partially correct with returned structural list `triPrefix(N)`;
- the configured `run` entry has the same result;
- `triPrefix` starts with 1 and appends the guarded `triValue` at every
  positive index;
- `triValue` has bases 1 and 3, the prompt's even values, and satisfies the
  prompt's odd recurrence.

The circular `evalCall` use is an induction/circularity for partial
correctness. It does not prove termination.

### Trust and assumption ledger

| Boundary | Dependents | Judgment |
|---|---|---|
| K parser, compiler, Haskell prover, LLVM runner, and reachability kernel | all machine-check results | Standard low-level trusted computing base; version and fresh commands recorded. |
| Imported `INT`, `BOOL`, `STRING` operations and generated K list productions | arithmetic, guards, syntax | Standard K primitives; acceptable and independently ground-tested on representative values. |
| Trusted mounted translator | source-to-`solution.mpy` bridge | Acceptable: mounted candidate copy is byte-identical and fresh translation is byte-identical. |
| `solutionProgram` macro | real-program pinning | Not merely assumed: fresh macro-expanded KORE equals submitted-program KORE. |
| `triValue` and `triPrefix` equations | entry postcondition and recurrence claims | Audited truthful, guarded, disjoint, descending definitions; no opacity. |
| Purpose-scoped parameter/name/call model | execution connection | Acceptable for this exact pure one-parameter body; not reusable as general Python semantics. |
| K `Int` and structural `IntSeq` as returned numeric/list contents | bridge to Python values | Supported by concrete K/Python comparisons and source inspection; allocation, identity, and Python numeric class are excluded. |
| Resource-unbounded calls and absent exception state | bridge to actual CPython termination behavior | Concerning but explicit. `N=998` witnesses the difference. The proof must be read as partial correctness of normal returned values, not total/full-runtime correctness. |
| Finite differential evidence | source intent bridge only | 0 numeric mismatches on all normal returns tested; it supports but does not replace the K connection proof or universal algebra. |

The canonical float-versus-candidate-int distinction is empirically visible
for `n >= 2`. Since all values are integral and Python list equality agrees,
this is not a material numeric-result divergence, but the proof does not
establish element-class identity with the canonical implementation.

### Gate summary

- Real-program soundness / result constraint: **PASS** for the exact program
  under the generated source-level semantics.
- Intent adequacy: **PASS with limitation** for numeric sequence values;
  termination, CPython recursion exceptions, and canonical element classes are
  outside the theorem.
- Trust/evidence auditability: **PASS**; all builds, tests, claims, and the
  fresh negative mutation are reproducible from preserved sources and logs.

The limitations are material enough to prevent an unqualified `PASS`, but
they do not introduce a false normally returned value, an oracle, a
substituted body, or a vacuous theorem. The candidate therefore contains a
legitimate partial-correctness proof with documented semantics/intent
boundaries.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
