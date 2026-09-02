# Independent adversarial review: 97-multiply

## Headline

The candidate contains a freshly reproducible, non-vacuous
partial-correctness proof of the exact submitted `solution.mpy` under its
generated semantics. The proof does not use an answer oracle, free result,
substituted program, or unsound local rule.

It does **not** establish that the submitted implementation agrees with the
trusted HumanEval/97 behavior over the full intended integer domain. The
candidate first replaces each negative argument by its absolute value; the
trusted canonical implementation applies Python `% 10` to the original
argument. A concrete satisfying witness is `(-1, 1)`: the candidate, rebuilt K
semantics, and formal postcondition give `1`, while the trusted canonical gives
`9`. The independent differential found 338 mismatches among 882 documented,
boundary, grid, large, and deterministic generated inputs.

Accordingly, this is a legitimate proof about the real submitted program but
has a material implementation-to-intent adequacy concern. It is not a false K
theorem about that program, so the appropriate decision-boundary pairing is
`CONCERNS / LEGIT`, not `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `GENERATED_SEMANTICS`, and
`/reference/reference-semantics` is absent. This is the required mount state;
there is no infrastructure contradiction and no hidden or inferred reference
semantics was used. See
`/audit-output/evidence/01_stage1_provenance.log`.

### Required artifacts and types

The following required candidate artifacts all exist as ordinary files:

- `run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and the single structured JSONL trace;
- `prompt.py`, `py2mpy.py`, `solution.py`, and `solution.mpy`; and
- `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`.

No required artifact is missing, mistyped, or symlinked. There are no
candidate helper K files beyond the three listed K sources.

The candidate has additional compiled/build evidence:
`semantic-kompiled/`, `verification-kompiled/`, `kprove.out`,
`__pycache__/`, and generation logs/traces. These extras are regular entries,
were treated solely as untrusted evidence, and were neither copied into nor
used by the clean proof reconstruction. The complete entry inventory is in
`01_stage1_provenance.log`.

The candidate prompt is byte-identical to `/reference/prompt.py`, with SHA-256
`cadfab7a20c335c251fcd403e9c144183ae36eee01a205783c534184aa1d3004`.
The candidate translator is byte-identical to `/reference/py2mpy.py`, with
SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
These hashes also agree with the untrusted `run-input.json` claims.

### Untrusted run records

The untrusted metrics claim a 527-second, non-timeout run with exit 0.
`codex-last.txt`, `codex-output.log`, and the structured trace claim six
concrete successes and `#Top`; the logs also show earlier compiler errors
while the candidate was being developed. None of these claims was used as
proof evidence. The reviewer parsed all 172 structured trace records and
recorded its event census and tool-call claims in
`01_stage1_provenance.log`.

The first reviewer provenance attempt failed only because `jq` was not
installed. That bounded failed command is preserved at
`/audit-output/evidence/01_stage1_provenance_attempt1.log`; the corrected
standard-library JSON reader completed with exit 0. This was not a trusted
mount breach or candidate failure.

