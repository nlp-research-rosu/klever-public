# Independent adversarial review: 76-is-simple-power

## Executive decision

The candidate contains a freshly reproducible, non-vacuous K reachability proof
of the behavior of the submitted `solution.mpy` under the supplied semantics.
The proof runs the real submitted function: there is no operational rewrite
that replaces the function, call, loop, return, or result with an oracle.  The
candidate-local recursive summary is connected to the exact loop context by a
separately proved reachability claim.  All five positive claims close in fresh
builds, and a fresh false-result mutation fails with the expected residual.

I nevertheless assign `CONCERNS`, not `PASS`.  The prompt never states that
`x` and `n` are positive.  The formal predicate declares every `X > 1,
N <= 1` case false.  At the satisfiable instance `(x,n)=(4,-2)`, this is the
actual generated-program result, but the trusted canonical implementation
returns true because `(-2)**2 = 4`.  The broad negative-base differential
found 26 such discrepancies.  Thus the K theorem is a sound execution
characterization, and it is the usual simple-power predicate on the inferred
positive-integer domain, but the bridge to the unqualified natural-language
contract has a real domain limitation.  That bridge is also informal rather
than a K theorem about exponentiation.

There are additional provenance concerns: four required generation-record
artifacts are absent, and the submitted `spec.json` is stale and does not
describe the current `spec.k`.  Neither issue was used to infer proof success.

## 1. Input and provenance integrity

### Mode and trusted-mount boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present.  This is internally consistent;
there is no infrastructure breach.  Evidence:
`evidence/stage1-mode-and-inventory.log`.

I recursively compared `/candidate/reference-semantics` with the trusted tree
using `diff --recursive --no-dereference --report-identical-files`.  The
candidate tree contains no symlink, and all 24 files and both directories have
matching types and byte-identical contents.  There are no missing, additional,
changed, mistyped, or symlinked entries.  Evidence:
`evidence/stage1-semantics-integrity.log`.

The candidate prompt and translator are also byte-identical to their trusted
counterparts:

- `prompt.py`: SHA-256
  `4d99f80a460939bc03631f3a652d9af5d5a09da2fd8fab20205c9682f766a361`;
- `py2mpy.py`: SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

See `evidence/stage1-prompt-integrity.log` and
`evidence/stage1-translator-integrity.log`.

### Missing and inconsistent untrusted records

The following required candidate records are missing:

- `/candidate/run-input.json`;
- `/candidate/metrics.json`;
- `/candidate/codex-last.txt`;
- `/candidate/codex-output.log`.

No file named as a structured trace is present.  `spec.json` is a compiled KAST
artifact, not a generation trace.  It is also stale: it names an older
`function-correct` claim and has only two claims, whereas current `spec.k` has
five differently partitioned claims.  It was not used for parsing, building,
or proving the current source.  The absence report is
`evidence/stage1-required-generation-artifacts.log`; the source review,
including `spec.json`, is
`evidence/stage1-untrusted-and-trusted-source-review.log`.

The candidate also contains untrusted generated/cache material
(`__pycache__`, `kore-exec.tar.gz`).  None was copied into the proof workspace.
Only source artifacts and the supplied-semantics source tree were copied; the
scratch inventory is `evidence/stage1-scratch-copy.log`.

Stage 1 result: integrity of the proof sources and supplied semantics passes;
generation provenance is incomplete and `spec.json` is inconsistent.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and intended domain

The trusted prompt asks for `is_simple_power(x,n)` to return true exactly when
`x` is a power of `n`, written as `n**int = x`.  Its examples require:

`(1,4)->true`, `(2,2)->true`, `(8,2)->true`, `(3,2)->false`,
`(3,1)->false`, and `(5,3)->false`.

The trusted canonical implementation begins at power 1, special-cases `n == 1`,
and repeatedly multiplies by `n` while the power is less than `x`.  The examples
and the canonical loop strongly suggest positive integers, but neither trusted
file explicitly states that restriction.  The canonical itself is not a
total implementation over all integer pairs: for example, it does not
terminate for `x > 1` with `n` equal to 0 or -1, and it rejects negative `x`
without considering odd powers.  This makes positivity the most plausible
dataset domain, but it remains an undocumented assumption.

