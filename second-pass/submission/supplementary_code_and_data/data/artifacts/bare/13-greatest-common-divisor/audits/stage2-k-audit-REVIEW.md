# Independent adversarial audit: 13-greatest-common-divisor

The candidate contains a legitimate, result-constraining partial-correctness
proof of the exact generated program over all mathematical integer inputs. The
proof and its generated semantics reconstruct cleanly, the entry claim is
constructor-identical to the trusted translation of `solution.py`, and two
fresh false mutations are rejected for the expected semantic reasons.

The result is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, for three
non-fatal validation limitations:

1. the proved loop claim has an empty continuation, while the manually
   installed priority-40 summary admits a framed continuation; the
   generalization is sound for this loop but lacks a bridge-free universal
   framed-context theorem;
2. `gcdSpec` is incorrectly declared `[total]` outside the nonnegative domain
   covered by its equations, and a fresh LLVM evaluator demonstrates why this
   declaration is unsafe to reuse, although the Haskell proof backend behaves
   correctly on every domain used by the proof; and
3. the final identification of the Euclidean recurrence with the
   human-language “greatest common divisor” property is ordinary mathematical
   reasoning plus finite differential evidence, not a separate K theorem about
   divisibility and maximality.

No materially unsound rule, substituted program, narrowed source domain, free
result, or vacuous proof was found.

## 1. Input and provenance integrity

I treated every candidate and generation record as untrusted evidence. The
launcher declares `record_layout = legacy-selected-stage1`,
`condition = bare`, and `semantics_mode = GENERATED_SEMANTICS`.

- `/audit-input.json` and `/audit-campaign-lock.json` are real readable files.
  The `audit_campaign` JSON object equals the lock object, and the independently
  computed lock SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- All records required for `legacy-selected-stage1` are present as regular
  files: `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and
  `prompt.txt`. `usage.json` is present and was also checked. Historical
  `runtime-metrics.json` is absent, as permitted for this layout.
- The structured trace contains one regular JSONL file. All 388 lines parse as
  JSON. Its file hash is the hash recorded by both
  `/generation-result.json` and `invocation.json`; its pipeline tree digest is
  the `source_trace_sha256` recorded by `usage.json`.
- Every recorded per-file hash checked in the launcher input matches the
  mounted bytes, including the run/task/result/invocation records, prompt,
  translator, canonical program, generation prompt, output, last message,
  metrics, usage, and trace.
- There are no symlinks or unsupported entries in `/candidate`,
  `/generation-evidence`, or `/reference`. The independently recomputed
  pipeline-format candidate tree digest is
  `8205fdfb08b67691a58a6df629686cf3b652d07927684465a60771c96757b30e`,
  exactly matching both the retained workspace digest in `invocation.json` and
  the output workspace digest in `/generation-result.json`.
- `/audit-input.json` additionally records launcher tree digests
  `864171...` for the candidate and `acff7f...` for the trace but does not
  declare their serialization. I did not equate those opaque launcher digests
  with the documented pipeline tree format. This is not an observed
  contradiction: individual file hashes and the independently reproducible
  pipeline tree hashes all match their corresponding generation records.
- [`/candidate/prompt.py`](/candidate/prompt.py) is byte-identical to
  [`/reference/prompt.py`](/reference/prompt.py), and
  [`/candidate/py2mpy.py`](/candidate/py2mpy.py) is byte-identical to
  [`/reference/py2mpy.py`](/reference/py2mpy.py).
- `/reference/reference-semantics` is absent, as required by
  `GENERATED_SEMANTICS`. The candidate supplies its own
  [`semantic.k`](/candidate/semantic.k).

The generation records claim prior success, but no prior build, `#Top`, cache,
or report was used. The full integrity check and structured-trace inventory are
in
[`01b-provenance-check-corrected.log`](evidence/01b-provenance-check-corrected.log);
the reviewer script is
[`provenance_check.py`](evidence/provenance_check.py). The earlier
[`01-provenance-check.log`](evidence/01-provenance-check.log) is preserved to
show an initially invalid comparison between two undeclared tree
serializations; the corrected check compares like with like and exits zero.
The live versions are recorded in
[`00-toolchain.log`](evidence/00-toolchain.log): K 7.1.293 and Python 3.10.12.
There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt asks for
`greatest_common_divisor(a: int, b: int) -> int`, “a greatest common divisor”
of the two integers, with examples `(3,5) -> 1` and `(25,15) -> 5`. It states
no positivity restriction. Under the ordinary mathematical convention, the
GCD is nonnegative; `gcd(0,0) = 0` is the convention used by the supplied
canonical and Python's `math.gcd`.

