# Independent adversarial review: 32-find-zero

The reconstructed K proof is machine-closing and non-vacuous for the five
submitted ground examples, and those examples execute a byte-identical copy of
the submitted `solution.mpy`. It is not a proof of the requested program over
the stated input domain. `spec.k` has no symbolic entry claim, domain
precondition, invariant, or universally quantified coefficient list; it proves
only five concrete test cases. That is a material adequacy failure, so the
candidate is not a legitimate partial-correctness proof of the HumanEval task.

## 1. Input and provenance integrity

The rendered mode and trusted mounts agree. `/reference` contains exactly the
three trusted regular files `canonical.py`, `prompt.py`, and `py2mpy.py`;
`/reference/reference-semantics` is absent, as required for
`GENERATED_SEMANTICS`. The candidate tree has no symlinks. See
`evidence/01_environment_and_inventory.log`.

All required generated source artifacts are present as regular files:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
executable `prove.sh`. The required provenance artifacts are also present:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and one
JSONL structured trace. Their types, sizes, modes, hashes, and decoded JSON are
in `evidence/23_provenance_json_and_required_types.log`.

Candidate `prompt.py` is byte-identical to trusted `/reference/prompt.py`
(SHA-256 `17c137ed...b223f`), and candidate `py2mpy.py` is byte-identical to
trusted `/reference/py2mpy.py` (SHA-256 `406485ea...db16`). The candidate also
contains extra generated `semantic-kompiled/`, `verification-kompiled/`, and
`__pycache__/` trees. Those are not source-integrity failures, but they were
treated as untrusted and never copied into or used by the audit builds.

The provenance files claim a bare/generated-semantics run, exit zero, two
successful `krun` checks, and `#Top`. Those claims are internally consistent
but were not trusted. The source/log excerpts are in
`evidence/02_provenance_integrity.log`; the structured trace was independently
decoded by `evidence/extract_generation_trace.py`, with selected messages,
commands, and outputs preserved in
`evidence/04_untrusted_generation_trace.log`.

No required artifact is missing, changed, mistyped, or symlinked. `PROOF.md`
and a candidate vacuity spec are absent, but neither was a required deliverable
of the recorded generation prompt. The compiled/cached trees are the only
material extras.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks for `find_zero(xs)` where `xs` is a nonempty,
even-length coefficient list whose highest-degree (last) coefficient is
nonzero. Thus the polynomial has odd degree and at least one real root. The
function must return one root. The examples require approximately `-0.5` for
`[1, 2]` and `1.0` for `[-6, 11, -6, 1]`.

Trusted `canonical.py` expands a bracket from `[-1.0, 1.0]`, bisects until its
width is at most `1e-10`, and returns the left endpoint. Candidate
`solution.py` implements the same bracketing and bisection control flow with an
iterative polynomial evaluator, but returns the final midpoint. That is a
different yet acceptable root-finding result: the midpoint differs from the
canonical endpoint by at most half the final interval on ordinary terminating
inputs.

Regenerating with the trusted translator produced SHA-256
`a7f52038...cb3fc` for both the regenerated term and submitted
`solution.mpy`; byte comparison exited zero
(`evidence/05_translator_identity.log`).

The reviewer-authored `evidence/differential_test.py` imports the trusted
canonical entry point directly from `/reference/canonical.py` and the copied
candidate entry point from scratch. It tests:

- both documented examples;
- empty, all-zero, and zero-leading outside-domain boundaries;
- roots at the initial midpoint and each initial endpoint;
- both bracket-expansion directions;
- both bisection update directions;
- small and fractional coefficients; and
- 60 deterministic generated valid lists of lengths 2, 4, and 6.

The bounded run covered 74 cases, including 71 intended-domain cases, with
zero material mismatches at a `1e-8` comparison threshold. Both prompt examples
round as required. On normal cases the systematic difference is about
`2.91e-11`, explained by midpoint versus left-endpoint return. The complete
inputs and results are in
`evidence/06b_differential_test_bounded.log` (exit zero).

The first unbounded differential attempt was interrupted and is retained as
`evidence/06_differential_test.log`. It exposed that candidate Python does not
terminate promptly for the invalid zero-leading input `[1, 0]`, because its
integer bracket grows without overflow. The corrected test gives each call a
one-second bound and records that behavior. This outside-domain observation is
not used for the verdict.

Differential testing supports implementation fidelity on the tested values; it
does not prove universal equivalence or replace the K proof.

## 3. Clean proof reconstruction

All work occurred in `/tmp/audit-work/32-find-zero-audit`. Only candidate source
files and trusted reference inputs were copied. No candidate-provided compiled
definition or cache was reused. The live toolchain was K v7.1.293.

Fresh builds:

- LLVM concrete definition: `kompile semantic.k --backend llvm
  --main-module SEMANTIC --syntax-module SEMANTIC-SYNTAX
  --output-definition audit-semantic-kompiled` exited zero
  (`evidence/07_build_concrete_semantics.log`).
- Haskell standalone semantics: the analogous build to
  `audit-semantic-haskell-kompiled` exited zero
  (`evidence/10_build_concrete_haskell_semantics.log`).
- Haskell proof definition: `kompile verification.k --backend haskell
  --main-module VERIFICATION --syntax-module VERIFICATION
  --output-definition audit-verification-kompiled` exited zero
  (`evidence/08_build_proof_definition.log`).

The LLVM definition does not actually execute this program: every tested input
exited 113 with the residual `negRat(rat(1,1))`. The arithmetic equations are
marked `[simplification]`, which this LLVM concrete path did not use as
operational equations. This reproducible backend defect is in
`evidence/09_generated_semantics_concrete_cases.log`; it is not an audit
infrastructure failure.

The Haskell backend used by the proof did execute the actual submitted
constructor tree. Five independent concrete runs all exited zero with empty
environment/function/stack cells:

| Coefficients | Fresh K result | Candidate Python result |
|---|---:|---:|
| `[1,2]` | `-17179869185 / 34359738368` | `-0.5000000000291038` |
| `[-6,11,-6,1]` | `34359738367 / 34359738368` | `0.9999999999708962` |
| `[0,1]` | `-1 / 34359738368` | `-2.9103830456733704e-11` |
| `[-8,0,0,1]` | `68719476735 / 34359738368` | `1.9999999999708962` |
| `[8,0,0,1]` | `-68719476735 / 34359738368` | `-1.9999999999708962` |

The K outputs and exact commands are in
`evidence/11_generated_semantics_haskell_cases.log`; the corresponding Python
and canonical values are in the differential log.

The reviewer copy `evidence/spec-positive-labeled.k` changes only the module
name and adds labels, allowing the five unchanged claim bodies to be selected
one at a time. Each independent `kprove` invocation exited zero and printed
`#Top`:

- claim 1: `evidence/12_positive_claim_1.log`;
- claim 2: `evidence/13_positive_claim_2.log`;
- claim 3: `evidence/14_positive_claim_3.log`;
- claim 4: `evidence/15_positive_claim_4.log`; and
- claim 5: `evidence/16_positive_claim_5.log`.

Finally, the candidate's exact unmodified aggregate command,
`kprove spec.k --definition audit-verification-kompiled --output pretty`,
also exited zero and printed `#Top`
(`evidence/24_original_multi_claim_proof.log`).

Clean reconstruction therefore succeeds for the theorem the candidate actually
wrote. It does not cure that theorem's scope.

## 4. Adequacy and real-program pinning

`verification.k` defines the `solution` macro by embedding a constructor tree.
Removing the four-space K-source indentation from that macro produces a file
byte-identical to submitted `solution.mpy`, with the same SHA-256
`a7f52038...cb3fc` (`evidence/17_program_pinning_identity.log`). Thus the
claims execute the submitted program, not a substituted algorithm.

There are no helper or loop claims. Both program loops and every call to
`evaluate_polynomial` execute through the base semantics. `VerifyRoot` is
strict in its root argument, so the invocation must finish before the residual
test runs. The returned value is not a free variable: it is consumed by
`polyValue`, `absRat`, and `leRat`, and the destination requires
`bool(true)`.

Each entry claim has no `requires` clause. Its complete precondition is simply
the one displayed ground initial state: the exact program and one exact list in
`<k>`, plus empty `<env>`, `<functions>`, and `<stack>` cells. Each displayed
state is itself a satisfying witness. The postconditions are:

1. for `[1,2]`, the returned point has `|1 + 2x| <= 1e-8`;
2. for `[-6,11,-6,1]`, it has
   `|-6 + 11x - 6x^2 + x^3| <= 1e-8`;
3. for `[0,1]`, it has `|x| <= 1e-8`;
4. for `[-8,0,0,1]`, it has `|-8 + x^3| <= 1e-8`; and
5. for `[8,0,0,1]`, it has `|8 + x^3| <= 1e-8`.

These are meaningful, result-constraining claims, and the concrete substitutions
agree with both Python implementations on those inputs.

The fatal adequacy gap is the absence of an entry claim for an arbitrary valid
`xs`. There is no symbolic coefficient list, even-length/nonzero-leading
precondition, root-existence statement, loop invariant, or theorem connecting
the bisection result to the polynomial for the intended domain. Four of the
five claims are hand-selected branch demonstrations, and all five are closed
ground executions. Passing them establishes no result for any sixth valid
coefficient list. This is testing by symbolic-execution machinery, not a
partial-correctness proof of the requested general program.

## 5. Rule-by-rule static soundness review

