# Independent adversarial review: 59-largest-prime-factor

This review treats every candidate and generation artifact as untrusted
evidence. All execution used source files copied to
`/tmp/audit-work/59-largest-prime-factor`; no candidate-provided compiled
definition or cache was used.

## 1. Input and provenance integrity

The launcher declares `record_layout: legacy-selected-stage1`,
`condition: bare`, and `semantics_mode: GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent, as this mode requires. I did not
search for or use a hidden reference semantics.

The campaign object in `/audit-input.json` is exactly equal as parsed JSON to
`/audit-campaign-lock.json`. The lock's SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the recorded value. All declared provenance mounts and every record
required by the historical layout are real readable files/directories, not
symlinks. `runtime-metrics.json` is absent, but is not required for
`legacy-selected-stage1`; historical runtime observations must not be
reconstructed. The optional historical `usage.json` is present and was
inspected.

I read `/run.json`, `/task.json`, `/generation-result.json`, the invocation and
metrics records, the optional usage record, both Codex text records,
`prompt.txt`, the legacy records, and all 111 JSON events in the structured
trace. The trace parses completely. Those records claim a successful
generation run, but that claim was not used as proof evidence.

Every recorded regular-file hash checked by
`evidence/integrity_check.py` matches its mounted bytes, including the single
trace file and the legacy records listed in `generation-result.json`. The
independent pipeline tree digest of `/candidate` is
`ba4c8447536b3f27b64485e5aa5c2f7d6faa5413937c936e76ba53320540478e`,
matching both the retained workspace binding and stage-1 output binding. The
independent trace tree digest is
`63d4f1ebb780019513f2db0669b48e1dc99ee62b680f5fb1dbd4ca8c89e2c4a4`,
matching `usage.json`; the trace file itself matches its separately recorded
`004aff...` hash. The two launcher-level aggregate fields in
`audit-input.json` use an untagged launcher digest rather than the recorded
pipeline-v2 tree digest, so the independently reproducible stage-layout tree
bindings and every constituent file hash were used for mount verification.
There is no content discrepancy.

Candidate `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. The immutable candidate tree
contains exactly eight regular files: prompt, translator, Python solution,
translated program, generated semantics, verification module, spec, and proof
script. There are no candidate-built definitions or caches in the mount.

Evidence: `evidence/integrity_check.py`, `evidence/integrity.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt asks `largest_prime_factor(n: int)` to return the largest
prime factor of `n`, assuming that `n > 1` and `n` is composite. The documented
examples are 13195 → 29 and 2048 → 2. The intended domain is the unrestricted
set of composite mathematical integers greater than 1. Because the argument is
a scalar integer, there is no meaningful “empty” value; the smallest
contract-valid boundary is 4.

The trusted canonical implementation scans every divisor from 2 through `n`
and keeps the largest divisor that passes its local primality test. The
candidate instead starts at factor 2, repeatedly divides the residual `n` when
the factor divides it, and otherwise increments the factor; when
`factor * factor > n`, it returns the residual. This is a different but
standard trial-division algorithm. It does not bound the input, special-case
the examples, or narrow the contract domain.

### Translation identity

Running the trusted translator on the copied `solution.py` exits 0. The
regenerated and submitted `solution.mpy` files are byte-identical and both have
SHA-256
`db068bfdeddf4555800505c6781d12cabba9f862bbe376347326aeec08e2c591`.

### Independent differential test

`evidence/differential_test.py` independently loads the trusted canonical and
candidate entry points and compares both with a third trial-factor oracle. It
checks:

- the smallest composite and exact factor-square boundary;
- both divisibility branch outcomes, repeated factors, powers, squares, and
  semiprimes;
- the two prompt examples;
- every composite in `[4, 4999]`;
- 256 seeded products beyond that exhaustive range; and
- a bounded prime sample because the formal claim is broader than the source
  contract.

The run covered 4,528 distinct integers with zero mismatches. This is finite
fidelity evidence, not a universal proof.

Evidence and exact commands: `evidence/run_stage2.sh`,
`evidence/stage2.log`, `evidence/differential_test.py`.

## 3. Clean proof reconstruction

K reports version 7.1.293. I copied only source artifacts to scratch and created
new output directories. A concrete definition was compiled from `semantic.k`
alone:

```text
kompile semantic.k --backend haskell --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --output-definition .../semantic-kompiled
```

It exited 0. Fresh `krun` executions of the actual submitted `solution.mpy` for
4, 6, 9, 15, 2048, and 13195 all exited 0 with empty `<k>` cells and results
2, 3, 3, 5, 2, and 29 respectively, matching independent Python.

A separate proof definition was compiled from `verification.k`, which imports
the generated semantics:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition .../verification-kompiled
```