The trusted canonical executes the Euclidean loop directly:

```python
while b:
    a, b = b, a % b
return a
```

The candidate normalizes each input to its absolute value, then performs the
same Euclidean recurrence with scalar assignments
([`solution.py`](/candidate/solution.py)). It accepts the full stated integer
domain; it does not add a bound, fixed size, or positivity precondition.

The trusted translator was rerun in scratch. The regenerated
`solution.regen.mpy` is byte-identical to the submitted
[`solution.mpy`](/candidate/solution.mpy), both with SHA-256
`7f5ef56c549193a381a89a8345f661aafa4e8b9d5d9f3d0bb0b522ef2b784b96`.
See
[`02-translator-regeneration.log`](evidence/02-translator-regeneration.log).

### Independent differential

[`differential_test.py`](evidence/differential_test.py) imports the trusted
canonical and scratch candidate independently. It tests:

- both documented examples;
- all zero and sign-branch boundaries;
- equal, coprime, multiple, and large values;
- the complete grid `[-20,20] × [-20,20]`; and
- 500 deterministic generated pairs in `[-10^12,10^12]`.

Across 2,196 cases, the candidate had zero mismatches with `math.gcd`. There
were 1,077 candidate/canonical mismatches, all also
canonical/`math.gcd` mismatches: the trusted canonical can return a negative
divisor when the second argument is negative or when the loop is skipped with
a negative first argument. Examples are `canonical(25,-15) == -5` and
`canonical(-1,0) == -1`, while the candidate and ordinary GCD contract return
`5` and `1`. The complete bounded output is
[`02-differential-test.log`](evidence/02-differential-test.log).

The differential deliberately exits nonzero to keep the canonical discrepancy
visible. I judge the candidate's nonnegative result to conform to the prompt's
ordinary GCD meaning; the discrepancy is not a narrowing or wrong result in
the candidate. It is nonetheless part of the trust ledger because canonical
equivalence cannot support the negative-input bridge.

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied to
`/tmp/audit-work/reconstruction`. No candidate compiled definitions or caches
were copied or reused. The trusted translator was copied separately. Fresh
output definitions have audit-specific names.

### Generated semantics execution

The generated semantics compiled from source with LLVM:

```text
kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX \
  --backend llvm --output-definition semantic-llvm-audit
```

It exited zero
([`03-kompile-semantic-llvm.log`](evidence/03-kompile-semantic-llvm.log)).
[`concrete_semantics_test.py`](evidence/concrete_semantics_test.py) then ran
the exact submitted `solution.mpy` on 13 normal, zero, sign, equal, multiple,
and large inputs. Every `krun` exited zero, consumed `<k>` to `.K`, and matched
both the candidate Python result and `math.gcd`. The complete configurations
and comparisons are in
[`03b-concrete-semantics-test.log`](evidence/03b-concrete-semantics-test.log).
An initially defective reviewer regex is transparently preserved in
[`03-concrete-semantics-test.log`](evidence/03-concrete-semantics-test.log);
it was a test-harness parsing mistake, not a K execution failure.

### Positive proof targets

The candidate designates two positive proof commands, one per claim-bearing
specification file. Both were rebuilt and run independently:

| Target | Fresh build | Fresh proof |
|---|---|---|
| Loop theorem | [`03-kompile-loop-haskell.log`](evidence/03-kompile-loop-haskell.log), exit 0 | [`03-kprove-loop.log`](evidence/03-kprove-loop.log), exit 0, `#Top` |
| Whole program | [`03-kompile-verification-haskell.log`](evidence/03-kompile-verification-haskell.log), exit 0 | [`03-kprove-whole-program.log`](evidence/03-kprove-whole-program.log), exit 0, `#Top` |

The exact proof commands were:

```text
kprove loop-spec.k --definition loop-haskell-audit \
  --spec-module LOOP-SPEC
kprove spec.k --definition verification-haskell-audit \
  --spec-module SPEC
```

Each spec contains exactly one claim, so these runs independently cover every
positive target claim. The successful dynamic gate is therefore satisfied.

## 4. Adequacy and real-program pinning

### Claims in plain language

