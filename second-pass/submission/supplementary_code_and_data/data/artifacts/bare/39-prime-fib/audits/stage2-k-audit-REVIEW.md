# Independent adversarial audit: HumanEval/39 `prime_fib`

## Executive finding

The candidate does not contain a legitimate partial-correctness proof of the
submitted generated program. Fresh reconstruction does reproduce every reported
`#Top`, and the submitted Python implementation agrees with the trusted
canonical implementation on the intended positive-index test domain. The fatal
issue is instead in `verification.k`: a priority-20 rule rewrites the whole
`primeFibProgram` directly to the desired result, preserves an empty
environment, and skips all program execution. It has no bridge-free universal
connection theorem.

This is not merely an evidence gap. For the satisfiable input `N = 1`, fixed
small-step execution terminates with seven local bindings in `<env>`, whereas
the bridge proves a final empty environment. The extended proof closes for that
false final state, and the same claim fails under the bridge-free definition
with the real populated state shown in the residual. A material K-level body
mutation (`return b` to `return a`) also changes fixed execution from result
`2` to result `1`, while the unchanged bridge still proves result `2`.

## 1. Input and provenance integrity

I first read `/audit-input.json` and used only its `container_paths` mounts, not
the host-only provenance paths. The declared layout is
`legacy-selected-stage1`, the condition is `bare`, and the semantics mode is
`GENERATED_SEMANTICS`.

The following required records are present as real regular files:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- the structured trace at
  `/generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T04-48-17-019f8939-d9de-75e0-b02f-2e24ba019299.jsonl`.

`usage.json` is present and was inspected. Historical
`runtime-metrics.json` is absent, which is expected for this legacy layout and
is not a defect. The additional legacy records `legacy-metrics.json` and
`legacy-run-input.json` are present, regular, readable, and match the hashes in
the selected-stage result.

The campaign object in `/audit-campaign-lock.json` is structurally identical to
the campaign block embedded in `/audit-input.json`; its SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the recorded value. Every recorded regular-file hash was recomputed and
matched, including the manifests, selected result, invocation, metrics, usage,
generation prompt/output/last message, trusted canonical, trusted prompt,
trusted translator, and the candidate copies of the prompt and translator.

The candidate tree contains only regular files and real directories; no
candidate or trace entry is a symlink or an unsupported node. An independent
path/type/size/content digest of `/candidate` is
`7617d1a2325643c15e9cad9323f05382956c15750782d74e86ee0ac603495696`,
which exactly matches both the selected result's workspace digest and the
invocation's retained-workspace digest. The corresponding trace content digest
is `8005ca4f13d0b87546060d252cda7f01b00d0f848101327c4d3fa43ddf8a0102`,
which exactly matches `usage.json`'s source-trace digest; the sole trace file
also matches its recorded file hash. The launcher separately records snapshot
tree digests `04be...` and `85ad...`; their encoding is not declared, so I
recorded them without conflating them with the independently computed pipeline
content digests.

The entire 200-line structured JSONL trace parsed successfully (136 response
items, 61 event messages, one session metadata record, one turn-context record,
and one world-state record). I also read all 15,533 lines of
`codex-output.log`, all 12 lines of `codex-last.txt`, and all 55 lines of the
generation prompt. Their `KPROVE_PASSED` text was treated only as an untrusted
historical claim.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. As required for
`GENERATED_SEMANTICS`, neither `/reference/reference-semantics` nor a candidate
`reference-semantics` tree exists. Thus there is no supplied semantics to infer
or compare, and no semantics-mode infrastructure contradiction.

Evidence: [stage1_integrity.py](evidence/stage1_integrity.py) and
[stage1_integrity.log](evidence/stage1_integrity.log). No infrastructure breach
was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and intended domain

The trusted prompt says that `prime_fib(n)` returns the `n`-th number that is
both Fibonacci and prime, with examples:

`1 ↦ 2`, `2 ↦ 3`, `3 ↦ 5`, `4 ↦ 13`, and `5 ↦ 89`.