The submitted implementation uses the standard repeated-division algorithm:
it accepts `x == 1`, rejects `x < 1` and `n <= 1`, divides by `n` while the
remainder is zero, and returns whether the quotient reached 1.  This is
equivalent to the canonical algorithm for integer `x` and `n >= 1`; it is not
equivalent for all negative bases.

### Translator identity

I regenerated `solution.mpy` from the scratch copy of `solution.py` using the
trusted `/reference/py2mpy.py`.  The regenerated and submitted MPY files are
byte-identical, both with SHA-256
`6ff96ae7a85be104dce4df1ba85354cb8958580c725fce1f81b76f081dfa28fd`.
Commands and statuses are in
`evidence/stage2-regenerate-solution-mpy.log` and
`evidence/stage2-solution-mpy-byte-identity.log`.

### Independent differential testing

`evidence/differential_test.py` independently imports the trusted canonical
entry point and the scratch copy of the generated entry point.  It covers all
documented examples; zero and branch boundaries; all
`x in [-25,1000], n in [1,20]`; 2,000 seeded generated pairs; exact powers and
their neighbors; and terminating `x <= 1, n <= 0` cases.  There were 23,117
unique inputs and zero mismatches.  Exact command, scope, result, and exit 0:
`evidence/stage2-differential-test.log`.

Because the prompt does not explicitly exclude negative bases, I added
`evidence/differential_negative_bases.py`.  For `n <= -2`, the canonical loop
terminates: its magnitude grows, and every second product is positive.  On all
19,494 pairs with `x in [-25,1000], n in [-20,-2]`, the test found 26
mismatches, all positive even powers in the sampled range.  The first witness
is:

```text
is_simple_power(4, -2): canonical=True, generated=False
```

See `evidence/stage2-negative-base-differential.log`.  This is outside the
inferred positive-base domain but inside the literal unqualified “number”
wording and inside the candidate's formal all-integer partition.  It is the
principal intent-adequacy concern.

Stage 2 result: source-to-MPY fidelity passes; candidate-to-canonical fidelity
passes on the inferred positive domain and has a documented negative-base
discrepancy.

## 3. Clean proof reconstruction

All builds ran under K version `v7.1.337` from source in
`/tmp/audit-work/76-is-simple-power`.  Tool versions are recorded in
`evidence/stage3-tool-versions.log`.  No candidate-built definition, cache,
KORE archive, or `spec.json` was used.

### Concrete definition

I built the trusted supplied semantics with the LLVM backend:

```bash
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled
```

The command exited 0.  Compiler warnings concern non-exhaustive total
functions in unused list/float/string facilities; none is on this integer-only
program path.  See `evidence/stage3-build-concrete.log`.  A concrete execution
of the six documented examples through the fresh definition exited 0:
`evidence/stage3-concrete-examples.log`.

### Proof definition and program pinning

I built `verification.k` with the Haskell backend:

```bash
kompile verification.k --backend haskell \
  --main-module SIMPLE-POWER-VERIFICATION \
  --syntax-module SIMPLE-POWER-VERIFICATION \
  --output-definition verification-kompiled
```

This exited 0; see `evidence/stage3-build-proof.log`.  I independently expanded
both the submitted `solution.mpy` and `solutionModule` to KORE using the fresh
definition and diffed them.  `diff` exited 0 with no difference:
`evidence/stage3-solution-module-pinning.log`.

### Positive claims

Every positive target was run in its own auditor invocation:

| Claim | Invocation detail | Exit | Result evidence |
|---|---|---:|---|
| `loop-correct` | claim alone | 0 | `#Top`, `stage3-kprove-loop-correct.log` |
| `function-one` | claim alone | 0 | `#Top`, `stage3-kprove-function-one.log` |
| `function-below-one` | claim alone | 0 | `#Top`, `stage3-kprove-function-below-one.log` |
| `function-degenerate-base` | claim alone | 0 | `#Top`, `stage3-kprove-function-degenerate-base.log` |
| `function-positive-domain` | with independently proved `loop-correct` selected and trusted | 0 | `#Top`, `stage3-kprove-function-positive-domain.log` |

The positive-domain run uses `--trusted SIMPLE-POWER-SPEC.loop-correct`, but
only after the exact same loop claim independently closed under the fixed
semantics.  The independently successful loop proof is the connection theorem
for that use; it is not a candidate assertion accepted without checking.

Stage 3 result: pass.

## 4. Adequacy and real-program pinning

### Claims in plain language

- `loop-correct`: whenever execution is exactly at the generated repeated-
  division loop, followed by the generated final return and `#endcall`, with
  local bindings `x=X`, `n=N` and `N>1`, the call returns
  `positivePowerLoop(X,N)` and pops the exact frame.
- `function-one`: for every integer `N`, loading the submitted module and
  calling the entry point with `(1,N)` returns `simplePower(1,N)`, namely true.
- `function-below-one`: for `X<1` and every integer `N`, the call returns false.
- `function-degenerate-base`: for `X>1` and `N<=1`, the call returns false.
- `function-positive-domain`: for `X>1` and `N>1`, the call returns the
  repeated-division summary.

The four entry preconditions partition all K integer pairs.  None is
unsatisfiable.  The loop precondition is also satisfiable; `BASE=.Map`,
`X=8`, `N=2`, and the displayed concrete frame give a witness.

`evidence/claim_witnesses.py` instantiates every precondition and compares the
claimed summary with both Python implementations.  The exact output is
`evidence/stage4-claim-witnesses.log`.  Representative results are:

| Claim | Witness | Claimed | Generated | Canonical |
|---|---|---:|---:|---:|
| function-one | `(1,4)` | true | true | true |
| function-below-one | `(0,2)` | false | false | false |
| function-degenerate-base | `(4,-2)` | false | false | true |
| function-positive-domain | `(8,2)` | true | true | true |
| loop-correct | local `x=8,n=2` | true | true | true |

### Execution and result sensitivity

The `<k>` cell does not name an uninterpreted stand-in for the program.  It
expands to `#loadAll` of the exact submitted module, name lookup of
`is_simple_power`, argument evaluation, creation of a real function frame,
execution of the three guards, the exact while condition and assignment,
the exact final `Return`, and frame pop.  The loop claim matches the real loop
head and the exact continuation
`Return(powerResult) ~> #endcall`; it does not admit an arbitrary suffix.

The right-hand side is result-bearing and constrained.  `simplePower` has
disjoint equations, and `positivePowerLoop` is fixed by complementary
remainder guards.  The returned Boolean is neither fresh nor existential.
The Stage 6 mutation further demonstrates sensitivity.

The adequacy limitation is not an execution-pinning defect: at `(4,-2)` the K
claim correctly describes the generated program as returning false.  The
limitation is that the formal name `simplePower` does not denote the ordinary
integer-power predicate on that broader domain.