It exited 0. Positive proof reconstruction produced:

| Target | Selection | Exit | Output |
|---|---|---:|---|
| loop refinement | `SPEC.loop-refines-lpf` | 0 | `#Top` |
| universal entry theorem | loop helper plus `SPEC.largest-prime-factor-correct` | 0 | `#Top` |
| example 13195 | `SPEC.prompt-example-13195` | 0 | `#Top` |
| example 2048 | `SPEC.prompt-example-2048` | 0 | `#Top` |
| all four aggregate | no filter | 0 | `#Top` |

The universal entry theorem depends on the loop claim as a circularity.
Selecting only the entry label removes that helper under K's `--claims`
semantics and causes unbounded loop unfolding; I interrupted that diagnostic
run rather than represent it as a target failure. The valid independent entry
command retains the exact helper dependency and closes. The aggregate
candidate command also closes from the fresh definition.

Evidence and exact bounded output: `evidence/run_stage3.sh`,
`evidence/stage3.log`, `evidence/run_stage3_targets.sh`,
`evidence/stage3-targets.log`.

## 4. Adequacy and real-program pinning

### Claims in plain language

`loop-refines-lpf` starts with the real translated loop followed by the real
last-position return, an environment containing exactly `factor = F` and
`n = N`, no result, `N > 1`, and `F >= 2`. It says termination consumes the
computation, leaves some integer factor, sets both local `n` and the result to
`lpfSpec(N,F)`, and preserves the framed input.

`largest-prime-factor-correct` starts the submitted entry module with input
`N`, an empty environment, and no result, for every integer `N > 1`. It says
termination consumes the computation and sets local `n` and the result to
`lpfSpec(N,2)`; only the final local `factor` is existential.

The example claims start the same module at the two fixed prompt inputs and
require fixed results 29 and 2. Their final local environments are irrelevant
and existential.

All preconditions are satisfiable. For example, the loop state with
`N = 15`, `F = 2`, any integer input cell, exactly the two named environment
bindings, and `noResult` satisfies the loop precondition. The entry state with
`N = 15`, empty env, and `noResult` satisfies the entry precondition. Concrete
K execution, candidate Python, and canonical Python all return 5 for that
witness. The fixed example states are also directly realizable.

### Constructor-level program identity

The trusted translation check pins `solution.py` to `solution.mpy`. I then used
the fresh proof definition to parse and expand macros for both:

1. the submitted `solution.mpy`; and
2. the `solutionModule` term that occurs in every entry claim.

The resulting KORE files are byte-identical, both 4,394 bytes, with SHA-256
`df782079940f921a5d1c4d52ddb4b87b719deb22723e17da4e7c65fd8a3b0394`.
Thus the omitted source file read is replaced by a mechanical constructor-level
identity check, not an informal visual comparison. `factorLoop` expands inside
that identical term.

The loader rule does not replace any computation with `lpfSpec`. It binds the
input to the function's sole parameter and executes every submitted statement
and expression through the generated rules. `lpfSpec` occurs only in proof
postconditions and the definitional equations used to match real loop steps.

### Body sensitivity