The ordinary meaning of “n-th” and every documented example make the material
source-contract domain the positive integers `n >= 1`. This is also the domain
of the candidate's general claim. For completeness, I characterized nearby
out-of-domain values: both Python implementations return `1` for `n = 0`;
the submitted implementation returns `1` for `n = -1`, while the canonical
implementation does not terminate within a bounded subprocess.

The trusted canonical implementation grows a Fibonacci list and uses a local
trial-division primality predicate. The submitted `solution.py` instead carries
two adjacent Fibonacci values and checks divisors in a nested loop. The
algorithm is different but implements the same positive-index behavior.

### Trusted regeneration

From the scratch copy I ran:

```text
python3 /tmp/audit-work/39-prime-fib/src/trusted-py2mpy.py \
  /tmp/audit-work/39-prime-fib/src/solution.py \
  > /tmp/audit-work/39-prime-fib/src/regenerated-solution.mpy
cmp regenerated-solution.mpy solution.mpy
```

The command exited 0. Both files have SHA-256
`b974be7f6a38b276db6edf9f42b1a45f969a938cd59d15a0b492367469d67945`.
See [stage2_regeneration.log](evidence/stage2_regeneration.log).

### Independent differential test

The reviewer-authored test imports the trusted canonical entry point and the
submitted entry point independently. It compares inputs `1..10`, thereby
covering all five examples, the positive boundary, generated later indices,
the `b < 2` branch, divisor-loop zero and nonzero iterations, divisible and
non-divisible candidates, prime and non-prime candidates, and the outer-loop
exit. There were zero mismatches:

```text
[2, 3, 5, 13, 89, 233, 1597, 28657, 514229, 433494437]
```

It also records the scalar-input “empty case” as not applicable and checks
`0` and `-1` as the adjacent out-of-domain boundaries. The final run exited 0.
See [differential_test.py](evidence/differential_test.py) and
[stage2_differential.log](evidence/stage2_differential.log).

Stage 2 result: the submitted implementation is faithful on the intended
positive domain, and `solution.mpy` is the trusted translation of that exact
implementation.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/39-prime-fib/src`; no
candidate-provided compiled definition or cache was reused. The live toolchain
is K `v7.1.293`.

### Generated semantics

Fresh LLVM build:

```text
kompile --main-module MPY --syntax-module MPY-SYNTAX \
  --backend llvm -o audit-semantic-llvm-kompiled semantic.k
```

Exit 0; see
[stage3_kompile_semantic.log](evidence/stage3_kompile_semantic.log).

Fresh `krun` comparisons on `n = -1, 0, 1, 2, 3, 4, 5` all exited 0, consumed
the computation to `.K`, and matched the submitted Python result exactly:
`1, 1, 2, 3, 5, 13, 89`. The logs also preserve the final environments.
See [semantic_differential.py](evidence/semantic_differential.py) and
[stage3_semantic_differential.log](evidence/stage3_semantic_differential.log).

### Bridge-free finite concrete claims

Fresh Haskell build:

```text
kompile --main-module PRIME-FIB-PROGRAM \
  --syntax-module PRIME-FIB-PROGRAM \
  --backend haskell -o audit-concrete-kompiled verification.k
```

Exit 0. Then:

```text
kprove concrete-spec.k --definition audit-concrete-kompiled \
  --spec-module CONCRETE-SPEC --color off
```

printed `#Top` and exited 0. See
[stage3_kompile_concrete.log](evidence/stage3_kompile_concrete.log) and
[stage3_kprove_concrete_all.log](evidence/stage3_kprove_concrete_all.log).

### Extended target claims

Fresh Haskell build:

```text
kompile --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --backend haskell -o audit-verification-kompiled verification.k
```

Exit 0. Then:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --color off
```

printed `#Top` and exited 0. See
[stage3_kompile_verification.log](evidence/stage3_kompile_verification.log) and
[stage3_kprove_spec_all.log](evidence/stage3_kprove_spec_all.log).

I also selected every claim separately. Each of `concrete-1` through
`concrete-5`, `prime-fib-correct`, and `example-1` through `example-5` printed
`#Top` and exited 0. Exact commands and statuses are in
[run_all_claims.sh](evidence/run_all_claims.sh) and
[stage3_kprove_each.log](evidence/stage3_kprove_each.log).