The loop claim in
[`loop-spec.k`](/candidate/loop-spec.k) starts with exactly the submitted
Euclidean `while b != 0` statement, an otherwise empty continuation, and the
exact three-entry environment
`a=A, b=B, r=R0`. Its precondition is `A >= 0 and B >= 0`. If the loop
terminates, it consumes the loop and leaves:

- `a = gcdSpec(A,B)`;
- `b = 0`; and
- `r = finalR(B,R0)`, which is `R0` when the initial `B` is zero and `0`
  otherwise.

Other configuration cells are preserved by configuration completion. A
satisfying state is `A=25, B=15, R0=0`; a boundary satisfying state is
`A=7, B=0, R0=13`.

The entry claim in [`spec.k`](/candidate/spec.k) has no `requires` clause:
`A` and `B` range over all K mathematical integers. It starts with the exact
submitted module, empty environment, `inputA=A`, `inputB=B`, and
`noResult`. If execution terminates, it consumes `<k>` and leaves:

- `a = gcdSpec(normInt(A),normInt(B))`;
- `b = 0` and `r = 0`; and
- `result(gcdSpec(normInt(A),normInt(B)))`.

Thus the returned value is explicitly constrained and agrees with the final
`a`; it is not a fresh variable, tautology, or one-way implication.

### Mechanical program identity

[`program_term_compare.py`](evidence/program_term_compare.py) parses the
submitted `solution.mpy` with `kast`, emits the fully parsed entry claim with
`kprove --dry-run --emit-json-spec`, extracts the left side of its `<k>`
rewrite, and compares the complete K constructor trees. They are exactly
equal. This also mechanically handles the harmless textual normalization in
which the claim writes `.Stmts` for the translator's empty list.
See
[`04b-program-term-compare.log`](evidence/04b-program-term-compare.log).
The earlier failed attempt to feed internal `.Stmts` back through the concrete
program parser is preserved in
[`04-program-term-compare.log`](evidence/04-program-term-compare.log).

The translator byte-identity check links this exact constructor term back to
the submitted `solution.py`. Omitted Python annotations are typing-only and
the trusted translator omits them identically.

### Ground witnesses

[`ground_postcondition_test.py`](evidence/ground_postcondition_test.py)
substitutes five satisfying entry states into
`gcdSpec(normInt(A),normInt(B))` and executes the expression with a fresh
Haskell definition. For `(25,15)` the formal expression, generated Python,
trusted canonical, and `math.gcd` all return `5`. For `(25,-15)`, the formal
expression, generated Python, and `math.gcd` return `5`, while the canonical
sign quirk returns `-5`. All five formal results agree with the generated
program and ordinary GCD contract
([`04-ground-postcondition-test.log`](evidence/04-ground-postcondition-test.log)).

### Loop-summary pinning

The whole-program definition manually installs the proved loop transition as
a rule. [`loop_summary_compare.py`](evidence/loop_summary_compare.py)
mechanically emits the loop claim and compares it with the parsed
[`verification.k`](/candidate/verification.k) rule:

- the complete loop constructor term is equal;
- the environment rewrite is equal;
- the precondition is equal; and
- the installed rule has priority 40.

See
[`05b-loop-summary-compare.log`](evidence/05b-loop-summary-compare.log).
The source rule has `<k> loop => .K ... </k>`, so it preserves but admits an
arbitrary continuation. The proved claim has an exact empty continuation. The
candidate supplies no bridge-free universal theorem over the installed rule's
larger continuation domain. This is a real auditability limitation, not
evidence of a false transition.

The rule performs no abrupt return, exception, frame pop, allocation, or I/O.
The fixed loop touches only `<k>` and `<env>`; the summary reads and rewrites
the same cells and frames the untouched input/result cells. A fresh observable
continuation assigns `r = a % 7` after the loop and returns it.
[`bridge_context_test.py`](evidence/bridge_context_test.py) compares the
complete fixed-semantics and bridge-enabled configurations for the submitted
program and that continuation on seven normal/boundary/sign cases. All
configurations agree
([`05-bridge-context-test.log`](evidence/05-bridge-context-test.log)).

## 5. Rule-by-rule static soundness review

The mechanical lexical ledger is
[`05-source-rule-inventory.log`](evidence/05-source-rule-inventory.log).
The following is the exhaustive semantic review, including continuation lines
that a line-head inventory cannot display by itself.