All source artifacts required for execution were copied to
`/tmp/audit-work/97-multiply/candidate-source`, and trusted inputs to
`/tmp/audit-work/97-multiply/trusted`. The exact copy command and inventory
are in `/audit-output/evidence/00_copy_sources.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

`/reference/prompt.py` requires `multiply(a, b)` for valid integer inputs to
return the product of their unit digits. Its examples are:

- `(148, 412) -> 16`;
- `(19, 28) -> 72`;
- `(2020, 1851) -> 0`; and
- `(14, -15) -> 20`.

The trusted `/reference/canonical.py` fixes the executable meaning as:

```python
abs(a % 10) * abs(b % 10)
```

Because Python modulo with positive divisor has a nonnegative remainder,
negative inputs that are not multiples of ten generally distinguish this
from `(abs(a) % 10) * (abs(b) % 10)`.

### Submitted implementation and translation

`/candidate/solution.py` conditionally replaces each negative argument by its
negation, then returns `(a % 10) * (b % 10)`. It is defined for every pair of
Python integers and exercises four sign branches.

The trusted translator regenerated `solution.mpy` from the scratch-copied
`solution.py`. `cmp` exited 0; both files have SHA-256
`d860df715e34cbe117902f177b536f6f8a92baf503ead76ad17158df9e1556a6`.
The exact command, status, and hashes are in
`/audit-output/evidence/02_solution_mpy_regeneration.log`.

### Independent differential

Reviewer-authored
`/audit-output/evidence/differential_test.py` independently loads the
scratch copy of the trusted canonical entry point and the submitted entry
point. It tested:

- all four documented examples;
- the complete `{-1,0,1} x {-1,0,1}` sign/branch boundary;
- a 25-by-25 sign/unit-digit grid around negative and positive multiples of
  ten;
- four unbounded-integer representatives; and
- 250 deterministic generated integer pairs.

There is no meaningful “empty” integer input; this is explicitly recorded.
The de-duplicated total is 882. Inputs and every result are preserved in
`/audit-output/evidence/differential_inputs.json` and
`/audit-output/evidence/differential_results.json`.

The script exited 1 after reporting 338 mismatches, as designed. The exact
command and bounded mismatch output are in
`/audit-output/evidence/03_differential_test.log`. Small witnesses include:

| Input | Trusted canonical | Candidate |
|---|---:|---:|
| `(-1, 1)` | 9 | 1 |
| `(1, -1)` | 9 | 1 |
| `(-1, -1)` | 81 | 1 |
| `(-14, 15)` | 30 | 20 |

All prompt examples pass, including `(14,-15)`, because `-15 % 10 == 5`;
that example does not expose the general negative-modulo disagreement.

This is a material implementation-to-intent divergence on valid documented
input types.

## 3. Clean proof reconstruction

No candidate-provided compiled directory or cache was copied or reused. The
scratch tree contained only copied source before compilation. Source hashes
are recorded in `/audit-output/evidence/10_static_source_census.log`.

### Concrete semantics definition

From `/tmp/audit-work/97-multiply/candidate-source`:

```text
kompile semantic.k --backend haskell --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition semantic-kompiled
```

This exited 0. See
`/audit-output/evidence/04_semantic_kompile.log`.

### Proof definition

```text
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled
```

This exited 0. See
`/audit-output/evidence/05_verification_kompile.log`.

### Every positive target claim

The static census found exactly one claim in `spec.k` and no helper claims.
It was run independently:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

The command printed exactly `#Top` and exited 0. See
`/audit-output/evidence/06_positive_spec_kprove.log`.

### Fresh concrete generated-semantics execution

Reviewer-authored
`/audit-output/evidence/generated_semantics_test.py` ran the byte-identical
`solution.mpy` against the rebuilt definition for 17 documented, zero,
four-quadrant sign-boundary, negative-modulo-distinguishing, and very large
integer inputs. It separately executed both Python implementations.

Every `krun` invocation exited 0, and K agreed with the submitted
`solution.py` in all 17 cases. It also reproduced the canonical disagreement:
for `(-1,1)`, K and candidate Python returned 1 while canonical returned 9.
The script exited 0; exact nested commands and results are in
`/audit-output/evidence/07_generated_semantics_concrete.log`, with complete
K output in
`/audit-output/evidence/generated_semantics_results.json`.

Thus the clean dynamic reconstruction succeeds and faithfully tracks the
submitted implementation on the tested normal and boundary cases.

## 4. Adequacy and real-program pinning

### Plain-language entry claim

The sole claim has no `requires` clause. Sort inference through `#invoke`
makes `A` and `B` arbitrary mathematical integers. Its starting state has:

- `<k>` equal to `multiplyProgram` followed by
  `#invoke("multiply", A, B)`;
- empty environment and function maps; and
- `noResult`.

It requires complete consumption of `<k>` and the following final state:

- parameters `"a"` and `"b"` contain `absInt(A)` and `absInt(B)`;
- the function map contains the exact loaded `multiplyBody`; and
- result is `unitDigit(A) *Int unitDigit(B)`, where the only `unitDigit`
  equation is `absInt(I) %Int 10`.

There is no existential or otherwise free destination value. The result,
environment, function map, and computation are all constrained. There are no
loop or helper claims.

### Exact submitted program

`multiplyProgram` and `multiplyBody` are closed ordinary rewrite
abbreviations. They expand to the `Module`, `FuncDef`, two `If` statements,
assignments, comparisons, unary minuses, modulo operations, multiplication,
and return that appear in the byte-identical submitted `solution.mpy`. They
do not rewrite to a result.