Stage 3 result: machine closure is reproducible. It is closure under the
candidate's theory, not yet evidence that the theory faithfully executes the
real program.

## 4. Adequacy and real-program pinning

### Plain-language claims

The general `prime-fib-correct` claim starts with:

- computation exactly `primeFibProgram`;
- empty environment;
- input cell `N`;
- `noResult`;
- precondition `N > 0`.

It claims termination with an empty computation, the same empty environment,
the unchanged input cell, and result `primeFibSpec(N)`.

Each `example-i` claim has the same exact initial and final cell shapes, fixes
`N` to `1..5`, and fixes the result to `2, 3, 5, 13, 89`. Each bridge-free
`concrete-i` claim instead executes the same entry term and correctly constrains
the populated final local environment as well as the result for one fixed
input.

The general precondition is satisfiable; for example:

```text
<k> primeFibProgram </k>
<env> .Map </env>
<n> 1 </n>
<result> noResult </result>
```

Substitution gives `primeFibSpec(1) = 2`, agreeing with both Python
implementations, and `primeFibSpec(4) = 13`, also agreeing with both.

### Mechanical program identity

After trusted regeneration, I extracted the RHS of the
`primeFibProgram` definitional rule and parsed it and `solution.mpy` with the
fresh K parser. The only normalization was three explicit replacements of the
internal K list identity `.Stmts` with the external parser's blank empty-list
spelling. The two parsed KAST byte strings are identical and both have SHA-256
`b128584ac048671a1b1670c7efcbbfe9c55dc7b9b1a96eac7b77ccee0a72a9a7`.
See [compare_program_terms.py](evidence/compare_program_terms.py) and
[stage4_program_term_compare.log](evidence/stage4_program_term_compare.log).

Thus the alias itself pins the submitted translated body. Lack of automatic
source-to-alias regeneration is only a maintenance observation here, not the
failure.

### False final-state witness

The priority-20 rule in `verification.k` is:

```k
rule <k> primeFibProgram => .K </k>
     <env> .Map </env>
     <n> N </n>
     <result> noResult => primeFibSpec(N) </result>
  requires N >Int 0
  [priority(20)]
```

At `N = 1`, this rule proves a final empty `<env>`. Under the bridge-free
small-step definition, the real final configuration is:

```text
<env>
  "a" |-> 1
  "b" |-> 2
  "c" |-> 2
  "count" |-> 1
  "divisor" |-> 2
  "n" |-> 1
  "prime" |-> true
</env>
<result> 2 </result>
```

The extended witness claim printed `#Top` and exited 0. The identical state
claim under the bridge-free definition exited 1 with
`WarnStuckClaimState`, displaying the populated environment above. These are
[audit-bridge-state-extended.k](evidence/audit-bridge-state-extended.k),
[audit-bridge-state-fixed.k](evidence/audit-bridge-state-fixed.k),
[stage4_bridge_extended_accepts.log](evidence/stage4_bridge_extended_accepts.log),
and [stage4_bridge_fixed_rejects.log](evidence/stage4_bridge_fixed_rejects.log).

This is the required concrete false conclusion enabled by the rule on a state
satisfying the entry precondition. Every target claim that demands an empty
final environment is false of fixed execution.

### Body sensitivity

I made a K-level body mutation in the actual alias expansion:

```text
Return(Name("b"))  ->  Return(Name("a"))
```

This changes the program term reached from `primeFibProgram`, not merely an
external `solution.py` file. With the bridge disabled, the mutated body at
`N = 1` provably returns `1` and the fixed claim prints `#Top`. With the bridge
enabled, the unchanged summary still proves result `2` and an empty environment,
also with `#Top`. See
[make_body_mutation.py](evidence/make_body_mutation.py),
[audit-body-mut-verification.k](evidence/audit-body-mut-verification.k),
[audit-body-mut-fixed-spec.k](evidence/audit-body-mut-fixed-spec.k),
[audit-body-mut-extended-spec.k](evidence/audit-body-mut-extended-spec.k), and
the five `stage4_*body_mut*.log` files.