### Local declarations and construct coverage

`MPY-SYNTAX` declares:

1. `Pgm ::= Module(Stmts)`;
2. a concatenative `Stmts` list;
3. five `Stmt` constructors: `FuncDef`, `If`, `While`, `Assign`, and `Return`;
4. `Params` and its comma-separated `Strings` list;
5. five `Expr` constructors: `Int`, `Name`, `UnaryOp`, `BinOp`, and `Compare`;
   and
6. `CmpOp`.

`MPY` declares `Result ::= noResult | result(Int)`, the two control symbols
`execStmts` and `execStmt`, and the partial functions `evalInt` and
`evalBool`. The configuration has exactly the required state:
`<k>`, `<env>`, immutable `<inputA>/<inputB>`, and `<result>`.

Every constructor in `solution.mpy` is covered:

| Program constructor | Declaration/rules |
|---|---|
| `Module`, `FuncDef`, `Params` | syntax at semantic.k:6,9,15 and entry rule 60–64 |
| statement concatenation | `Stmts` at line 7 and rules 66–67 |
| `If` | syntax line 10, boolean rules 55–58, branch rules 72–77 |
| `While` | syntax line 11 and rules 79–85 |
| `Assign` | syntax line 12 and rule 69–70 |
| `Return` | syntax line 13 and rule 87–89 |
| `Int`, `Name`, unary `-`, binary `%` | syntax 18–21 and rules 49–53 |
| comparisons `<` and `!=` | syntax 22–23 and rules 55–58 |

No used construct is replaced by an unconstrained oracle or fabricated result.
Missing syntax for unused Python constructs is permissible in generated
semantics mode.

`GCD-SPEC` declares three result-bearing functions:
`gcdSpec(Int,Int)`, `finalR(Int,Int)`, and `normInt(Int)`, each marked
`[function,total]`. There are no opaque symbols. `LOOP-VERIFICATION` declares
no local syntax or rules. `VERIFICATION` declares the one priority rule.
`LOOP-SPEC` and `SPEC` each declare one reachability claim and no proof-local
functions.

### Fifteen operational/evaluation rules in `semantic.k`

1. `evalInt(Int(I),ENV) => I` is literal evaluation.
2. `evalInt(Name(X),(X |-> I) REST) => I` is deterministic map lookup.
3. Unary `"-"` rewrites to `0 -Int value`, matching Python integer negation.
4. Binary `"%"` rewrites to `%Int`. This rule is broader than the submitted
   execution path, but every actual modulo occurs after sign normalization and
   under `b != 0`; for nonnegative dividend and positive divisor, K and Python
   remainders agree. Negative-divisor and zero-divisor behavior is therefore
   outside every reachable use of this rule in the submitted program.
5. Comparison `"<"` maps to `<Int`.
6. Comparison `"!="` maps to `=/=Int`.
7. The module-entry rule matches exactly one function named
   `greatest_common_divisor` with two parameters, binds them to the input cells,
   and begins its body. This is a narrow entry-point invocation model, but it
   matches the exact submitted module and does not silently accept another
   function name.
8. Empty `execStmts` consumes.
9. Nonempty `execStmts` evaluates the head before the tail using `~>`.
10. Assignment evaluates the right-hand expression in the pre-update
    environment, then updates exactly the named binding.
11. True `If` selects the `THEN` statement list.
12. False `If` selects `ELSE`. Boolean truth and `notBool` guards are disjoint.
13. True `While` schedules the body before the same loop term.
14. False `While` consumes. The two loop guards are disjoint and cover every
    reducible Boolean condition.
15. `Return` evaluates its expression in the current environment, changes
    `noResult` to `result(value)`, and discards the remaining function
    continuation. This models Python return. In the real program return is
    last; no state-changing cleanup or exception effect is omitted.

Evaluation order, lookup, assignments, condition checks, loop recurrence, and
return control all match the submitted scalar integer program. There is no
heap, allocation, I/O, exception, or global state in the program, so omitting
such cells is sound. Integers are unbounded K `Int`, matching Python's relevant
arbitrary-precision behavior.

### Twelve local equations/simplifications in `gcd-spec.k`

1. `gcdSpec(A,0) => A` under `A>=0` is the Euclidean base equation.
2. `gcdSpec(A,B) => gcdSpec(B,A %Int B)` under `A>=0, B>0` is the Euclidean
   step. The guards are disjoint from the base case. On the covered domain the
   remainder is nonnegative and strictly below `B`, so the ground recursion
   descends.