To remove reliance on those abbreviations, the reviewer created
`/audit-output/evidence/spec-literal-program.k`, whose entry and final
function map contain the full submitted AST literally. It does not use
`multiplyProgram` or `multiplyBody`. This independent claim printed `#Top`
and exited 0:

```text
kprove /audit-output/evidence/spec-literal-program.k --definition verification-kompiled --spec-module AUDIT-LITERAL-PROGRAM-SPEC -I /tmp/audit-work/97-multiply/candidate-source
```

See `/audit-output/evidence/08_literal_program_kprove.log`.
This demonstrates body sensitivity and real-program pinning without a
result-bearing program abstraction.

### Satisfying ground states

Because there is no explicit precondition beyond integer sorts, every tested
integer pair is satisfying. Reviewer ground substitutions are preserved in
`/audit-output/evidence/claim_ground_witness.py` and
`/audit-output/evidence/09_claim_ground_witness.log`:

| `A,B` | Claimed result | Candidate Python | Canonical Python |
|---|---:|---:|---:|
| `148,412` | 16 | 16 | 16 |
| `-1,1` | 1 | 1 | 9 |
| `-14,15` | 20 | 20 | 30 |

The claim is adequate for the submitted algorithm but not for universal
equivalence to the trusted task implementation.

## 5. Rule-by-rule static soundness review

The exhaustive declaration, attribute, opaque-symbol, rule, construct
coverage, and per-rule decision record is
`/audit-output/evidence/rule_inventory.md`. The mechanical source census is
`/audit-output/evidence/10_static_source_census.log`.

### Inventory summary

`semantic.k` defines:

- AST syntax for `Module`, statement lists, exact two-parameter `Params`,
  `FuncDef`, `If`, `Assign`, `Return`, `Int`, `Name`, `UnaryOp`, `BinOp`,
  `Compare`, and `CmpOp`;
- internal data/computation syntax for `function`, `noResult`, `#invoke`,
  `#if`, `#assign`, `#return`, `#lessThan`, `#unaryMinus`, `#modulo`, and
  `#multiply`;
- `Int` and `Bool` as results and evaluated expressions; and
- one configuration with `<k>`, `<env>`, `<functions>`, and `<result>`.

There are 22 local semantic rules, exhaustively identified as S1-S22 in the
inventory:

- S1-S3 schedule the module and ordered statement list;
- S4 loads the exact function and S5 invokes the stored body with exact
  bindings;
- S6-S15 implement literals, lookup, negation, modulo, multiplication, and
  less-than through fully connected dispatch/computation pairs;
- S16-S18 implement conditionals;
- S19-S20 implement name assignment; and
- S21-S22 evaluate and perform entry-function return.

`verification.k` has exactly three rules:

- V1 expands the closed `multiplyBody` to the exact submitted statements;
- V2 expands the closed `multiplyProgram` to the exact module/function AST;
  and
- V3 defines total `unitDigit(I)` as `absInt(I) %Int 10`.

V3 is the sole local `[function,total]` declaration. Its unguarded,
nonrecursive equation has complete `Int` coverage and no overlap. There are
no `[functional]`, `[simplification]`, `[concrete]`, priority, `owise`, or
`anywhere` declarations; no local simplification or priority rules; no
auxiliary claims; and no fresh or existential answer symbol.

### Control, state, and arithmetic assessment

Statement scheduling is left-to-right. `#if` evaluates only its condition
before selecting a branch. Assignment evaluates its expression before
updating exactly one environment binding. Return evaluates its expression,
sets the result, and discards the remaining body, which is correct for the
only modeled entry call. Function lookup selects the name and exact body
stored by the preceding definition.

The two-operand strict declarations do not promise Python left-to-right
ordering, but every operand reached in this program is a pure name or literal
expression. Consequently, no result, environment, control, exception, or
other modeled cell can distinguish the possible evaluation orders.

`%Int` has a nonzero-divisor guard; every reached divisor is literal 10.
Moreover, the submitted program makes each operand nonnegative before
modulo, so K and Python remainder agree on all reached executions. Missing
zero-division and nested-call semantics covers unused constructs only; no
used construct is silently assigned a fabricated value.

The closed V1/V2 match domains cannot accept a broader body or binding.
The literal-AST proof independently eliminates them. `function(...)` and
`noResult` are opaque data/sentinel constructors, but neither bears or
generates the returned integer. Every internal operational symbol is fully
connected to builtin mathematics or an explicit state transition.

