# Independent adversarial review: 75-is-multiply-prime

This audit used only fresh builds below
`/tmp/audit-work/75-is-multiply-prime` and reviewer evidence below
`/audit-output/evidence`. Candidate-provided build products, prose, and prior
success reports were not trusted. The required Kit path was `using-kit`,
followed by `validating-proof` and, because the mode is
`GENERATED_SEMANTICS`, `writing-semantics`.

## 1. Input and provenance integrity

The declared record layout is `legacy-selected-stage1`; the declared semantics
mode is `GENERATED_SEMANTICS`. I read `/audit-input.json` first and then
inspected:

- `/audit-campaign-lock.json`, `/run.json`, `/task.json`, and
  `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the present legacy records `legacy-metrics.json` and
  `legacy-run-input.json`; and
- the sole structured trace,
  `/generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T05-41-47-019f896a-d221-75d1-9fea-e0f95da354bd.jsonl`.

`runtime-metrics.json` is absent, which is permitted for this legacy-selected
layout. `usage.json` is present and was inspected. The generation records claim
`KPROVE_PASSED`; that claim was not used as proof evidence.

The campaign-lock object exactly equals the campaign block in
`/audit-input.json`. Its independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
which matches the recorded value. Every launcher-declared container path is
present with the required real-file or real-directory type. All required
records are regular files, the candidate and trace trees contain no symlinks or
unsupported entries, and all 127 trace lines parse as JSON.

All recorded leaf-file hashes reproduce, including the run/task/result and
invocation records, generation prompt/output/last/metrics/usage, canonical,
trusted prompt, and trusted translator. The candidate prompt and translator
are byte-identical to `/reference/prompt.py` and `/reference/py2mpy.py`.
The task-manifest fields equal the embedded manifest; the embedded manifest's
launcher-added `config` also agrees with both top-level config fields.

For independent tree binding, the pipeline tree hash of `/candidate` is
`3e3adf6ec1d061b5091ee3021b87196af35fa5805041369f5d54c67a274b7c2b`,
exactly the retained-workspace hash in the invocation/result records. The
pipeline tree hash of the structured trace is
`e26962f545b169affac16c7174a2e9da2de4d89212516299928a6885cde4d717`,
exactly `usage.json`'s source-trace hash; its only leaf also matches the
recorded leaf hash
`27be93a4e71b990c0deadc304814cc1770ca101a3ef3283ecbf78d06633f7b04`.
`audit-input.json` additionally records launcher-specific directory digests
`9c51...` and `492c...` without declaring that digest scheme. I did not guess
that scheme; the independently reproducible pipeline hashes and all leaf hashes
fully bind the mounted content.

The generated-semantics boundary is intact:
`/reference/reference-semantics` does not exist, no baseline was sought or
inferred, and `/candidate/reference-semantics` is also absent. There is no
infrastructure breach.

Evidence:

- `evidence/stage1_integrity.py`
- `evidence/stage1_integrity.log` — command exit 0, `failures=0`

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For an integer `a < 100`, return true exactly when there exist three prime
numbers `p`, `q`, and `r` (repetition allowed) such that `p*q*r = a`; otherwise
return false. The documented example is `a = 30`, with `30 = 2*3*5`.

The trusted canonical implementation (`/reference/canonical.py:14-27`) tests
primality and searches all triples of primes from 2 through 100. The submitted
implementation (`/candidate/solution.py:1-26`) instead compares `a` against the
22 possible products below 100. This is a different but valid algorithm.

### Translator identity

Exact command, run from the scratch working copy:

```sh
python3 /reference/py2mpy.py /candidate/solution.py > regenerated-solution.mpy
cmp --silent regenerated-solution.mpy /candidate/solution.mpy
sha256sum regenerated-solution.mpy /candidate/solution.mpy
```

Exit status was 0. Both files hash to
`2ed20f37c9f9cc534ea932248a2599788f3e6de80cc7303669d627aef0439709`;
submitted `solution.mpy` is therefore byte-identical to trusted regeneration.
See `evidence/translation_identity.log`.

### Independent differential test

`evidence/differential_test.py` independently imports the trusted canonical and
candidate entry points. It also implements a separate primality/product oracle
without reusing K equations. Its input set contains:

- the documented example and numeric empty/boundary cases;
- the predecessor, value, and successor around every true comparison branch;
- every integer from -250 through 100; and
- 40 deterministic generated integers from -1,000,000,000 through 99
  (seed `750075`).

Exact command:

```sh
python3 /audit-output/evidence/differential_test.py
```

It tested 391 distinct values, exited 0, and reported zero
canonical/candidate mismatches and zero independent-oracle mismatches. The
script and `evidence/differential_test.log` preserve the complete input
construction, seed, generated sample, and result.

Program fidelity passes.

## 3. Clean proof reconstruction

The scratch source copy initially contained no `*-kompiled` directory. The
installed `kompile` and `kprove` both report K v7.1.293. I built an LLVM
concrete definition and a separate Haskell proof definition from candidate
source:

```sh
kompile semantic.k \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled

kompile definition.k \
  --backend haskell \
  --main-module DEFINITION \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-kompiled
```

Both commands exited 0. `spec.k` contains exactly one positive target claim. I
ran the complete spec module:

```sh
kprove spec.k \
  --definition proof-kompiled \
  --spec-module SPEC
```

The command exited 0 and printed exactly `#Top`. The command sequence, tool
versions, empty pre-build cache scan, and output are in
`evidence/stage3_rebuild.sh` and `evidence/stage3_rebuild.log`.

For generated-semantics execution, `evidence/stage3_semantics_compare.py` ran
the following command shape for each of
`[-7, 0, 7, 8, 10, 29, 30, 31, 98, 99, 100]`:

```sh
krun solution.mpy --definition concrete-kompiled -cARG=<value>
```

Every `krun` exited 0 with consumed `<k>`, empty `<env>`, and a Boolean result.
All 11 results matched both Python implementations; mismatch count was zero.
The normal case 30 returned true; 10 returned false; lower, first-true,
last-true, and upper-bound cases were included. See
`evidence/stage3_semantics_compare.log`.

Clean reconstruction passes.

## 4. Adequacy and real-program pinning

### Formal claim in plain language

The sole claim (`/candidate/spec.k:6-13`) starts with:

- an arbitrary K integer `A` satisfying `A < 100`;
- the exact `solutionProgram` term in `<k>`;
- `A` in `<arg>`;
- an empty local environment; and
- `noResult`.

If the modeled execution terminates, the destination requires empty `<k>`,
preserves `A`, restores an empty environment, and fixes the result to
`Bool(isThreePrimeProductBelow100(A))`. There is no right-only free result
variable, implication-only result condition, helper/loop claim, or omitted
result constraint.

### Mechanical program pinning

Trusted regeneration pins `solution.py` to `solution.mpy`. Separately,
`evidence/constructor_compare.py` extracts the RHS of the only
`solutionProgram` rule and compares constructor tokens against
`solution.mpy`. Both contain 416 constructor tokens and are identical. The
command

```sh
python3 /audit-output/evidence/constructor_compare.py
```

exited 0; see `evidence/constructor_compare.log`. Thus the claim's function
binding, parameter, return body, all 22 comparisons, ordering, and constants
are the submitted translated program, modulo whitespace only.

The semantics then expands that constant and executes it. It does not replace
the body with the postcondition helper: `semantic.k` does not import
`verification.k`, and no semantic rule mentions
`isThreePrimeProductBelow100`.

### Satisfiability and concrete substitution

`A = 30` satisfies `A < 100`. Substitution makes the claimed predicate true
because one disjunct is `30 = 2*3*5`; fresh K execution, the candidate Python,
and the canonical Python all returned true. As a distinct outcome, `A = 10`
satisfies the same precondition and all three returned false.

### Body sensitivity

The reviewer mutation in
`evidence/solution-program-body-mutation.k` changes the first comparison in
the program term actually executed by the claim from `a == 8` to `a == 9`.
This is not an external-source-only mutation. A fresh Haskell build succeeded,
but the unchanged target claim exited 1 with `WarnStuckClaimState`; the
residual explicitly contrasted the `8` and `9` disjunctions. The wrapper
verified the expected failure and exited 0. See
`evidence/stage4_body_sensitivity.sh` and
`evidence/stage4_body_sensitivity.log`.