The exhaustive source inventory is preserved in
`evidence/20_static_rule_inventory.log`: 17 local `syntax` declarations, 46
rules and 3 explicit contexts in `semantic.k`; 4 syntax declarations and 7
rules in `verification.k`; and 5 claims in `spec.k`. There are no opaque
symbols, priorities, `[functional]` declarations, `[owise]` rules, concrete
rules, or separate helper K files.

### Syntax, configuration, and construct coverage

`SEMANTIC-SYNTAX` declares comma-separated strings/expressions, parameters,
statement lists, the used expression constructors (`Int`, `Name`, `UnaryOp`,
`BinOp`, one comparison, one- and two-argument calls), the used statements
(`FuncDef`, `Assign`, `Return`, `For`, `While`, `If`), modules, `Program ;; Expr`,
and the three runtime values `rat`, `bool`, and `list`. It also declares
`Invoke`. The configuration has exactly the state used here: `<k>`, local
`<env>`, global `<functions>`, and a call `<stack>`.

Every constructor in `solution.mpy` is mapped:

| Submitted construct | Declaration/rule group |
|---|---|
| `Module`, `FuncDef`, `Params`, statement concatenation | S11-S16 |
| `Int`, `Name`, `Assign` | S17-S18, S27, generated strict context |
| `UnaryOp`, `BinOp` | S19-S23, explicit contexts C1-C3 |
| `For` and list iteration | S28-S31 |
| `While` | S32-S34 |
| `Compare`, `CmpOp(">")` | S24-S26 |
| `If` | S35-S37 |
| one-/two-argument `Call`, `Invoke` | S38-S45 |
| `Return` | S46 and generated strict context |
| `VerifyRoot` | V7 and its generated strict context |

Missing behavior for unused Python constructs is correctly not treated as a
defect in generated-semantics mode.

### All `semantic.k` rules

- S1-S2 (`gcdInt`, lines 82-84) are Euclid's algorithm. They are mathematically
  correct on the positive-second-argument uses reached from `makeRat`.
- S3-S5 (`makeRat`, lines 93-99) normalize zero, denominator sign, and gcd.
  The overlap at numerator zero and negative denominator agrees at
  `rat(0,1)`. These rules preserve positive denominators on all submitted
  executions.
- S6-S10 (`addRat`, `subRat`, `mulRat`, `divRat`, `negRat`, lines 101-110)
  are the usual rational equations. Division is guarded against zero
  numerator in the divisor; every program division is by 2 or 10,000,000,000.
- S11-S14 (lines 113-120) load a module, execute statement lists in order, and
  clean the externally invoked run. They preserve the computed value and
  intentionally clear the runner's internal state.
- S15-S16 (lines 123-126) install exactly one- and two-parameter function
  bodies in the separate function map. They match the two submitted
  definitions.
- S17-S18 (lines 129-131) construct integer rationals and perform local name
  lookup.
- S19-S23 (lines 133-137), with C1-C3 (lines 139-141), implement unary minus
  and left-to-right `+`, `-`, `*`, `/`. Their equations are correct for the
  normalized rational values reached here.
- S24-S26 (lines 144-147) evaluate the left operand and then right operand of
  `>`. The cross-multiplication direction is correct when denominators are
  positive, which all reachable submitted states preserve.
- S27 (lines 150-151) evaluates the assignment RHS through the generated
  strict context and updates the named local.
- S28-S31 (lines 153-157) evaluate a list once, iterate in order, bind the loop
  variable, execute the complete body, and retain the loop variable, matching
  the used Python `for`.
- S32-S34 (lines 159-162) re-evaluate a `while` guard every iteration and
  select true/false control correctly.
- S35-S37 (lines 164-166) evaluate an `if` guard and execute exactly one branch.
- S38-S43 (lines 169-174) evaluate call arguments left-to-right and translate
  external `Invoke` to the same one-argument call mechanism.
- S44-S45 (lines 176-184) look up the installed function, replace locals with
  its parameter map, and save the whole caller continuation and environment.
- S46 (lines 187-189) discards the remaining callee continuation on return,
  restores the saved caller environment, pops one frame, and resumes with the
  return value. Its abrupt-control footprint matches the modeled Python return
  for these bodies.

No S11-S46 rule is an execution-skipping proof bridge; they are the generated
base semantics. Calls and both loops actually run.

There are nevertheless two bounded semantics concerns:

1. The declarations mark `makeRat`, all five arithmetic helpers, and `negRat`
   `[total]` over all `Val`, although their equations cover only rational
   arguments; `makeRat(_,0)` is also uncovered. The LLVM compiler emitted
   non-exhaustive-match warnings for these declarations (and conservatively for
   `gcdInt`). Likewise, `absRat` and `leRat` below are marked total while
   covering only `rat` values. No submitted claim reaches an uncovered case,
   so this is recorded as a totality/evidence gap rather than an intended-domain
   false-conclusion witness.