In scratch I changed the increment in both the claim-executed macro and the
mechanically compared mutated constructor term from `factor + 1` to
`factor + 2`. The two mutated expanded terms remained mechanically identical.
Concrete generated-semantics execution on 13195 then returned 13195, not 29,
and the fixed-result proof exited 1 with `WarnStuckClaimState`, showing the
actual residual configuration and `result(13195)`. This changes the program
term executed by the claim; it is not a mutation of an ignored external file.

### Adequacy limitation

The result is constrained, not free: the universal claims require exact
equality to `lpfSpec`, and the examples require exact integers. However, no K
claim states or proves primality, divisibility of the original input, or
maximality among prime divisors. The name and comment attached to `lpfSpec` do
not establish those facts. The formal result-to-source-contract bridge is an
ordinary number-theoretic argument, supported by differential evidence but not
machine checked in K. This is the principal non-fatal concern.

Evidence: `evidence/run_pinning_check.sh`, `evidence/pinning.log`,
`evidence/run_body_sensitivity.sh`, `evidence/body-sensitivity.log`.

## 5. Rule-by-rule static soundness review

`evidence/rule-inventory.md` is the exhaustive inventory. It enumerates every
local syntax production, configuration cell, function attribute, semantic
rule, proof helper, macro, and claim. There are no other local K files.

### Generated semantics

The local declarations cover `Module`, `FuncDef`, `Params`, statement lists,
assignment, while, if, return, integer/name/binop/compare expressions, the
comparison list, result values, `evalInt`, `evalBool`, and the three internal
execution items. The configuration contains only `<k>`, `<input>`, `<env>`,
and `<result>`; every cell is used.

The 18 semantic rules are:

- S1–S6: integer literal, name lookup, `+`, `*`, guarded `//`, and guarded `%`;
- S7–S8: one-element integer `<=` and `==` comparisons;
- S9: exact entry-module loading and parameter binding;
- S10–S11: empty and nonempty statement sequencing;
- S12–S13: RHS evaluation followed by map update;
- S14–S15: disjoint true/false if branches;
- S16–S17: disjoint true/false while branches; and
- S18: return-value evaluation.

All submitted constructors map to one of these declarations and rules. The
submitted program has no heap, calls inside the body, exceptions, I/O,
allocation, break/continue, or other unmodeled effect. Expressions are pure,
so the direct recursive evaluator preserves every material evaluation-order
fact. On the claimed positive domain all operands and divisors are positive;
K's unbounded integer arithmetic and division/modulo agree with Python there.
The assignment rules read the old map before updating it. If and while guards
are disjoint and exhaustive for the two supported comparison forms.

S9 is a deliberately narrow entry harness, not general Python function/module
semantics. It matches the exact sole function name, parameter, and body, starts
only from an empty environment, and then executes the body. It does not encode
an answer or summarize a property-bearing operation.

S18 is globally over-broad as Python semantics because it sets the result but
does not discard a nonempty continuation. A preserved witness,
`return-followed.mpy`, uses contract-valid input 4 with `return 1` followed by
`return 2`: K exits with a residual second return after recording result 1,
whereas Python terminates at the first return. This is a concrete language-model
counterexample, not a witness against the submitted theorem: the immutable
function has its only return last, its reachable continuation is just the
empty statement sequence, and the loop helper uses the same exact context.
Therefore the rule is faithful on every submitted reachable return state but
limits reuse of the semantics.

### Verification extensions

The only result-bearing proof helper is
`lpfSpec(Int,Int) [function]`. It is not opaque and not declared `total`.
Its three equations exactly mirror loop exit, divisible, and nondivisible
steps. Their guards are pairwise disjoint. For `N > 1`, `F >= 2`, they cover
every loop state and recursive calls preserve that domain. Divisible steps
strictly reduce positive `N`; nondivisible steps increase `F` toward the exit
guard. No semantic rule rewrites the submitted loop to `lpfSpec`; equality is
established by executing one real loop step and applying the loop circularity.

The two `[macro]` rules only name constructor trees. Fresh macro expansion
proved their program identity. They do not survive as answer-producing
operational bridges.