Stage 4 result: syntactic pinning passes, but semantic pinning fails. The target
proof is insensitive to material execution and proves a final state the real
program cannot reach.

## 5. Rule-by-rule static soundness review

The complete numbered sources and machine-extracted declaration counts are in
[stage5_numbered_sources.log](evidence/stage5_numbered_sources.log) and
[stage5_declaration_counts.log](evidence/stage5_declaration_counts.log).

### Local declaration inventory

`semantic.k` declares:

- `Pgm`: `Module(Stmts)`;
- list and wrapper sorts `Stmts`, `Params`, and `Strings`;
- statement constructors `FuncDef`, `Assign`, `If`, `While`, and `Return`;
- expression constructors `Int`, `Bool`, `Name`, `BinOp`, and `Compare`;
- `CmpOp`;
- `Value ::= Int | Bool` and `Result ::= noResult | Value`;
- K items `exec`, `eval`, `assignTo`, `binLeft`, `binRight`, `cmpLeft`,
  `cmpRight`, `ifDecision`, `whileLoop`, `whileDecision`, and `returnValue`;
- one `<mpy>` configuration with `<k>`, `<env>`, `<n>`, and `<result>`.

`verification.k` additionally declares:

- the `Pgm` alias token `primeFibProgram`;
- Boolean functions `noDivisors(Int,Int)` and `isPrime(Int)`;
- integer functions `primeFibFrom(Int,Int,Int)` and `primeFibSpec(Int)`.

There are four `[function]` declarations. There are no local `[total]`,
`[functional]`, `[simplification]`, `[concrete]`, or opaque declarations.
There are two priority rules: alias unfolding at priority 30 and the
whole-program bridge at priority 20. There are no generated helper K files
outside `semantic.k` and `verification.k`.

### Used-construct coverage

Every constructor in `solution.mpy` is covered:

| Program construct | Declaration and behavior |
|---|---|
| `Module`, one `FuncDef`, `Params`, statement list | module-start rule and the two `exec` list rules |
| `Assign(Name(...), ...)` | assignment evaluation and map-update rules |
| `If` and Boolean conditions | condition evaluation plus true/false selection |
| `While` | loop wrapper, guard evaluation, true back-edge, false exit |
| `Return` | expression evaluation, result update, and function-level continuation discard |
| `Int`, `Bool`, `Name` | literal and environment-lookup rules |
| `BinOp("+")`, `BinOp("*")`, `BinOp("%")` | left-to-right evaluation and the three integer operations |
| comparisons `<`, `<=`, `==` | left-to-right comparison and three Boolean result rules |

No used construct is parsed but left without behavior. Unsupported operators or
shapes stop visibly rather than fabricating a value.

### All 27 `semantic.k` rules

| ID / source | Rule | Decision |
|---|---|---|
| S01 line 61 | Start the sole one-argument function body, bind its parameter to `<n>`. | Sound for the chosen one-function module representation and the submitted term. It requires the exact empty initial environment. |
| S02 line 65 | `exec(.Stmts) => .K`. | Sound empty-list termination. |
| S03 line 66 | Execute list head, then tail. | Sound sequencing. |
| S04 line 68 | Lower assignment to expression evaluation then `assignTo`. | Sound evaluation order. |
| S05 line 69 | Update the map with an evaluated `Value`. | Sound assignment state change. |
| S06 line 72 | Lower `If` to guard evaluation. | Sound. |
| S07 line 73 | Select then-branch on `true`. | Sound. |
| S08 line 74 | Select else-branch on `false`. | Sound. |
| S09 line 76 | Lower `While` to `whileLoop`. | Sound. |
| S10 line 77 | Evaluate the loop guard. | Sound. |
| S11 line 78 | On true, run the body and return to the same loop head. | Sound control/back-edge; supports the real nested loops. |
| S12 line 79 | On false, finish the loop. | Sound zero-iteration/exit case. |
| S13 line 81 | Evaluate a return expression. | Sound. |
| S14 line 82 | Store the returned value and discard the remaining function computation. | Sound for this top-level, call-stack-free function model; it preserves the environment, as the fixed witness confirms. |
| S15 line 85 | Evaluate integer literal. | Sound. |
| S16 line 86 | Evaluate Boolean literal. | Sound. |
| S17 line 87 | Look up a bound name. | Sound; an unbound name remains visibly stuck. |
| S18 line 90 | Begin binary expression with its left operand. | Sound left-to-right order. |
| S19 line 91 | After the left integer, evaluate the right. | Sound left-to-right order. |
| S20 line 92 | Integer addition. | Sound; K unbounded integers match Python integers here. |
| S21 line 93 | Integer multiplication. | Sound. |
| S22 line 94 | Integer remainder. | Sound on the used positive divisor states; divisor zero is unreachable in this program. |
| S23 line 96 | Begin comparison with the left operand. | Sound left-to-right order. |
| S24 line 98 | After the left integer, evaluate the right. | Sound. |
| S25 line 99 | Integer `<`. | Sound. |
| S26 line 100 | Integer `<=`. | Sound. |
| S27 line 101 | Integer equality. | Sound. |