Stage 4 result: real-program pinning and result constraint pass; natural-intent
adequacy is qualified by the undocumented domain.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_rule_inventory.py` inventories every top-level configuration,
syntax declaration, context, rule, and claim in the assembled semantics, all
23 helper K files, `verification.k`, and `spec.k`.  Its complete annotated
output is `evidence/stage5-k-rule-inventory.tsv`:

```text
26 files
952 records
1 configuration
234 syntax declarations
5 contexts
707 rules
5 claims
```

Every supplied-semantics item is marked as an accepted supplied baseline only
after the recursive byte-identity check.  This does not bless candidate-local
rules: all 18 local declaration/rule records in `verification.k` have separate
assessments in the inventory.  Full numbered source for the used path is in
`evidence/stage5-used-path-semantics.log`.

There are no `[simplification]` rules and no `[functional]` declarations in
the reviewed sources.  The special-declaration inventory
`evidence/stage5-special-declarations.log` lists every `total`, `owise`,
priority, symbol, and no-evaluator occurrence.  The 25 opaque/symbol
declarations belong to supplied float, sort, and MD5 facilities.  None is
reachable from this program or any proof postcondition.

### Construct-to-semantics map

| Submitted construct | Declaration | Executing rules |
|---|---|---|
| `Module`, statement lists | `syntax.k:56,61` | `core.k:124-127` (`#loadAll`, sequencing) |
| `FuncDef`, `Params` | `syntax.k:53-60` | `functions.k:14-16` (closure binding) |
| `Call`, `Name` | `syntax.k:12,28` | `core.k:130-154`; `call.k:20-21,69-75` |
| `Int`, `Bool` | `syntax.k:9,11` | `core.k:194-195` |
| `If` | `syntax.k:49` with strict condition | `controls.k:51-54` |
| `While` | `syntax.k:46` | `controls.k:65-67,77-85` |
| `Assign(Name,...)` | `syntax.k:41` with strict RHS | `controls.k:9-18` |
| `Return` | `syntax.k:50` with strict expression | `functions.k:78-90` |
| `BinOp("%",...)`, `BinOp("//",...)` | `syntax.k:15`, left-to-right `seqstrict` | `operators.k:12`; `int.k:15-20` |
| integer comparisons | `syntax.k:30-32` and comparison contexts | `operators.k:15-17`; `int.k:22-27` |

The configuration cells are `<k>`, `<env>`, `<scopes>`, `<scopeLoc>`,
`<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and `<exit-code>`.
Function entry updates environment, scopes, scope allocation, and stack;
return/pop restores those cells and emits the value.  This program performs no
heap allocation, output, or exception-producing operation.  The loop claim
matches every cell that its execution changes (`env`, `scopes`, `scopeLoc`,
`stack`, and `ret`); omitted heap/exception/exit cells are framed and untouched
on the used path.

Evaluation order is fixed by `seqstrict` for binary operators, explicit
comparison contexts, strict guards/returns/assignment RHSs, the left-to-right
argument loop, and the concrete call-frame rules.  There is one deterministic
binding for `is_simple_power` after `#loadAll`.  The candidate adds no call
priority or interception rule.

### Candidate-local extension decisions

1. `simplePower` is a definitional summary, not an operational bridge.  Its
   four guards (`X==1`; `X<1`; `X>1,N<=1`; `X>1,N>1`) are satisfiable,
   pairwise disjoint, and exhaustive over integer pairs.  Their right sides
   agree with the generated program.  The third equation is not a valid
   definition of mathematical power for all negative bases; this is the
   Stage 2/4 intent gap, not a false claim about program execution.
2. `positivePowerLoop` is a result-bearing definitional summary.  When
   `pyMod(X,N)==0`, the concrete body computes Python floor division.  Under
   the guard, `(X-pyMod(X,N))/Int N` equals `X/Int N`, exactly the recursive
   equation.  When the remainder is nonzero, the concrete while exits and
   returns `X==1`, exactly the second equation.  The guards are complementary
   whenever `pyMod` is defined.  On the used positive entry domain,
   `X/N < X`, so recursion descends.  The helper claim's broader `N>1`
   domain also soundly models nontermination such as `X=0`: both concrete loop
   and recursive summary fail to reach a result, which is permitted by partial
   correctness.
3. The six macro declarations and six expansion rules are syntax-only.  Their
   expanded module is independently KORE-identical to `solution.mpy`.  They do
   not rewrite a running program state.
4. `loop-correct` is an auxiliary reachability theorem/circularity over the
   exact loop invocation and continuation.  It was proved without importing an
   operational bridge, then used for the positive entry claim.  Its state
   footprint and binding context are contained in the proved match.

