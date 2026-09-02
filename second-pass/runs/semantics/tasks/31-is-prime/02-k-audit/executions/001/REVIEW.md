# Independent adversarial review: 31-is-prime

The candidate contains two useful, freshly reproducible reachability results: a result-bearing theorem for the loop tail and a result-bearing entry theorem for `N < 2`. It does **not** contain a result-bearing entry theorem for `N >= 2`. Its only large-input entry claim stops at the unevaluated `Assign/While/Return` suffix. Consequently, the candidate never proves that a large input returns `trialPrime(N, 2)`, `isPrimeSpec(N)`, or any other constrained result. This is a missing/non-constraining target theorem, not an audit-infrastructure failure.

The audit used the mandated `using-kit` and `validating-proof` procedures. All candidate material was treated as untrusted and read-only. Builds and experiments used `/tmp/audit-work/31-is-prime`; reviewer artifacts and bounded logs are under [`/audit-output/evidence`](/audit-output/evidence).

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and the trusted tree [`/reference/reference-semantics`](/reference/reference-semantics) is present. A recursive, non-dereferencing comparison against [`/candidate/reference-semantics`](/candidate/reference-semantics) exited 0. The candidate tree has exactly the same regular files/directories, with no missing, additional, mistyped, or symlinked entries. This satisfies the mode/mount boundary; there is no infrastructure breach and an ordinary candidate verdict is appropriate.

The exact inventory, hashes, type checks, and comparison statuses are in [`stage1-integrity.log`](/audit-output/evidence/stage1-integrity.log). The trusted baseline establishes source integrity only; it does not bless the proof-local rules in [`verification.k`](/candidate/verification.k:1).

### Prompt, translator, and generation records

The candidate [`prompt.py`](/candidate/prompt.py:1) is byte-identical to [`/reference/prompt.py`](/reference/prompt.py:1), and the candidate [`py2mpy.py`](/candidate/py2mpy.py:1) is byte-identical to the trusted translator. Both `cmp` checks exited 0.

Four requested generation/provenance artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured trace file was present. The candidate also contains a compiled archive and Python cache, but neither was copied or trusted. These missing records reduce provenance auditability, although the decisive verdict below follows from the proof sources themselves.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From the trusted [`prompt.py`](/reference/prompt.py:3) and [`canonical.py`](/reference/canonical.py:7), the entry point is `is_prime(n)`: on the intended integer domain, return `True` exactly when `n` is prime and `False` otherwise. In particular, every integer below 2 is non-prime. The documented examples are `6, 101, 11, 13441, 61, 4, 1`.

The submitted [`solution.py`](/candidate/solution.py:1) implements standard trial division: reject `n < 2`, test divisors beginning at 2 while `divisor² <= n`, reject on divisibility, and otherwise return true. Over mathematical/Python integers this is extensionally equivalent to the trusted canonical implementation, which tests a larger but sufficient divisor interval.

### Trusted translation

The trusted translator regenerated `solution.mpy` from the scratch copy of `solution.py`. Translation exited 0; byte comparison against the submitted [`solution.mpy`](/candidate/solution.mpy:1) exited 0. Both `.mpy` files have SHA-256:

`870a9890935eca71a5ef2604103b07f703ec76b9fd3fcae0600d75d3d8964e7d`

Commands and statuses are preserved in [`stage2-regeneration.log`](/audit-output/evidence/stage2-regeneration.log).

### Independent differential test

[`differential_test.py`](/audit-output/evidence/differential_test.py) independently imported `/reference/canonical.py` and the scratch copy of the submitted `solution.py`. Its corpus contained:

- all seven documented examples;
- negative, zero, one, and first-loop boundaries;
- perfect-square guard equalities and immediate/later divisor cases;
- every integer from `-50` through `500`;
- 300 deterministic generated integers using seed `31031`.