2. S26 omits an explicit positive-denominator guard. Cross multiplication is
   false for syntactically allowed negative-denominator `rat` terms, but all
   intended inputs use normalized positive denominators and S3-S10 preserve
   that invariant. Under the audit's witness requirement, this is an
   over-broad-rule evidence gap, not a claimed intended-domain unsoundness.

The simplification-only arithmetic marking also explains the concrete LLVM
failure. It is a portability/executability defect, while the reconstructed
Haskell proof path has consistent operational behavior on all claim states.

### All `verification.k` rules

- V1 (lines 9-48) is the `solution` macro. It is an exact byte-level embedding
  of `solution.mpy`, so it does not substitute or summarize execution.
- V2-V3 (lines 56-58) define the empty and cons cases of
  `polyValue` as `c0 + x*(c1 + ...)`, the correct polynomial for ascending
  coefficients. The recursion structurally decreases the list.
- V4-V5 (lines 60-63) are disjoint negative/nonnegative absolute-value cases
  for normalized rational values.
- V6 (lines 64-65) correctly decides `A/B <= C/D` for positive denominators.
- V7 (lines 68-69) forms the Boolean residual check only after strict
  evaluation of `ROOT`.

V2-V7 are truthful definitional postcondition machinery on all submitted
uses. They do not preempt any program term, supply an oracle result, or bypass
the invocation. The `[total]` domain overstatements for `absRat` and `leRat`
are the same non-reached coverage concern described above.

The generated semantics models exact unbounded rationals rather than CPython
binary floating point and omits Python exceptions. That is an empirical and
informal language-model bridge, not a theorem. It is adequate for the five
small integer ground executions as checked dynamically, but could not support
an unrestricted theorem about all Python numeric inputs without additional
work.

## 6. Fresh non-vacuity test

The candidate supplied no vacuity artifact. The reviewer created
`evidence/spec-vacuity-audit.k`, retaining claim 1's satisfiable ground initial
state but changing its result-constraining destination from `bool(true)` to
`bool(false)`.

The mutation built successfully with `kprove --dry-run` (exit zero;
`evidence/21_stage6_mutation_build_after_static.log`). The actual proof exited
1 with `WarnStuckClaimState`. Its residual is the fully executed configuration
containing `bool(true)`, which does not unify with the false destination
(`evidence/22_stage6_mutation_proof_after_static.log`). This is the expected
unmet obligation, not a parser error, missing import, timeout, or unrelated
crash.

The five ground claims are therefore discriminating and non-vacuous. This
positive result cannot expand their domain.

## 7. Proven versus assumed accounting

What is formally established is precise but narrow:

> Under K v7.1.293's Haskell backend, the local generated semantics and
> verification equations rewrite each of five exact initial configurations to
> a state in which the returned point's exact-rational polynomial residual is
> at most `1e-8`.

Trust and assumption ledger:

| Boundary | Dependents | Assessment |
|---|---|---|
| K Haskell prover and built-in `INT`, `BOOL`, `STRING`, `MAP`, `LIST` semantics | Every build, execution, and claim | Normal low-level trusted computing base. |
| Local rational equations S1-S10 and V2-V6 | Arithmetic, guards, residual checks, all claims | Audited as mathematically correct on normalized rational claim states; totality declarations are over-broad outside those states. |
| Local control semantics S11-S46 | Actual program execution, all claims | Audited against every used construct; no operational shortcut or opaque result. |
| `solution` macro identity | Real-program pinning | Byte identity proved by reconstruction, not assumed. |
| Trusted translator | Python-to-constructor identity | Byte identity of regenerated output established; correctness of the trusted translator itself is outside the candidate theorem. |
| Exact rationals as a bridge to CPython floats | Natural-language/Python interpretation | Informal plus finite empirical evidence only; exceptions, overflow, rounding, and nontermination differences are not modeled. |
| `VerifyRoot` as the intended property | Five postconditions | Its residual formula is explicit and audited, but the `1e-8` tolerance and its relation to the prompt are an intent interpretation. |
| Candidate versus canonical equivalence | Program fidelity | Supported on 71 intended-domain differential cases, not universally proved. |
| Correctness for arbitrary valid `xs` | The HumanEval task | Not established or even stated in K. |

There are no opaque symbols or fresh result-bearing oracles. There are no
empirical primitives inside the proof theory. The differential and concrete
tests support only their tested bridge; they are not used as a substitute for
a K theorem.

### Decision

The positive K reconstruction, program pinning, and non-vacuity checks all
pass for the candidate's five concrete propositions. The candidate nevertheless
fails the required theorem: it proves selected examples rather than partial
correctness of `find_zero` for the prompt's valid coefficient lists. This is a
material adequacy gap, not a minor validation limitation, and matches the
`FAIL / NOT_LEGIT` decision boundary.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
