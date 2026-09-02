# Independent adversarial review — HumanEval 121 `solution`

This audit used the required Kit route in order: `using-kit`,
`validating-proof`, and, because the declared mode is
`GENERATED_SEMANTICS`, `writing-semantics`. The candidate’s generation report,
prior traces, and prior `#Top` were treated only as untrusted claims.

The candidate rebuilds and all four submitted claims close, the theorem is
non-vacuous, and the theorem mechanically pins the submitted program.
Nevertheless, the generated language theory contains an unguarded, globally
false `%` equation. A trusted-translator-generated program and a valid
non-empty integer-list input produce a concrete wrong result under that rule.
The Kit soundness contract requires every imported equation to be true over its
complete guard and expressly disallows excusing an off-path false equation.
Gate A therefore fails, so the reconstructed `#Top` is not a legitimate proof
state.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `121-solution`;
- condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`; and
- complete input provenance.

I read `/audit-input.json` first and used only its `container_paths` for mounted
inputs. I then read `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, all required legacy-selected-stage1 generation
records, the optional recorded `usage.json`, both Codex text logs, the
generation prompt, and all 171 JSONL events in the structured trace. Historical
`runtime-metrics.json` is absent, which is permitted for this declared legacy
layout and was not reconstructed.

The campaign block equals the lock as a JSON object, and the lock’s SHA-256 is
the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every directly recorded file hash matches, including run/task/result,
invocation, metrics, usage, Codex output/last message, generation prompt,
trusted canonical/prompt/translator, candidate prompt/translator, and the
individual trace file. The trace contains 171 valid JSON records. The mounted
candidate’s independently recomputed pipeline tree digest is
`21f8d91bbf47e4943ac6cf5a1a82f04e4f4b735dac5e7acc9e95ff4be65d0e9c`,
exactly the retained-workspace hash in both invocation and generation-result.
The trace tree digest similarly matches `usage.json`’s source-trace digest.

No symlink occurs under `/candidate`, `/reference`, or
`/generation-evidence`. Candidate `prompt.py` and `py2mpy.py` are byte-identical
to their trusted mounts. `/reference/reference-semantics` does not exist, as
required in `GENERATED_SEMANTICS`; no hidden or inferred reference semantics
was used.

The first inventory helper attempted unavailable `jq` and exited 1. This was a
reviewer-probe issue, not missing evidence: the files remained readable and
the complete standard-library verifier subsequently exited 0. Evidence:
[stage1 inventory log](evidence/stage1_inventory.log),
[integrity verifier](evidence/stage1_verify.py),
[integrity log](evidence/stage1_verify.log), and
[tree-hash log](evidence/stage1_tree_hash.log).

**Stage 1 result: PASS.** There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt’s contract is: for a non-empty list of integers, return the
sum of values that are both odd and at zero-based even positions. The trusted
canonical implementation filters `enumerate(lst)` by even index and odd value.
The candidate takes `lst[::2]`, filters values with `x % 2 != 0`, and sums
them. For integer `x` and positive divisor 2, that is extensionally equivalent,
including negative integers.

Running the trusted `/reference/py2mpy.py` over the scratch copy of
`solution.py` produced SHA-256
`a55f820888905adcf823d46ef45309212d34c6901f266d3e4acd991cd5ff3507`,
byte-identical to submitted `solution.mpy`.

The independent differential script imports the trusted canonical and
candidate modules separately. It checked:

- all three documented examples;
- empty input as an extra outside-contract boundary;
- singleton odd/even and positive/negative boundaries;
- selected versus skipped positions;
- mixed negative inputs and arbitrary-precision integers;
- every list of length 0 through 6 over values -3 through 3; and
- 5,000 deterministic random non-empty lists, lengths 1 through 40, with
  values in `[-10^9,10^9]`.

There were 142,269 comparisons and zero mismatches. This is finite fidelity
evidence, not a replacement for the K theorem. Evidence:
[differential script](evidence/differential_test.py) and
[fidelity log](evidence/stage2_fidelity.log).

**Stage 2 result: PASS.**

## 3. Clean proof reconstruction

Only source artifacts were copied to
`/tmp/audit-work/121-solution-audit`; candidate caches and compiled definitions
were not copied or reused. K reports version 7.1.293.

Fresh reconstruction produced:

- LLVM definition `semantic-audit-kompiled` from `semantic.k`, exit 0;
- Haskell definition `verification-audit-kompiled` from `verification.k`,
  exit 0; and
- ten concrete `krun` comparisons covering empty, singleton true/false,
  two-cell true/false, recursion, all examples, negatives, and very large
  integers. Corrected comparison output reports ten cases, zero mismatches
  against both Python implementations, and exit 0.

Each positive target claim was then selected independently:

| Claim | `kprove` exit | Required output |
|---|---:|---|
| `SPEC.example-one` | 0 | `#Top` |
| `SPEC.example-two` | 0 | `#Top` |
| `SPEC.example-three` | 0 | `#Top` |
| `SPEC.all-integer-lists` | 0 | `#Top` |
| aggregate `SPEC` run | 0 | `#Top` |

The initial concrete comparison helper over-escaped its result regex and
reported parsed results as `None`, making the wrapper exit 1 even though its
raw K configurations displayed the correct integers. The reviewer parser was
fixed without changing any candidate or compiled source; the same fresh
definition then passed all ten comparisons. Both logs are preserved.

Evidence:
[reconstruction commands and all proof outputs](evidence/stage3_reconstruction.log),
[corrected concrete comparison script](evidence/semantics_differential.py), and
[corrected concrete log](evidence/stage3_semantics_compare_retry.log).

**Stage 3 dynamic result: PASS.** This establishes closure under the submitted
theory; Stage 5 determines whether that theory is sound.

## 4. Adequacy and real-program pinning

The claims mean:

1. `example-one` starts the exact submitted program with
   `[5,8,7,1]`, unchanged original input, and accumulator 0, and requires
   `result(12)`.
2. `example-two` does the same for five 3s and requires `result(9)`.
3. `example-three` does the same for `[30,13,24,321]` and requires
   `result(0)`.
4. `all-integer-lists` has no explicit `requires`: `INPUT` ranges over
   arbitrary finite `Ints`, `_ORIGINAL` over arbitrary `Ints`, and `ACC` over
   arbitrary mathematical integers. It requires the running program to reach
   `result(expected(INPUT,ACC))`.

The universal precondition is satisfiable. For example,
`INPUT=ORIGINAL=cons(5,cons(8,nil))` and `ACC=0` is a source-entry state and
its claimed value is 5. Candidate Python, canonical Python, fresh K concrete
execution, and `expected` all yield 5. Each concrete example’s displayed
starting configuration is also a direct satisfying witness.

The arbitrary `_ORIGINAL` does not weaken this submitted theorem: in the exact
body, both the filter and yielded value use the inner binding `x`, so
`ORIGINAL` cannot affect the result. Actual source entries are included by
choosing `ORIGINAL=INPUT` and `ACC=0`. The universal claim covers all finite
lists, including the required unrestricted non-empty domain; empty input is a
sound extra case, not a narrowing.

Mechanical tokenization found 87 constructor tokens in submitted
`solution.mpy` and 87 in the right side of `solutionProgram`; both token streams
have SHA-256
`0db533c165fed8409fac6ab476c69b09ccdeeead9a89541c79d19de745def1f6`.
The trusted-regenerated term is identical too. This is constructor-level
pinning of the exact function binding and body, not merely a similar algorithm.

For body sensitivity, I changed the compared literal in the term actually
bound to `solutionProgram` from 0 to 1. The trusted translator’s mutated term
was mechanically identical to the mutated claim term and different from the
submitted term. Its proof definition built successfully, but on valid witness
`[5,8]` the changed program reached `result(0)` and `kprove` rejected the
unchanged required result 5 with `WarnStuckClaimState`, exit 1.

Evidence:
[pinning script](evidence/program_pinning.py),
[pinning log](evidence/stage4_pinning.log),
[executed body mutation](evidence/verification-body-mutation.k), and
[body-sensitivity log](evidence/stage5_body_sensitivity.log).

**Stage 4 result: PASS.**

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[rule_inventory.md](evidence/rule_inventory.md), supported by the mechanical
[declaration extraction](evidence/static_declaration_extract.log). It includes
all 22 syntax groups, the one-cell configuration, ten local `[function]`
symbols, 26 local equations/operational rules, and four claims. There are no
local `total`, `functional`, simplification, concrete, priority, `owise`,
opaque, fresh, or uninterpreted declarations.

The submitted constructors map completely to the generated semantics:
the five `run` rules match the full
module/function/return/sum/comprehension/slice shape; `testAt` and `valueAt`
evaluate the filter and body; lookup/projection rules preserve bindings; and
empty, singleton, and pair-plus cursor rules implement zero-based pair
skipping. The rules preserve the sole observable `<k>` cell and continuation.
The program is pure on the integer-list domain, so there is no omitted heap,
I/O, allocation, mutation, exception, or abrupt-control effect. Cursor cases
are disjoint, Boolean guards are complementary, and recursive cases remove two
cells. `solutionProgram` is a truthful ground definition, and all five
`expected` equations are disjoint, exhaustive for `Ints`, and descending.

One semantic equation fails its complete-domain obligation:

```k
rule eval(BinOp("%", LEFT, RIGHT), ENV)
  => intVal(asInt(eval(LEFT, ENV)) modInt asInt(eval(RIGHT, ENV)))
```

