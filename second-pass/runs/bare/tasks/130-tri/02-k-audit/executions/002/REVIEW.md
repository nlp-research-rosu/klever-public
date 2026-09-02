# Independent adversarial audit: HumanEval 130 `tri`

The candidate's K claims do reconstruct and close, are non-vacuous, and
mechanically execute the submitted constructor tree. They are nevertheless not
a legitimate partial-correctness proof of the real generated Python program
over the stated unrestricted domain. The generated call semantics has an
unbounded mathematical call stack and no `RecursionError` path. On the
satisfying input `n = 1100`, fresh K execution returns the claimed 1101-element
list, while the actual submitted `solution.py` terminates exceptionally with
`RecursionError`; the trusted iterative canonical function returns normally.
This is a concrete, material false-normal-return witness on the source-contract
domain.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `130-tri`, condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`; and
- `mount_reference_semantics: false`.

I used only its `container_paths`, not the host provenance strings. Every
required launcher record for this layout is a real regular file, both required
trees are real directories, and no required proof artifact is symlinked or
mistyped. I read `/run.json`, `/task.json`, `/generation-result.json`,
`invocation.json`, `metrics.json`, `usage.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and all 173 JSONL events in the structured
trace. Historical runtime metrics are absent but are not required for
`legacy-selected-stage1`; I did not reconstruct them.

The campaign lock is structurally identical to the `audit_campaign` block and
its SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
All recorded regular-file hashes checked by the reviewer match. The independent
pipeline tree digest of `/candidate` is
`fee6381d823aa4f536d15c10a5e095c38fc71e0ffbbe5d0aefca2362a99553fa`,
matching both the invocation's retained-workspace digest and the stage result.
The independently reconstructed trace digest is
`f3073adc16c231331e219680cd7314816bbd95e381a805a3b5069f70d1bd241b`,
matching `usage.json`; the sole trace file also matches its recorded
per-file hash.

The mounted candidate `prompt.py` and `py2mpy.py` are byte-identical to their
trusted `/reference` versions. As required in generated-semantics mode,
`/reference/reference-semantics` does not exist, and the candidate contains no
purported reference-semantics tree. There is no infrastructure breach.

Evidence:

- [stage1_integrity.py](evidence/stage1_integrity.py)
- [stage1_integrity.log](evidence/stage1_integrity.log)

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

For every non-negative integer `n`, `tri(n)` must return the first `n + 1`
sequence values. From the prompt, example, and trusted canonical source:

- value 0 is 1 and value 1 is 3;
- an even index `i` has value `1 + i / 2`; and
- an odd index `i >= 3` has value
  `value(i-1) + value(i-2) + value(i+1)`.

The trusted canonical implementation constructs the list iteratively. The
candidate instead calls `tri(n-1)` recursively and appends a closed-form last
value: `1 + n // 2` for even `n`, and
`((n+1)//2) * ((n+5)//2)` for odd `n`. The odd closed form is mathematically
correct.

### Translation identity

I copied source inputs to `/tmp/audit-work/130-tri-audit`, used the trusted
translator, and generated `regenerated-solution.mpy`. Translation exited 0;
`cmp` exited 0; both submitted and regenerated files have SHA-256
`22d6128fdbae80fa2d4785035d262da6050bbe91572a3a1b7825c8579fc85663`.

Evidence:

- [prepare_and_translate.sh](evidence/prepare_and_translate.sh)
- [prepare_and_translate.log](evidence/prepare_and_translate.log)

### Independent differential

The reviewer differential imports both entry points and also uses an
independently written recurrence oracle. It covers the documented example,
every input 0 through 300, 117 distinct seeded samples up to 900, and explicit
recursion-boundary probes. Across 385 ordinary cases there were zero numeric
value mismatches.

The candidate returns Python integers where the canonical returns integral
floats from index 2 onward. Python list equality treats those numerically equal,
and the prompt does not impose exact element classes, so this is a
representation observation rather than the decisive defect.

The unrestricted-domain control behavior diverges materially. Under the
mounted CPython 3.10.12 runtime with recursion limit 1000, sufficiently deep
calls raise `RecursionError`. The stable witness used for the semantics
comparison is:

| Input | Submitted `solution.py` | Trusted canonical | Contract oracle |
|---:|---|---|---|
| 1100 | raises `RecursionError` | returns length 1101, last value 551 | returns length 1101, last value 551 |

This input satisfies the exact source precondition. It is not a fixed-size or
out-of-contract test.

Evidence:

- [differential.py](evidence/differential.py)
- [differential.log](evidence/differential.log)

## 3. Clean proof reconstruction

No candidate-built definition or cache was used. From the scratch source copy I
built:

```text
kompile semantic.k --backend llvm --main-module TRI-SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-concrete-kompiled

kompile verification.k --backend haskell \
  --main-module TRI-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-proof-kompiled
```