There is no local opaque value, no local `total` or `functional` annotation,
no local priority/`owise` rule, no simplification rule, and no operational
bridge.  Therefore no opposite interpretation or bridge-continuation witness
is applicable.  I make no unsound-rule allegation and hence no false-conclusion
witness is required.  The narrower evidence gap is the lack of a formal
exponentiation theorem connecting `simplePower` to the English predicate.

Stage 5 result: Gate A static soundness passes.

## 6. Fresh non-vacuity test

There is no submitted `spec-vacuity.k`.  I wrote a fresh mutation,
`evidence/spec-vacuity.k`, whose satisfiable concrete witness calls the exact
submitted program at `(x,n)=(1,4)` but demands the false return value.

The mutation was copied to scratch and first run with `--dry-run`.  Parsing and
KORE generation exited 0; see `evidence/stage6-vacuity-dry-run.log`.  The full
proof then exited 1 with `WarnStuckClaimState`.  Its residual contains:

```text
<k>
  true ~> .K
</k>
```

which cannot unify with the demanded `false`.  The failure is therefore the
expected unmet result obligation, not a parser error, missing import, timeout,
or unrelated crash.  Full output is
`evidence/stage6-vacuity-proof.log`.

Stage 6 result: pass.

## 7. Proven versus assumed accounting

### What is machine-checked

Conditional on the supplied MPY semantics and K backend, the successful
reachability claims establish this partial-correctness characterization of the
actual submitted module for all K integer arguments:

- `x == 1` returns true;
- `x < 1` returns false;
- `x > 1` and `n <= 1` returns false;
- `x > 1` and `n > 1` returns true exactly when repeated exact division by
  `n` reaches 1 before encountering a nonzero remainder.

The machine proof also establishes the exact loop summary for `N>1` in the
displayed function-frame context.  It does not prove total termination.

### Trust ledger

| Boundary | Influence | Assessment/evidence |
|---|---|---|
| Supplied MPY semantics | All execution, state, calls, and returns | Authorized fixed semantics; candidate tree is byte-identical. Used integer/call/control path was statically audited. |
| K frontend, Haskell/LLVM backends, SMT/builtin Int/Bool/Map/List theory | Proof closure and concrete execution | Standard toolchain trust boundary; version and actual outputs recorded. |
| Trusted `py2mpy.py` | Python-to-MPY identity | Trusted mounted translator; regenerated MPY is byte-identical. |
| `solutionModule` macros | Program text loaded by claims | No semantic abstraction; expanded-KORE identity checked independently. |
| `positivePowerLoop` equations | Final positive-domain Boolean | Fully equational, non-opaque, and connected to exact loop execution by the independently proved loop claim. |
| Loop circularity | Inductive reasoning over repeated division | Exact context and cells; independently closed before being trusted in the entry proof. |
| Meaning of “simple power” | Natural-language correctness conclusion | Informal ordinary-mathematics bridge on positive integers, finitely supported by the 23,117-case zero-mismatch differential; not itself a K exponentiation theorem. |
| Positive input-domain inference | Whether the bridge covers the prompt | Concerning: examples/canonical suggest it, but prompt does not state it; negative-base witness shows the unrestricted reading is false. |

The opaque float/sort/MD5 symbols and the compiler's unused-path totality
warnings have no control, state, or result influence on these claims.

Differential tests support only the stated finite bridge.  They do not replace
the K execution proof, and the K proof does not erase the negative-base
discrepancy.  Candidate prose, stale `spec.json`, caches, and missing generation
records establish nothing.

### Gate and verdict rationale

- Real-program soundness: pass.
- Real-program pinning and result constraint: pass.
- Non-vacuity: pass.
- Positive-integer intent bridge: supported but informal.
- Unqualified all-number intent bridge: not established; concrete canonical
  counterexample `(4,-2)`.
- Reproducibility of proof evidence: pass.
- Generation provenance: incomplete.

The proof is therefore legitimate as a partial-correctness proof of the real
generated program and of the ordinary simple-power result on the inferred
positive-integer domain.  The unstated-domain discrepancy and informal
summary-to-exponent bridge prevent an unqualified `PASS`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