3. `normInt(A) => -A` under `A<0`.
4. `normInt(A) => A` under `A>=0`. These guards are disjoint and cover every
   integer.
5. `finalR(R,R) => 0` with `[simplification]`.
6. `finalR(B,0) => 0` with `[simplification]`.
7. `finalR(0,R) => R`.
8. `finalR(B,R) => 0` under `B != 0`.

The `finalR` rules cover all inputs. Their overlaps agree: `(0,0)` always gives
zero; an equal nonzero pair and every pair with second argument zero also give
zero; nonzero first arguments use the final rule. This is exactly the loop's
bookkeeping: with initial `B=0`, `r` remains `R0`; otherwise the last iteration
sets `r=0`.

9. `{ gcdSpec(A,0) #Equals A } => #Top` under `A>=0`.
10. Its symmetric equality.
11. `{ gcdSpec(A,B) #Equals gcdSpec(B,R) } => #Top` under
    `A>=0, B>0, R=A%B`.
12. Its symmetric equality.

All four simplifications are true instances of equations 1–2 on their complete
guards. Their guards do not overlap inconsistently, and they do not mention a
fresh value. They accelerate symbolic equality checks but do not replace
program execution with an oracle.

The global `[total]` attribute on `gcdSpec` is not justified: no equation covers
`A<0` or `B<0`. This does not affect any proof use because both the loop
precondition and the entry's `normInt` arguments are nonnegative. It is still a
real reusable-theory defect. A fresh LLVM build emits a non-exhaustive-match
warning
([`05-kompile-gcd-eval.log`](evidence/05-kompile-gcd-eval.log)), and its
generated evaluator produces the false ground reduction
`gcdSpec(25,15) => 25`
([`05-gcd-totality-ground-runs.log`](evidence/05-gcd-totality-ground-runs.log)).
This is a concrete intended-domain witness of why the global totality promise
must not be trusted across backends.

The positive proof does not use that LLVM helper evaluator. A fresh Haskell
definition reduces `gcdSpec(25,15)` to `5` and leaves the uncovered
`gcdSpec(-1,0)` opaque
([`05-gcd-ground-haskell.log`](evidence/05-gcd-ground-haskell.log)). A
deliberately false Haskell claim `gcdSpec(25,15) => 25` builds and is rejected
with residual `<k> 5`
([`05-gcd-wrong-dry-run.log`](evidence/05-gcd-wrong-dry-run.log),
[`05-gcd-wrong-proof.log`](evidence/05-gcd-wrong-proof.log)). Thus I do not
attribute the LLVM false reduction to the reconstructed Haskell reachability
proof, but the declaration prevents an unqualified `PASS`.

`normInt` and `finalR` are genuinely total. `evalInt` and `evalBool` are
intentionally not marked total and cover exactly the real expression forms.

### Priority-40 loop rule in `verification.k`

The rule matches the exact real loop at the head of `<k>`, the exact
three-entry environment, and nonnegative `A,B`. It rewrites `a` to
`gcdSpec(A,B)`, `b` to zero, and `r` to `finalR(B,R0)`. It reads/writes only
`<k>` and `<env>` and frames the input/result cells that fixed loop execution
does not touch. Priority 40 makes it preempt the ordinary while rule, so its
justification is critical.

The separately reconstructed loop claim proves the same constructor,
environment transition, and guard using only `MPY` and `GCD-SPEC`; it does not
import `VERIFICATION`. This avoids circular dependence on the bridge. The
remaining match-domain difference is continuation framing, discussed in stage
4. Because the loop body has no abrupt control and the rule rewrites only the
loop item while preserving the suffix, fixed operational execution commutes
with that suffix. Complete-configuration differential checks with an
observable suffix found no discrepancy. I found no satisfiable false
conclusion witness for this rule and therefore do not label it unsound. The
missing universal framed theorem is a narrower evidence gap.

## 6. Fresh non-vacuity test