No local rule is judged unsound, so no false-rule witness is asserted. The
narrow call/return model would not be a reusable Python semantics for nested
calls, but nested calls are absent from the submitted syntax and intended
entry configurations. The concrete false conclusion is instead the
candidate-to-canonical bridge: at `(-1,1)`, the sound candidate theorem gives
1 and canonical gives 9.

## 6. Fresh non-vacuity test

There is no candidate `spec-vacuity.k`; none was trusted.

The reviewer created
`/audit-output/evidence/spec-vacuity-audit.k`, changing only the final
result to:

```text
(unitDigit(A) *Int unitDigit(B)) +Int 1
```

The satisfying witness `A=148, B=412` has actual/formal result 16, while the
mutation requires 17.

First, the exact mutated artifact successfully parsed and generated KORE:

```text
kprove /audit-output/evidence/spec-vacuity-audit.k --definition verification-kompiled --spec-module AUDIT-SPEC-VACUITY -I /tmp/audit-work/97-multiply/candidate-source --dry-run
```

This exited 0; see
`/audit-output/evidence/11_vacuity_mutation_dry_run.log`.

The actual mutated proof then exited 1 with
`WarnStuckClaimState` and the expected unmet equality between the real product
and the product plus one. It was not a parser error, missing import, timeout,
or unrelated crash. Exact output is in
`/audit-output/evidence/12_vacuity_mutation_kprove.log`.

The positive proof is therefore discriminating and non-vacuous.

## 7. Proven versus assumed accounting

The detailed ledger is
`/audit-output/evidence/trust_ledger.md`.

### What is proven

Conditional on the freshly compiled K definition and its builtins, the
machine-checked reachability theorem establishes partial correctness for the
exact submitted constructor program over all mathematical integer inputs:
the computation is consumed, the two parameters end as their absolute input
values, the exact function body remains loaded, and the result is

```text
(absInt(A) %Int 10) *Int (absInt(B) %Int 10)
```

Both the original and literal-AST claims close. The off-by-one destination
does not. This is a result-constraining theorem of the real submitted program,
not a test-only conclusion.

### Trusted and informal boundaries

- K v7.1.293 parsing, compilation, Haskell backend, and proof checking are
  unavoidable checker trust.
- K `Int`, `Bool`, `String`, `Map`, arithmetic/comparison operations,
  map operations, and generated strict heat/cool rules are trusted
  low-level primitives.
- The mounted translator is trusted; byte identity and regeneration establish
  that its output is exactly the submitted `solution.mpy`.
- Correspondence of the individually generated semantics to Python is
  supported by exhaustive static review of every used construct and 17
  concrete K-versus-candidate-Python executions. This is strong structural
  and finite evidence, not a universal machine-checked CPython connection
  theorem.
- `unitDigit` is not assumed or opaque: its total equation is inspected, but
  the fact that this is the requested HumanEval result is an intent bridge.
- `function(...)` and `noResult` are opaque data constructors only; neither
  can influence the integer answer except by carrying the explicitly executed
  body or marking initialization.
- Partial correctness does not add a separate total-termination theorem.
  The code is loop-free and all concrete executions terminate.

There are no result-bearing opaque primitives, empirical answer oracle,
unconstrained fresh symbols, proof-local axioms, algebraic simplifications,
loop summaries, or candidate-provided compiled facts in the trust base.

### Gate and verdict accounting

- Real-program soundness / non-vacuity: **PASS**. Fresh `#Top`, exact literal
  AST pinning, complete local-rule audit, result constraint, and rejected
  false mutation all succeed.
- Intent adequacy: **FAIL materially**. The proved absolute-input unit-digit
  formula disagrees with the trusted canonical's Python-modulo formula on
  valid negative inputs.
- Evidence auditability: **PASS**. Commands, statuses, bounded logs, scripts,
  input manifest, complete differential results, literal claim, mutation, and
  rule/trust inventories are preserved under `/audit-output/evidence/`.

Under the supplied decision boundary, the material intent discrepancy
precludes `PASS`, while the sound, non-vacuous proof of the exact real program
precludes `FAIL / NOT_LEGIT`. It is therefore a legitimate proof with a
material concern.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