Both commands exited 0 using K 7.1.293. The unmodified `TRI-SPEC` proof exited
0 and printed `#Top`. I then ran exact isolated copies of all six positive
claims. Each exited 0 and printed `#Top`; the outer `run` claim was tested
together with the exact `evalCall` circularity on which it depends.

Evidence:

- [build_fresh.sh](evidence/build_fresh.sh) and
  [build_fresh.log](evidence/build_fresh.log)
- [run_positive_claims.sh](evidence/run_positive_claims.sh),
  the [isolated claim sources](evidence/positive-claims/), and
  [positive_claims.log](evidence/positive_claims.log)

The freshly built LLVM semantics was concretely run on
`0,1,2,3,4,5,6,10,25,50`. Every K result numerically matched both Python
implementations and the independent oracle. The boundary witness exposes the
model gap: `krun` at `N=1100` exited 0 and returned an `IntSeq` of length 1101
ending in 551, while actual `solution.tri(1100)` raised `RecursionError`.

Evidence:

- [concrete_semantics_compare.py](evidence/concrete_semantics_compare.py)
- [concrete_semantics_compare.log](evidence/concrete_semantics_compare.log)

The dynamic reconstruction gate therefore has two distinct results:
verification under the submitted theory succeeds, but that theory's execution
does not faithfully reconstruct real Python control behavior on the full
domain.

## 4. Adequacy and real-program pinning

The six submitted claims say:

1. For every `N >= 0`, evaluating binding `"tri"` in `solutionProgram` returns
   `LVal(triPrefix(N))`. This exact invocation claim is also the recursive
   circularity.
2. For every `N >= 0`, the configured `run(solutionProgram,N)` entry returns
   that same constrained result.
3. `triValue(0) = 1`.
4. `triValue(1) = 3`.
5. Every even `N >= 2` has value `1 + N/2`.
6. Every odd `N >= 3` satisfies the stated three-term recurrence.

The return is not a free variable, tautology, or one-way implication:
`triPrefix` is recursively defined from the fully guarded `triValue` equations.
Concrete states `N = 0,1,2,3,6,25,1100` all satisfy the entry precondition.
Substitution at the ordinary inputs agrees with both Python implementations.

Program syntax is pinned successfully. Fresh `kast` expansion of
`solutionProgram` and fresh parsing of submitted `solution.mpy` produced
byte-identical 6903-byte KORE files with SHA-256
`7b4bafd19673b5457db3ae3ab955c887034738cdf0f50aa2fe71682211d49c8b`.

A reviewer body-sensitivity mutation changed the executed macro term itself,
replacing the odd factor `n+5` with `n+7`. Its KORE hash changed to
`81470e351b35ee9f5e30f0ed4dc822a924a75f37c6a63ea0a405c17275672554`.
The ground `N=1` proof then failed with a meaningful residual showing the
mutated actual result `[1,4]` against the original obligation `[1,3]`. This is
valid body sensitivity, not an external-source-only mutation.

Evidence:

- [pinning_and_substitution.sh](evidence/pinning_and_substitution.sh) and
  [pinning_and_substitution.log](evidence/pinning_and_substitution.log)
- [verification-body-mutant.k](evidence/verification-body-mutant.k),
  [body-mutant-spec.k](evidence/body-mutant-spec.k),
  [run_body_sensitivity.sh](evidence/run_body_sensitivity.sh), and
  [body_sensitivity.log](evidence/body_sensitivity.log)

Constructor identity is therefore established. Semantic identity to the real
program is not: the exact body recurses 1100 levels, while the K configuration
has no bounded call stack or exception path.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is preserved in
[rule_inventory.md](evidence/rule_inventory.md), backed by
[static_inventory_scan.log](evidence/static_inventory_scan.log). It covers:

- every local syntax and configuration declaration;
- all 34 rules in `semantic.k`;
- all five macro/function equations in `verification.k`; and
- all six target claims in `spec.k`.

The submitted constructor set is completely mapped:

| Used constructor/operator | Declaration and behavior |
|---|---|
| `Module`, `FuncDef`, `Params` | module and exact-name function lookup |
| statement sequence, empty sequence | `exec`, `fellThrough`, and continuation rules |
| `If`, `Return` | condition selection, return propagation, and suffix handling |
| `Int`, `Name("n")` | `IVal` and exact argument lookup |
| `Compare`/`CmpOp("==")` | left-to-right integer equality |
| `BinOp` `+,-,*,%,//` | left-to-right evaluation and guarded reachable integer/list equations |
| singleton `ListExpr` | `LVal(cons(...,nil))` |
| named single-argument `Call` | argument evaluation, recursive lookup, and normal return |