There were 839 unique inputs and zero mismatches, including result types. The exact input groups and ordered corpus are in [`differential-inputs.json`](/audit-output/evidence/differential-inputs.json); complete per-input results are in [`differential-results.json`](/audit-output/evidence/differential-results.json). The command exited 0; see [`stage2-differential.log`](/audit-output/evidence/stage2-differential.log). This is finite implementation-fidelity evidence, not a substitute for a K theorem.

## 3. Clean proof reconstruction

The scratch tree was populated from trusted semantics/translator/reference sources and the candidate's source proof/program files only. Candidate-provided compiled definitions, caches, and archives were not reused. The live toolchain was:

- `/usr/bin/kompile`, `/usr/bin/kprove`, `/usr/bin/krun`
- K `v7.1.337`, build date June 18, 2026
- Python `3.10.12`

See [`stage3-toolchain.log`](/audit-output/evidence/stage3-toolchain.log) and [`source-hashes.log`](/audit-output/evidence/source-hashes.log).

### Concrete definition

The LLVM definition was freshly built from trusted `reference-semantics/semantics.k` with main module `MPY-KRUN`. Build exit was 0. The compiler reported non-exhaustive total-function warnings, addressed in stage 5.

An independent translated harness containing the exact submitted function body, all prompt examples, and additional entry/loop boundaries ran under `krun` and finished with `.K`, `NoExc`, and exit code 0. Evidence:

- source: [`concrete_harness.py`](/audit-output/evidence/concrete_harness.py)
- translation: [`stage3-harness-translate.log`](/audit-output/evidence/stage3-harness-translate.log)
- build: [`stage3-llvm-build.log`](/audit-output/evidence/stage3-llvm-build.log)
- execution: [`stage3-concrete-run.log`](/audit-output/evidence/stage3-concrete-run.log)

### Haskell proof definitions and positive claims

Both proof definitions were freshly compiled from source. Every submitted positive label was run independently:

| Target | Exact proof result |
|---|---|
| `LOOP-SPEC` module | exit 0, `#Top` |
| `loop-correct` alone | exit 0, `#Top` |
| `SPEC` module | exit 0, `#Top` |
| `entry-small` alone | exit 0, `#Top` |
| `entry-large-prefix` alone | exit 0, `#Top` |

The proof-base and public-definition builds exited 0; see [`stage3-proof-base-build.log`](/audit-output/evidence/stage3-proof-base-build.log) and [`stage3-proof-build.log`](/audit-output/evidence/stage3-proof-build.log). Proof outputs are in:

- [`stage3-kprove-loop-module.log`](/audit-output/evidence/stage3-kprove-loop-module.log)
- [`stage3-kprove-loop-individual.log`](/audit-output/evidence/stage3-kprove-loop-individual.log)
- [`stage3-kprove-spec-module.log`](/audit-output/evidence/stage3-kprove-spec-module.log)
- [`stage3-kprove-entry-small.log`](/audit-output/evidence/stage3-kprove-entry-small.log)
- [`stage3-kprove-entry-large-prefix.log`](/audit-output/evidence/stage3-kprove-entry-large-prefix.log)

Thus the submitted claims close under the submitted theory. Their scope is the issue.

## 4. Adequacy and real-program pinning

### Plain-language claim scope

| Claim | Precondition | Actual postcondition |
|---|---|---|
| `loop-correct` ([`spec.k:9`](/candidate/spec.k:9)) | `D >= 2`; distinct live/caller scope locations; fresh map keys; a function frame whose locals contain `n=N` and `divisor=D` | Execute the exact remaining while loop, trailing `return True`, and `#endcall`; return `trialPrime(N,D)` to the saved continuation while restoring/removing the ordinary call frame. |
| `entry-small` ([`spec.k:52`](/candidate/spec.k:52)) | `N < 2` in an explicit prepared `is_prime` call frame | Execute the exact body and return `false`, popping the call frame and local scope. |
| `entry-large-prefix` ([`spec.k:97`](/candidate/spec.k:97)) | `N >= 2`, local scope 1 contains `n=N`, and the framed map lacks key 1 | Evaluate only the initial `if` and reach `Assign(divisor,2); While(...); Return(true); #endcall`. No assignment, loop, return, frame pop, or result occurs in the destination. |