Adequacy and real-program pinning pass.

## 5. Rule-by-rule static soundness review

`evidence/rule_inventory.md` is the exhaustive local inventory.
`evidence/static_rule_scan.log` preserves the declaration/rule scan. It covers
every syntax production, configuration, function declaration, function
equation, operational rule, simplification rule, and claim in `semantic.k`,
`solution-program.k`, `verification.k`, `spec.k`, and `definition.k`.

### Construct coverage

Every constructor in `solution.mpy` has syntax and behavior:

| Submitted construct | Declaration | Behavior |
|---|---|---|
| `Module`, sole `FuncDef`, unary `Params` | `semantic.k:19-22` | module-launch rule at lines 64-66 |
| `Return` | `semantic.k:21` | return rule at lines 68-70 |
| `BoolOp("or", ...)` and expression list | `semantic.k:15,26` | `evalBool` delegation and `evalOr` at lines 50,52-54 |
| `Compare(Name("a"), CmpOp("==", Int(I)))` | `semantic.k:17,23-24,27-28` | exact integer equality equation at lines 46-49 |

The extra `Bool` literal syntax/equation is unused and sound. Missing behavior
for unused expression forms is not a defect in generated-semantics mode.

### Functions and equations

The LHS constructors of the three `evalBool` equations are disjoint. The empty
and nonempty `evalOr` equations are disjoint and exhaustive over list shape;
the recursive call strictly shortens the list. The exact singleton environment
required by integer-name comparison is exactly the environment created for
this submitted unary program. `orElseBool` gives left-to-right short-circuiting.

`evidence/stage5_short_circuit.sh` independently confirms control sensitivity:
a true Boolean head skips a deliberately unsupported `Int(123)` tail and
returns true; a false head reaches that tail and exits 113 with the residual
`evalBool(Int(123), ...)`. The semantics therefore stops visibly at an
unsupported construct instead of fabricating a result.

The nullary `solutionProgram` function has one unconditional, terminating
equation. It is a definitional AST constant, not an execution bridge.
Constructor comparison establishes its exact value.

The fresh `isThreePrimeProductBelow100(Int)` function has one unconditional,
terminating equation and is therefore covered for every K integer. Its
`[simplification]` attribute changes rewriting, not truth; the equation defines
the fresh predicate and does not preempt program execution.

There are no local `[total]` or `[functional]` declarations, opaque symbols,
priority rules, overlapping guarded equations, or other simplification rules.

### Operational rules, control, and cells

There are exactly two ordinary operational rules:

1. The module-launch rule accepts an exact one-function, one-parameter module
   in an exact `<k>` context, reads `<arg>`, requires empty `<env>`, and binds
   the real formal before moving to `execute(BODY)`. It has no continuation
   wildcard. The omitted result cell is framed and preserved.
2. The return rule accepts exact `execute(Return(E))`, reads the local map,
   computes the Boolean through the audited equations, empties the local map,
   and writes the result. It has no continuation to discard; `<arg>` is framed
   and preserved.

This is a small big-step entry-point harness, not a model of arbitrary Python
module loading. Its complete match domains contain the submitted term and
preserve all four modeled cells. The submitted expression has no mutation,
allocation, output, exception-producing operation, or non-Boolean operand.
Python and K integers are unbounded in the relevant model, so equality has no
overflow discrepancy.

### Prime-product characterization

`evidence/spec_characterization.py` parses all 22 factor products from the K
helper and independently enumerates nondecreasing prime triples. It reports the
same 22 unique values and exits 0; see
`evidence/spec_characterization.log`.

The exhaustive ordinary-mathematics argument is also short. Sort the three
primes as `p <= q <= r`. Since `5^3 > 100`, `p` is 2 or 3. For `p = 2`,
`q` can only be 2, 3, 5, or 7; bounding `r` in each case yields respectively
9, 5, 2, and 1 values. For `p = 3`, `q` can only be 3 or 5, yielding 4 and 1
values. These are exactly the 22 disjuncts. Every `A < 8`, including every
negative integer, is false because three primes have product at least 8.
Thus the finite helper is equivalent to the source property over the complete
integer domain `A < 100`, not merely over tested examples.