The reviewer-authored mutation
[`spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k) keeps the exact program,
environment postcondition, and precondition domain but changes the result to:

```k
result(gcdSpec(normInt(A), normInt(B)) +Int 1)
```

It is false at the satisfying state `A=25, B=15`: the independently executed
formal value and both relevant Python oracles are `5`, while the mutation
requires `6`.

The mutation parses and builds successfully under `kprove --dry-run` with exit
0
([`06-vacuity-dry-run.log`](evidence/06-vacuity-dry-run.log)). Its real proof
run exits 1 with `WarnStuckClaimState`; the residual explicitly requires the
false equality
`gcdSpec(A,B) +Int 1 = gcdSpec(A,B)`
([`06-vacuity-proof.log`](evidence/06-vacuity-proof.log)). This is the expected
unmet result obligation, not a parser error, timeout, or unrelated failure.

A separate operational-sensitivity mutation
[`spec-body-mutation.k`](evidence/spec-body-mutation.k) changes the loop body
inside the claim's executed constructor term from `r = a % b` to `r = 0`, while
retaining the GCD postcondition. It also builds successfully
([`06-body-mutation-dry-run.log`](evidence/06-body-mutation-dry-run.log)) and
fails semantically
([`06-body-mutation-proof.log`](evidence/06-body-mutation-proof.log)). The
residual returns `B` and requires the false general equality
`B = gcdSpec(A,B)`; at `A=25,B=15` the mutated body returns `15` instead of
`5`. This demonstrates sensitivity to the actual program body, not merely an
external source file.

The positive proof is therefore non-vacuous and result-constraining.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the local K theory compiled by the Haskell backend, the reconstructed
loop claim establishes partial correctness of the exact Euclidean loop for
all nonnegative `A,B` and arbitrary integer `R0`.

Using the independently proved transition as the priority summary, the
reconstructed entry claim establishes:

> For every mathematical integer pair `A,B`, if the exact submitted translated
> module terminates from empty environment with input cells `A,B`, then it
> consumes its computation and returns
> `gcdSpec(normInt(A),normInt(B))`, with `a` equal to the same value and
> `b=r=0`.

This statement covers the full source-contract integer domain. It is not a
finite unrolling or finite-size theorem. It is partial correctness; it does not
claim a separate termination theorem.

### Trust ledger

| Boundary | Effect and dependents | Audit judgment |
|---|---|---|
| K 7.1.293 Haskell prover, SMT, and builtin `Int`/`Bool`/`Map` | All proof closure and arithmetic reasoning | Necessary low-level trusted computing base; exact versions and fresh commands recorded |
| Trusted `py2mpy.py` | Source-to-constructor identity | Benchmark-authorized primitive; byte regeneration and parsed constructor equality establish the bridge actually used |
| Candidate-generated `MPY` semantics | Binding, evaluation, state, control, and returned value | Audited rule by rule; sound for every reachable construct/path; 13 fresh Python/K concrete comparisons |
| `gcdSpec` equations | Final result and loop summary | Fully value-determining on every proof use; Haskell ground checks and rejected wrong claim support it; global `[total]` attribute outside that domain is defective |
| Euclidean recurrence means mathematical GCD | Human-language postcondition | Standard informal theorem, supported by zero candidate/`math.gcd` mismatches on 2,196 tests; no K divisibility/maximality theorem, so this is a documented intent bridge |
| Priority-40 loop summary | Whole-program proof control and value | Exact body/state/guard proved without the summary; arbitrary continuation generalization is structurally sound and concretely tested, but lacks a universal framed-context connection claim |
| Trusted canonical on negative inputs | Differential evidence only | Not used as a proof axiom; its negative-sign behavior conflicts with ordinary nonnegative GCD and cannot validate those cases |
| `finalR` | Final environment's `r`, not returned GCD | Exhaustive, overlap-consistent equations; loop claim proves its use |
| `normInt` | Sign normalization and all negative-input branches | Exhaustive disjoint equations and direct concrete agreement |

There are no opaque result symbols, unconstrained empirical oracles, hidden
reference semantics, trusted candidate traces, or proof-specific rules that
directly assert the desired final claim.

### Final assessment

- Dynamic reconstruction: pass.
- Exact-program and full-domain adequacy: pass.
- Static soundness on every reachable program path: pass.
- Result/body non-vacuity: pass.
- Auditability/trust-boundary completeness: limited by the framed-loop
  connection theorem, the overclaimed global `gcdSpec [total]` attribute, and
  the informal Euclidean-to-GCD intent theorem.

These limitations prevent an unqualified `PASS`, but none enables the Haskell
proof to establish a false result for a satisfying input, substitutes another
program, or narrows the HumanEval source-contract domain. The candidate is
therefore legitimate with concerns.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