The depth-0 diagnostic confirms that K completes the large-prefix source with `<env>1</env>` while leaving the other omitted cells symbolic; see [`stage4-entry-large-depth0.log`](/audit-output/evidence/stage4-entry-large-depth0.log).

### Program identity

An independent parser expanded `#entryBody`, `#primeCond`, and `#primeLoopBody` and compared them structurally with the trusted regeneration of `solution.mpy`. All three comparisons were true. See [`program_pinning_check.py`](/audit-output/evidence/program_pinning_check.py) and [`stage4-program-pinning.log`](/audit-output/evidence/stage4-program-pinning.log).

Therefore no substituted body or loop was found: the terms executed by the claims are exact syntax copies of the submitted function body. However, no K source `requires` or parses `solution.mpy`, and no target claim executes the submitted `Module(FuncDef(...))` followed by an actual `Call`. Program identity depends on this external structural check and prepared-call-state reasoning rather than a direct source inclusion theorem.

### Satisfiable witnesses and ground results

Each precondition is satisfiable:

- `entry-small`: `N=1` with the explicit builtins/global/local maps and frame written in the claim.
- `entry-large-prefix`: `N=31`, `SC=.Map`; K completes the current environment as location 1.
- `loop-correct`: `N=31`, `D=2`, `L=1`, `CALLER=0`, `SC=.Map`, an arbitrary global scope at 0, the specified local scope at 1, and the specified saved frame.

A second loop witness, `N=9, D=2`, gives the distinct false result. For `N=31,D=2`, `trialPrime` is true and both Python implementations return true; for `N=9,D=2`, all return false; for `entry-small` at `N=1`, all return false. The witness artifact is [`claim-witnesses.json`](/audit-output/evidence/claim-witnesses.json), produced by [`claim_witnesses.py`](/audit-output/evidence/claim_witnesses.py); the command exited 0 in [`stage4-claim-witnesses.log`](/audit-output/evidence/stage4-claim-witnesses.log).

For `entry-large-prefix` at `N=31`, both Python implementations return true, but there is no formal claimed result to substitute or compare.

### Material adequacy failure

There is no claim of the form “the actual entry body returns `trialPrime(N,2)` for `N >= 2`,” nor a universal claim returning `isPrimeSpec(N)`. `isPrimeSpec` is declared in [`verification.k:52`](/candidate/verification.k:52) but never occurs in any claim. `LOOP-SPEC` is proved separately; `SPEC` neither imports that proof module nor contains a result-bearing composition claim. The fixed assignment/while steps and mathematical transitivity may suggest how to write the missing theorem, but an informal suggested composition is not the required K reachability proof.

The large-domain target is therefore missing/non-constraining even though its prefix claim prints `#Top`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`k_inventory.py`](/audit-output/evidence/k_inventory.py) inventoried the supplied `semantics.k`, every helper K file, `verification.k`, and `spec.k`. The line-addressable full inventory is available as [`rule-inventory.txt`](/audit-output/evidence/rule-inventory.txt) and [`rule-inventory.json`](/audit-output/evidence/rule-inventory.json).

It contains 1,123 records:

- 705 rules;
- 232 syntax declarations;
- 5 contexts;
- 1 configuration;
- 3 claims;
- 29 modules, 29 endmodules, 90 imports, and 29 file requirements.

Recorded attributes include 148 function declarations, 107 total declarations, 25 symbols, 22 `no-evaluators` declarations, 45 priority-bearing records, 38 concrete rules, 26 `owise` rules, 7 macros, and 1 recursive macro. There are no local `[functional]` declarations and no local `[simplification]` rules.