No local rule is unsound on its match domain, so there is no unsoundness claim
requiring a false-conclusion witness.

Static soundness passes.

## 6. Fresh non-vacuity test

I did not rely on a candidate mutation (none is present). The fresh
`evidence/spec-vacuity.k` keeps the real program and cells, selects the
satisfiable original-domain witness `A = 30`, and deliberately changes the
result obligation to `Bool(false)`.

Commands:

```sh
kprove spec-vacuity.k \
  --definition proof-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run

kprove spec-vacuity.k \
  --definition proof-kompiled \
  --spec-module SPEC-VACUITY
```

The dry run exited 0 and emitted the backend invocation, establishing that the
mutation built and parsed. The proof exited 1 with
`WarnStuckClaimState`. Its residual is the expected unmet obligation:
`<arg> 30 </arg>` and `<result> Bool(true) </result>` cannot unify with the
mutated false destination. The reviewer wrapper asserted the nonzero proof
status and expected residual, then exited 0.

Evidence:

- `evidence/spec-vacuity.k`
- `evidence/stage6_nonvacuity.sh`
- `evidence/stage6_nonvacuity.log`

Non-vacuity passes.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the audited generated semantics and imported K builtins, for every
mathematical integer `A < 100`, partial correctness of the exact regenerated
program holds: if its modeled entry-point execution terminates, it consumes the
computation, restores the empty local environment, preserves the argument, and
returns true exactly for

```text
8, 12, 18, 20, 27, 28, 30, 42, 44, 45, 50,
52, 63, 66, 68, 70, 75, 76, 78, 92, 98, 99
```

The rule audit and exhaustive prime-triple characterization establish that
this set is exactly the products of three primes below 100. The claim covers
all negative integers as well as 0 through 99; it is not a finite list of
input preconditions or a bounded unrolling of an unrestricted source domain.
The source contract itself supplies the `< 100` bound.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K v7.1.293 compiler, LLVM/Haskell backends, and `kprove` | Parsing, concrete execution, and proof checking | Necessary low-level toolchain trust; fresh independent builds avoid candidate caches. |
| Imported K `INT`, `BOOL`, `MAP`, `STRING`, and list domains | Integer equality/multiplication/order, Boolean strict and short-circuit operators, singleton maps, constructor lists | Acceptable standard primitives. No task-specific builtin or opaque oracle is used. |
| Trusted `/reference/py2mpy.py` | Source-AST-to-constructor bridge | Launcher hash verified; candidate copy identical; trusted regeneration is byte-identical. |
| Manual `solutionProgram` embedding | Which program term the claim executes | Mechanically checked at all 416 constructor tokens. The candidate's digest check alone would not prove this, but the immutable submitted artifact is independently pinned. |
| Generated entry-point semantics | Bridge from the translated module to invocation behavior | Audited rule by rule over every used construct and cell; concrete boundary tests and body sensitivity support it. The rules contain no task result. |
| Finite predicate-to-natural-contract bridge | Meaning of “product of three primes” | Established by exhaustive finite case analysis and an independent enumerator. It is not assumed from the helper's name. |
| Trusted canonical and CPython executions | Differential evidence only | 391 zero-mismatch cases support fidelity but are not substituted for the K proof or the universal mathematical argument. |
| Termination | Outside a pure partial-correctness statement | The audited program is a finite expression and all local recursion descends, but the verdict does not depend on overstating reachability logic as a separate termination theorem. |

The formal input sort is `Int`. This matches the intended domain: prime
factorization is an integer property, and the trusted canonical searches
integer primes. Non-integer Python objects are outside the HumanEval contract;
there is no added lower bound or finite input enumeration in the claim.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C (trust and
evidence auditability) all pass. The proof is result-constraining, sensitive to
the real body, sound under every local rule, non-vacuous, and covers the
material source-contract domain.

VERDICT: PASS
LEGITIMACY: LEGIT