The generated semantics models unbounded integers, maps, and pure local state;
that is adequate for every material operation in this program. It does not
model unused Python features, which is acceptable in generated-semantics mode.

### All 11 `verification.k` rules

| ID / source | Rule | Class and decision |
|---|---|---|
| V01 lines 11–43 | `primeFibProgram` unfolds to the full constructor body, priority 30. | Definitional alias. Sound: the mechanical KAST comparison is exact after empty-list spelling normalization. |
| V02 line 55 | `isPrime(N) => false` for `N < 2`. | Truthful definitional equation. |
| V03 line 57 | `isPrime(N) => noDivisors(N,2)` for `N >= 2`. | Truthful reduction to trial division. Guard is disjoint from V02. |
| V04 line 60 | `noDivisors(N,D) => true` when `D*D > N`. | Truthful empty remaining divisor interval on all uses (`N >= 2`, `D >= 2`). |
| V05 line 62 | Return false when `D*D <= N` and `D` divides `N`. | Truthful. |
| V06 line 64 | Increment `D` when in range and non-dividing. | Truthful recursive descent toward the square-root boundary. V04–V06 have disjoint used-state guards. |
| V07 line 72 | Initialize `primeFibSpec(N)` as `primeFibFrom(N,0,1)`. | Truthful definitional summary. |
| V08 line 73 | With zero remaining primes, return `B`. | Truthful base case. |
| V09 lines 74–76 | If successor `A+B` is prime and `R>0`, decrement `R`. | Truthful Fibonacci-prime search recurrence. |
| V10 lines 77–79 | If successor is not prime and `R>0`, retain `R`. | Truthful complementary recurrence. The guards of V08–V10 are disjoint. |
| V11 lines 84–89 | Rewrite the entire exact program directly to `primeFibSpec(N)`, preserve empty environment, priority 20. | **Illegitimate operational bridge.** It replaces all binding, assignments, loops, guard evaluation, primality computation, and return. There is no bridge-free universal connection theorem. It is false on observable state at `N=1`, and the K-level body mutation shows result-level body insensitivity. |

The functions are not declared total. Their equations cover every use in the
positive-domain postcondition: `isPrime` covers all integers;
`noDivisors` is entered at `D=2`; `primeFibFrom` is entered with positive
remaining count and transitions to zero. Potentially stuck or divergent
off-domain arguments therefore do not create a false totality assertion.

### Claim inventory and dependency

`spec.k` contains the general claim and five example claims. All six demand an
empty final environment and depend on V11. The general claim's transition is
textually the same transition V11 supplies; it does not prove V11.

`concrete-spec.k` contains five finite fixed-input executions. They import
`PRIME-FIB-PROGRAM`, not `VERIFICATION`, and legitimately prove the submitted
body's results and populated states for `N=1..5`. They neither quantify over
positive `N` nor establish a universal connection theorem for V11.

Stage 5 result: the generated small-step semantics is adequate for this
program, but V11 is a materially unsound, task-answer-encoding proof rule with
an explicit false conclusion witness. No other local rule is labeled unsound.

## 6. Fresh non-vacuity test

I created a fresh claim that keeps the satisfiable precondition `N > 0` but
changes the result obligation to:

```k
<result> noResult => primeFibSpec(N) +Int 1 </result>
```

At the concrete satisfying witness `N = 1`, the submitted program, canonical
program, and `primeFibSpec` all produce `2`; the mutation demands `3`.

The exact mutation is preserved as
[spec-vacuity.k](evidence/spec-vacuity.k). First:

```text
kprove audit-spec-vacuity.k --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY --dry-run --color off
```

exited 0, confirming successful parsing and proof-input construction. The same
command without `--dry-run` exited 1 with `WarnStuckClaimState`; its residual
shows the failed equality between `primeFibFrom(...) +Int 1` and
`primeFibFrom(...)`. See
[stage6_mutation_dry_run.log](evidence/stage6_mutation_dry_run.log) and
[stage6_mutation_proof.log](evidence/stage6_mutation_proof.log).

Stage 6 result: the submitted claim is result-constraining and non-vacuous in
this narrow sense. This does not validate the operational bridge that supplies
the result.

## 7. Proven versus assumed accounting

### What the successful K runs actually establish

Under the extended theory containing V11:

1. the exact token `primeFibProgram`, from an empty environment and positive
   input, rewrites to `.K`, an empty environment, and
   `primeFibSpec(N)`—because V11 states that transition as an ordinary rule;
2. the transparent helper equations reduce the first five concrete
   `primeFibSpec` values to `2, 3, 5, 13, 89`;
3. without V11, fixed small-step execution reaches the five concrete populated
   final states asserted in `concrete-spec.k`.

It does not establish a universal bridge-free theorem that the submitted body
computes `primeFibSpec(N)`, and it does not establish the target claims' empty
final environment under real execution.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K `v7.1.293` compiler, LLVM/Haskell backends, and `#Top` implementation | All machine runs | Ordinary toolchain trust; acceptable. |
| Built-in `Int`, `Bool`, `String`, `Map`, arithmetic, comparison, Boolean, and remainder operations | Small-step semantics and helper equations | Low-level fixed primitives; acceptable for the used non-exceptional states. |
| Trusted `/reference/py2mpy.py` | Source-to-`solution.mpy` bridge | Acceptable here: byte-identical regeneration and constructor-level term comparison were performed. |
| Candidate-generated `semantic.k` as a model of the used Python subset | Concrete claims and intended execution model | Independently audited rule by rule and concretely compared on boundary/normal inputs. Minimal unused-feature coverage is acceptable. |
| Mathematical reading of `isPrime`, `noDivisors`, and `primeFibFrom` as primality and Fibonacci-prime search | Human-facing meaning of `primeFibSpec` | Transparent equations and ordinary mathematics support it; differential checks through index 10 are finite corroboration, not a universal proof. |
| V11 whole-program summary | All six claims in `spec.k` | Illegitimate. It is program-derived, result/control/state-bearing, lacks the required bridge-free universal connection theorem, fabricates final state, and survives a material body mutation. |
| Five bridge-free concrete claims | Fixed inputs `1..5` only | Legitimate finite reachability evidence; cannot justify an unrestricted positive-input theorem. |
| Python/K differential tests | Inputs explicitly listed in Stages 2 and 3 | Empirical bridge evidence only; not a substitute for a K connection proof. |
| Partial-correctness termination boundary | General positive domain | The requested theorem is conditional on termination; no claim of infinitely many Fibonacci primes is needed. V11 nevertheless bypasses real execution rather than proving partial correctness of it. |

### Gate and benchmark decision

- Real-program soundness (Kit Gate A): **fail** because of V11's false state
  transition, missing connection theorem, and body insensitivity.
- Intent adequacy (Kit Gate B): the formal positive domain matches the material
  “n-th” source contract, and the result summary has the intended mathematical
  shape; this cannot rescue Gate A.
- Trust/evidence auditability (Kit Gate C): reconstruction and finite evidence
  are reproducible, but the central bridge has no acceptable justification.

Accordingly, the benchmark decision is failure, not a concern-only limitation:
the candidate's general `#Top` is obtained by a materially unsound
whole-program rule and the claimed full final configuration is false of the
real generated program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