Every inventory record has a disposition and justification in [`rule-review-dispositions.csv`](/audit-output/evidence/rule-review-dispositions.csv), generated by [`rule_dispositions.py`](/audit-output/evidence/rule_dispositions.py). The disposition run reviewed all 1,123 records and found no unexpected proof-local rule; see [`stage5-dispositions.log`](/audit-output/evidence/stage5-dispositions.log). The full special-attribute search is preserved in [`stage5-special-attributes.log`](/audit-output/evidence/stage5-special-attributes.log).

### Mapping of used constructs

| Submitted construct | Declaration/evaluation path |
|---|---|
| `Module`, statement list | `syntax.k`; `core.k` `#loadAll`, statement sequencing, `.Stmts` |
| `FuncDef`, `Params`, prepared calls | `syntax.k`; `functions.k` closure/frame lifecycle; `call.k` invocation and parameter binding |
| `Name` | `core.k` current-environment lookup and parent-scope walk |
| `Int`, `Bool` | `core.k` literal rules |
| `If` | strict condition in `syntax.k`; `controls.k` `truthy`/`#branch` |
| `Compare(<,<=,==)` | left/right contexts in `operators.k`; integer cases in `int.k` |
| `Assign(Name,...)` | strict RHS; `controls.k` current-scope update |
| `While` | `controls.k` `#while`, condition reevaluation, body, and loop label |
| `BinOp(*,%)` | sequential left-to-right strictness; `operators.k`; integer multiplication and `pyMod` |
| `AugAssign(+,1)` | strict RHS; current binding read; integer addition; scope update |
| `Return` | strict value evaluation; `functions.k` abrupt return, frame pop, environment/scope restoration |

For this integer-only body, values are unbounded K integers, matching Python integer arithmetic. The condition and operand rules preserve the program's evaluation order. The while condition is reevaluated each iteration. `Return` discards the in-function continuation and restores the saved continuation/frame, as required. No heap allocation or external state is used by the body.

### Proof-local extensions

1. **Map deletion rules, `verification.k:9-12`.** These are sound finite-map identities: deleting an absent key is identity, and deleting a freshly/disjointly added key restores the original map. Guards exclude overlap with an existing key. They assist frame removal; they do not determine the Boolean result.

2. **`#primeCond`, `#primeLoopBody`, `#entryBody`, `verification.k:16-38`.** These are pure macro abbreviations. The structural program-pinning check establishes exact equality to the submitted translated syntax after expanding `.Stmts` units. They neither bypass nor summarize execution.

3. **`trialPrime`, `verification.k:44-50`.** The three guarded equations are pairwise disjoint on the claim domain `D >= 2`: stop true once `D²>N`, stop false when `D` divides `N`, otherwise recurse at `D+1`. Recursion descends on the finite distance to the first `D` with `D²>N`. The program evaluates Python-style `pyMod`, while the summary tests K `%Int`; for positive `D`, equality to zero is equivalent, which is the only observation used. At `D=0` with some `N`, the function is intentionally not covered, but it is not declared total and that state is excluded by `loop-correct`. This is a coverage limitation, not a false equation.

4. **`isPrimeSpec`, `verification.k:52-54`.** The guards partition integers below/above 2. On the large branch, standard factor-pair mathematics shows that a composite has a divisor no greater than its square root, so `trialPrime(N,2)` characterizes primality. The definition is sound, but no reachability claim depends on it.

There is no proof-local operational bridge, oracle, opaque result, priority rule, simplification, or totality assertion. The result-bearing summary `trialPrime` is connected to exact fixed-semantics loop execution by the freshly closed universal `loop-correct` claim and has ground witnesses with opposite outcomes.

### Supplied-semantics boundaries