No used construct is silently fabricated or left unmodeled. Ordinary
expression/statement order, return continuation, integer operations on the
reachable non-negative operands, and immutable list concatenation are sound.
`bin`, `append`, `triValue`, and `triPrefix` are functions but are not declared
`total`; their equations are guard-disjoint on every relevant overlap.
`verification.k` contains no opaque symbol, priority rule, simplification rule,
unconstrained oracle, or operational rewrite from program execution directly
to the desired answer. Its closed forms are truthful definitional summaries,
and the entry connection claim symbolically executes the exact body.

The material unsoundness is the generated call model:

- configuration line 43 has only `<k>`, with no stack depth or exception state;
- rules 65–72 enter function bodies without a runtime depth check; and
- rules 112–116 recursively call and unwrap only normal `returned` results.

For the submitted program these rules are exercised once per positive input
level. The required false-conclusion witness is `N=1100`: those rules enable
the normal-return configuration constrained by the entry claim, but real
CPython reaches `RecursionError`. This is an observable control/result
difference, not merely an unused off-path semantics gap. It violates the
generated-semantics requirement to soundly cover every material operation and
control effect used by the submitted program.

The hardcoded parameter/name handling and unguarded general spelling of some
partial operator rules are broader than a reusable Python semantics, but no
separate false witness arises from them on the exact submitted term and
`N >= 0`; they are recorded as scope limitations, not mislabeled as additional
unsoundness.

## 6. Fresh non-vacuity test

I created a distinct reviewer spec for satisfying input `N=3` and changed the
result-constraining last element from the true 8 to false 9. This is separate
from the body mutation.

The mutated spec's `kprove --dry-run` exited 0, proving it parsed and built.
The actual proof exited 1 with `WarnStuckClaimState`; the residual explicitly
contained the actual returned list `[1,3,2,8]` against the mutated destination
`[1,3,2,9]`. There was no parser error, missing import, timeout, or unrelated
crash. The candidate proof is non-vacuous.

Evidence:

- [spec-vacuity-audit.k](evidence/spec-vacuity-audit.k)
- [run_non_vacuity.sh](evidence/run_non_vacuity.sh)
- [non_vacuity.log](evidence/non_vacuity.log)

## 7. Proven versus assumed accounting

### What is machine-checked

Under the candidate's generated, idealized semantics:

- the exact submitted constructor tree is interpreted;
- for every mathematical integer `N >= 0`, its unbounded recursive execution
  is related coinductively to `triPrefix(N)`;
- the configured `run` wrapper has the same constrained result; and
- the closed-form sequence values satisfy the prompt's bases, even clause, and
  odd recurrence.

That is an honest theorem about the supplied K transition system. It is not
the requested theorem about all executions of the real submitted Python
program.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K 7.1.293 parser, kompilers, LLVM/Haskell backends, reachability logic, and circularity mechanism | All builds, concrete runs, and symbolic closure | Ordinary low-level proof-tool trust; acceptable. |
| Imported K `INT`, `BOOL`, `STRING`, builtin list syntax, and mathematical integer hooks | Guards, arithmetic, parser lists, and final values | Acceptable for the reached non-negative integer cases. |
| Trusted `py2mpy.py` | Source-to-constructor identity | Acceptable: trusted hash matched, fresh generation was byte-identical, and KORE pinning independently matched. |
| `triValue`/`triPrefix` equations | Entire postcondition | Acceptable inside K: guarded, disjoint, descending where recursive, mathematically true, and connected to exact K execution without an operational oracle. |
| Generated semantics-to-CPython bridge | Binding, calls, control, exceptions, and final result | **Illegitimate for the full contract.** It is informal, unproved, and concretely falsified by `N=1100` because it omits reachable recursion failure. |
| Trusted canonical implementation and reviewer recurrence oracle | Differential and adequacy evidence | Finite/executable evidence only; not substituted for the K proof. Both establish the concrete counter-witness and ordinary agreement. |
| Candidate generation records, prior `#Top`, and final report | None | Treated only as untrusted history; not relied upon. |

There are no candidate-local opaque result symbols or external empirical
primitives to account for.

### Gate and decision accounting

- Clean verification: **PASS** under the submitted theory.
- Program-term pinning: **PASS**.
- Result constraint and non-vacuity: **PASS**.
- Gate A real-program soundness: **FAIL**, with the concrete `N=1100`
  false-normal-return witness.
- Gate B intent/domain adequacy: **FAIL** because the HumanEval contract is
  unrestricted over non-negative integers and the semantics silently removes
  a reachable material control effect.
- Gate C reproducibility: reviewer evidence is present and reproducible, but it
  cannot repair Gates A and B.

Per the benchmark decision boundary, a proof that relies on materially unsound
semantics for a source-contract input is `FAIL / NOT_LEGIT`, even when its
internal `kprove` run prints `#Top`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