It has no guard restricting `RIGHT` to a positive divisor. Python remainder
has the divisor’s sign; K `modInt` is Euclidean. This is not merely a
value-level discrepancy without observable effect. I used the trusted
translator on this program, which remains within the exact compound shape
accepted by the five `run` rules:

```python
def solution(lst):
    return sum([x for x in lst[::2] if 1 % x != 1])
```

On `[-2]`, a valid non-empty list of integers, Python computes
`1 % -2 == -1`, the filter is true, and the function returns `-2`. The
candidate semantics computes `1 modInt -2 == 1`, makes the filter false, and
returns `0`. `krun` exits 0 with that false result. The translated term, exact
command, input, Python result, K result, and exit are preserved in
[the false-rule witness log](evidence/stage5_mod_rule_witness.log).

The immutable submitted body reaches S5 only with divisor `+2`, where the
chosen operation agrees with Python. That does not validate the unguarded
equation over its declared match domain. Under the required Kit extension
contract, every equation must be true wherever its guard applies, and an
off-path false equation cannot be accepted merely because a present claim uses
one safe instance. The proof imports this `%` equation, and the equation
contributes to evaluating its result-bearing filter. It needed either a
positive-divisor guard/narrowed `Int(2)` pattern or an actual Python-remainder
definition.

**Stage 5 result: FAIL (Gate A4).** The successful `#Top` is closure under a
materially unsound generated semantics and is therefore unusable as a
legitimate proof state.

## 6. Fresh non-vacuity test

The candidate supplied no vacuity file, so there was nothing to trust. I
created a fresh concrete result mutation using the unchanged submitted program
term and satisfying input `[5,8]`. The true result is 5; the mutation demands
`expected([5,8],0) +Int 1`, i.e. 6.

`kprove --dry-run` exited 0, establishing that the mutation parsed and built.
The actual proof then reached `<k> result(5) ... </k>`, emitted
`WarnStuckClaimState`, and exited 1 because it could not unify with the false
destination. This is the expected unmet result obligation, not a parser error,
timeout, unrelated crash, or unreachable mutation.

Evidence:
[false spec](evidence/spec-vacuity-audit.k) and
[non-vacuity log](evidence/stage6_nonvacuity.log).

**Stage 6 result: PASS.** The theorem is result-constraining, but non-vacuity
does not repair Stage 5’s false semantic equation.

## 7. Proven versus assumed accounting and decision

What the successful reachability run establishes, precisely, is conditional on
the candidate theory:

> For every finite constructor list `INPUT`, every `Ints` term `_ORIGINAL`,
> and every mathematical integer `ACC`,
> `run(solutionProgram, INPUT, _ORIGINAL, ACC)` reaches
> `result(expected(INPUT,ACC))`; the three displayed ground instances also
> reach their displayed results.

For actual entry states, substitute `ORIGINAL=INPUT` and `ACC=0`.
`expected` is a fully equational, descending recurrence that sums odd values
at positions 0, 2, 4, and so on. This is a partial-correctness statement; it is
not by itself a total-correctness theorem, although the concrete operational
rules visibly descend on finite `Ints`.

Trust and assumption ledger:

| Boundary | Role and dependents | Assessment |
|---|---|---|
| Trusted prompt, canonical, and translator mounts | Fix source contract, executable oracle, and Python-AST constructor image | Integrity verified. Canonical/differential evidence is finite and is not substituted for K proof. |
| K parser/compiler/Haskell prover/LLVM runtime 7.1.293 | Builds and checks all K artifacts | Ordinary toolchain trust boundary; clean source rebuilds succeeded. |
| Built-in mathematical `Int`, `+Int`, integer equality, Boolean negation, and String equality | Used by semantics and `expected` | Acceptable fixed primitive boundary for mathematical integers/Booleans/strings. |
| Candidate-generated compound `run` semantics | Connects the submitted constructor term to Python list slice/filter/sum behavior | No hidden reference semantics exists. Rule-by-rule induction and concrete branch tests support the exact program, but this remains the generated-language intent bridge. |
| `solutionProgram` and `expected` | Exact program name and mathematical postcondition recurrence | Fully defined, mechanically pinned, non-opaque, terminating; not assumed or oracle-valued. |
| `%` rule S5 | Result-bearing filter evaluation in the target proof and any matching translated term | Illegitimate as asserted: the unguarded equation has a concrete false-result witness. |
| Differential tests | Candidate/canonical bridge and finite concrete semantics evidence | Strong finite support only: 142,269 Python comparisons and ten fresh K comparisons. |

There are no fresh, opaque, unconstrained, or external result-bearing symbols.
There is no domain narrowing: the claim is unbounded over finite integer lists.
Gate B (intent adequacy) and the non-vacuity/pinning portions of Gate C pass.
Gate A fails because the imported generated semantics contains a witnessed
false equation. Under the benchmark’s decision boundary, materially unsound
semantics makes the candidate proof not legitimate even though all positive
claims print `#Top`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