The supplied proof module imports many syntax-disjoint facilities. The 22 explicit `no-evaluators` opaque primitives are the float family (`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`), sorting (`sortVS`, `sortKeyVS`), and `md5hexCodes`. None is reachable from `solution.mpy` or any submitted destination.

Fresh builds warned that `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt` are not exhaustive over their full declared total sorts. These are narrower evidence/coverage gaps in unused facilities. No source term, proof-local function, branch, result, state, or postcondition in this task can contain them. I therefore do not label them unsound without a false conclusion witness on the intended program domain.

No materially unsound proof-local rule was found. The candidate fails because its large-input target result is absent, not because an identified false rule proves it.

## 6. Fresh non-vacuity test

The fresh mutation [`spec-vacuity.k`](/audit-output/evidence/spec-vacuity.k) changes the result-bearing `entry-small` destination from `false` to `true`, fixes the saved continuation to `.K`, and retains the satisfiable precondition `N < 2`. The concrete witness is `N=1`, for which the trusted canonical and submitted Python functions both return false.

The mutation dry-run compiled successfully: exit 0 in [`stage6-vacuity-dry-run.log`](/audit-output/evidence/stage6-vacuity-dry-run.log). The actual proof exited 1 with `WarnStuckClaimState`. Its final configuration contains `<k>false ~> .K</k>`, which cannot unify with the demanded `true`; see [`stage6-vacuity-proof.log`](/audit-output/evidence/stage6-vacuity-proof.log). This is failure for the intended unmet Boolean obligation, not a parser error, missing import, timeout, or unrelated crash.

This establishes discrimination of the small-input result-bearing theorem. It cannot rescue or test the large-input entry result, because the submitted large-prefix claim has no result obligation to mutate.

## 7. Proven versus assumed accounting

### What is machine-proved

Under the supplied MPY semantics plus the reviewed proof-local definitions:

1. From the exact loop-tail configuration and `D >= 2`, the loop/trailing return restores the call frame with result `trialPrime(N,D)`.
2. From the exact prepared call-body configuration and `N < 2`, the function restores the frame with result `false`.
3. From the large-prefix configuration and `N >= 2`, the initial `if` is skipped and the remaining `Assign/While/Return` syntax is exposed.

Item 3 does not state or establish the function's returned value.

### Trusted or informal boundaries

- **K implementation and builtin theories:** `kprove`/Haskell reachability, LLVM concrete execution, K integers, Booleans, Maps, Lists, and equality are foundational toolchain trust.
- **Supplied MPY semantics:** integrity-checked against the trusted mount and statically inventoried. It models the constructs used here; unused partial/opaque facilities are excluded from the theorem's operational path.
- **Translator/program bridge:** byte-identical trusted regeneration plus structural macro comparison supports that the copied K body is the submitted program body. The K claims themselves do not load `solution.mpy`.
- **Prepared-call bridge:** entry/loop claims assume an already-created call frame and local binding. Module loading and the actual `Call` transition are concretely tested but not included in a target reachability theorem.
- **Trial-division mathematics:** the equivalence between searching divisors through the square root and mathematical primality is ordinary mathematical reasoning encoded by `isPrimeSpec`; it is true but not connected to a universal entry claim.
- **Opaque supplied symbols:** the 25 supplied `symbol` declarations and the listed opaque/total facilities are unused by the submitted program and claims.
- **Empirical evidence:** 839 Python differential inputs and the K concrete harness support implementation and semantics bridges only on tested cases. They do not provide the missing universal entry theorem.
- **Generation provenance:** the four requested generation records are absent, so no generation-history claim is relied upon.

### Decision

Fresh `#Top` results validate exactly the three submitted reachability claims, not the natural-language task theorem. Because every intended integer `N >= 2` is covered only by a prefix claim whose postcondition contains no returned value, the candidate is missing the material large-domain partial-correctness obligation. The separate loop theorem and unused `isPrimeSpec` definition are ingredients for a proof, not a submitted result-constraining entry proof.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