There are no candidate-local `total`, `functional`, `simplification`,
priority, `owise`, or `concrete` attributes; no opaque/fresh value symbols; no
proof-local operational rules; no task-answer axiom; and no oracle. The only
claims are the four inventoried reachability claims.

I do not label any rule used by the submitted proof materially unsound. The
one concrete false-behavior witness is confined to an unreachable
return-with-suffix context and is reported as the narrower generated-language
coverage limitation required by the evidence.

Evidence: `evidence/rule-inventory.md`,
`evidence/run_return_limitation.sh`, `evidence/return-followed.log`.

## 6. Fresh non-vacuity test

I ignored any generation-time validation claim and authored a fresh
`spec-vacuity.k` in scratch. It executes the unchanged real
`solutionModule` from the satisfiable initial state with input 13195, but
changes the result obligation from 29 to the deliberately false value 30.

`kprove --dry-run` exited 0, establishing successful parsing/building of the
mutated claim. The actual proof exited 1 with `WarnStuckClaimState`. Its
residual is the fully terminated real execution with local `n = 29` and
`result(29)`, which does not unify with the required `result(30)`. This is the
expected unmet result obligation, not a parser error, missing import, timeout,
or unrelated crash.

Evidence: preserved `evidence/spec-vacuity.k`,
`evidence/run_nonvacuity.sh`, `evidence/nonvacuity.log`.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the candidate's generated semantics and K's built-in integer/Boolean/map
theories, for every mathematical integer `N > 1`, if the exact submitted
constructor program terminates from the modeled entry configuration, its
`<result>` and final local `n` equal the recursively defined
`lpfSpec(N,2)`. The loop claim establishes the corresponding statement for
every residual `N > 1` and factor `F >= 2`. The two fixed examples additionally
establish exact results 29 and 2.

This is genuine partial correctness over an unrestricted domain; it is not a
finite unrolling or a theorem only about the examples. Because the source
contract excludes primes, the formal `N > 1` domain is broader, not narrower.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K 7.1.293 compiler, Haskell backend, reachability logic | All builds and proofs | Standard unavoidable proof-tool trust. |
| Imported `INT`, `BOOL`, `MAP` operations | Arithmetic, guards, and environment updates | Acceptable primitive trust; reachable positive arithmetic agrees with Python and concrete tests. |
| Trusted `py2mpy.py` | Python-source to constructor bridge | Acceptable launcher-supplied bridge; byte identity was independently checked. |
| Exact entry loader S9 | Models calling the submitted sole function with integer `N` | Acceptable narrow harness bridge here: exact binding and body execution, no skipped material effect. |
| Generated last-position return semantics | Final control/result | Sound on every submitted reachable context; globally non-general, as the preserved suffix witness shows. |
| `lpfSpec` equals the largest-prime-factor mathematical function | Human-facing meaning of the K postcondition | True by the standard trial-division invariant, but not formally proved in K. Finite differential evidence covers 4,528 inputs only. This is the main concern. |
| Termination | Source contract normally expects a returned value | Outside partial correctness. The transition equations have an evident decreasing/progress argument on the claimed domain, but no separate termination theorem is claimed. |

There are no local opaque symbols, empirical execution oracles inside the K
theory, unconstrained result-bearing values, or proof rules that assume the
task answer. `PROOF.md`, generation traces, previous `#Top` output, and finite
tests were not substituted for the reconstructed reachability proof.

### Decision

Gate A (real-program soundness and non-vacuity) passes: fresh proofs close,
the constructor term is pinned mechanically, the result is constrained, body
sensitivity is demonstrated, and the false result is rejected. The material
source-contract domain is fully covered. The proof remains legitimate because
no false conclusion about the submitted program is enabled by its rules.

I select `CONCERNS / LEGIT`, rather than `PASS`, because the K theorem stops at
the recursive execution summary and leaves its “largest prime factor” meaning
to an informal mathematical bridge, and because the individually generated
return semantics is intentionally reliable only in the submitted
last-position context. Neither limitation narrows the HumanEval domain,
substitutes another program, or makes the proved execution/result claim false.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
