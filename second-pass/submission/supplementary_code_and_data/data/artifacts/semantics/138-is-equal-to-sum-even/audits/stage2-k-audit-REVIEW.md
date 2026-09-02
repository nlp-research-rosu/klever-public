# Independent adversarial review: 138-is-equal-to-sum-even

Conclusion: the candidate contains a legitimate, reconstructed partial-correctness proof for every intended integer input. The proof executes the submitted function body through the supplied semantics and constrains the returned Boolean exactly. I assign `CONCERNS / LEGIT`, rather than `PASS`, because the last bridge from the proved arithmetic characterization to the prompt's existential “sum of exactly four positive even numbers” wording is an elementary but informal mathematical argument, not a K claim. The manually duplicated entry wrapper is also an artifact-maintenance risk, although constructor-level comparison removes it as a soundness defect for this immutable candidate.

All candidate prose, prior logs, compiled artifacts, and generation claims were treated as untrusted. The executable reconstruction used only source copied to `/tmp/audit-work/reconstruction`; reviewer artifacts and bounded logs are in `/audit-output/evidence`.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `138-is-equal-to-sum-even`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- a mounted trusted semantics tree at `/reference/reference-semantics`.

This is internally consistent: the trusted semantics tree is present, so the rendered semantics mode does not create an infrastructure breach.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`, `/generation-result.json`, and all records required for `legacy-selected-stage1`: `invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace. `usage.json`, `legacy-metrics.json`, and `legacy-run-input.json` were also present and inspected. Historical runtime metrics are not required for this legacy layout and were not reconstructed.

The structured trace contains one regular JSONL file and 159 parseable records. Its assistant result merely claims prior success; it was not used as proof evidence. See:

- `/audit-output/evidence/trace_summary.py`
- `/audit-output/evidence/trace-summary.log`

The campaign lock object is exactly equal to the `audit_campaign` block, and its SHA-256 is the recorded `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.

Independent direct hashes matched for the trusted canonical, prompt, translator, run/task/result manifests, invocation, metrics, usage, prompt, Codex last message, Codex output, and every trace/evidence leaf declared by `generation-result.json`. Independently reconstructed manifest-tree digests also matched:

- candidate workspace: `49f59135d1f71d82f06bdc57acc8756409eb461251261f35fd94e471b6a1d1b7`;
- trusted and candidate semantics: `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- structured trace: `0a5e29407e1aaf66c5bbba3652cbf766ce41ec6653ff1573bcd342215753f438`.

The audit manifest also contains compatibility digest fields whose encoding is not identified by the record itself. I did not use those values as an algorithm oracle. Instead, I checked the mounted data through direct file hashes, the record-declared leaf hashes, canonical manifest-tree hashes, and recursive entry-by-entry comparison.

The candidate prompt and translator are byte-identical to `/reference/prompt.py` and `/reference/py2mpy.py`. Recursive comparison of `/candidate/reference-semantics` against `/reference/reference-semantics` found zero differences. Both trees contain only real directories and regular files: no missing, extra, changed, mistyped, special, or symlinked entry was found. This satisfies the stricter supplied-semantics integrity boundary.

Reproducible evidence:

- `/audit-output/evidence/provenance_check.py`
- `/audit-output/evidence/provenance.log`

Stage result: PASS. There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The prompt asks whether integer `n` can be represented as the sum of exactly four positive even integers. Such a sum is necessarily even and at least 8. Conversely, every even `n >= 8` has the representation:

`n = 2 + 2 + 2 + (n - 6)`,

where `n - 6` is positive and even. Therefore the intended Boolean is `n >= 8 and n % 2 == 0`.

The trusted canonical returns `n % 2 == 0 and n >= 8`. The candidate returns `n >= 8 and n % 2 == 0`. For integer inputs these are equivalent. The changed evaluation order has no exceptional or stateful effect on the intended integer domain.

### Trusted regeneration

Running the trusted translator in scratch:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

exited 0. `cmp -s regenerated-solution.mpy submitted-solution.mpy` also exited 0. Both files have SHA-256 `4be6b3778909ca1c91506046bb2f1925cb4f689dad0162b5f8faa007e84eee8d`. Thus submitted `solution.mpy` is byte-identical to trusted regeneration.

### Independent differential test

`/audit-output/evidence/differential_test.py` imports the trusted canonical and scratch candidate independently. It tested:

- documented examples `4, 6, 8`;
- threshold/parity boundaries and negative/zero cases;
- every integer in `[-10000, 10000]`;
- six huge positive/negative boundaries;
- 5,000 deterministic generated integers in `[-10^30, 10^30]`.

The scalar contract has no meaningful empty input. The test ran 25,022 cases and found zero result or Boolean-type mismatches.

Reproducible evidence:

- `/audit-output/evidence/program_fidelity.sh`
- `/audit-output/evidence/program-fidelity.log`
- `/audit-output/evidence/differential_test.py`

Stage result: PASS for the intended mathematical-integer domain. Non-integer Python objects are outside the formal claim and the natural meaning of “even number” used here.

## 3. Clean proof reconstruction

No candidate-built definition or cache was used. I copied:

- the trusted reference semantics from `/reference/reference-semantics`;
- the trusted translator;
- candidate source files `solution.py`, `solution.mpy`, `verification.k`, and `spec.k`;

to `/tmp/audit-work/reconstruction`.

The following fresh commands were run:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled

krun concrete-audit.mpy --definition runtime-audit-kompiled

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition verification-audit-kompiled

kprove spec.k --definition verification-audit-kompiled --spec-module SPEC
```

Both builds exited 0. The concrete program contains the exact candidate body plus assertions at `4, 6, 7, 8, 9, 10, 11, -2, 0, 100, 101`; it reached an empty `<k>` cell with `<exit-code> 0 </exit-code>`. The proof definition's main module is `VERIFICATION`, and it does not contain the concrete-only `MPY-CONCRETE` rules.

The original four-claim `spec.k` printed `#Top` and exited 0. To avoid relying on a single aggregate signal, I put each unchanged claim in its own spec module and ran each independently. All four printed `#Top` and exited 0:

| Claim | Evidence |
|---|---|
| universal exact result | `/audit-output/evidence/kprove-claim-1.log` |
| even and at least 8 implies `true` | `/audit-output/evidence/kprove-claim-2.log` |
| below 8 implies `false` | `/audit-output/evidence/kprove-claim-3.log` |
| odd and at least 8 implies `false` | `/audit-output/evidence/kprove-claim-4.log` |

Build and aggregate logs:

- `/audit-output/evidence/clean_reconstruction.sh`
- `/audit-output/evidence/kompile-runtime.log`
- `/audit-output/evidence/krun-concrete.log`
- `/audit-output/evidence/kompile-verification.log`
- `/audit-output/evidence/kprove-original-spec.log`

Stage result: PASS.

## 4. Adequacy and real-program pinning

### Plain-language claims

1. For every K mathematical integer `N`, from the clean initial scope/heap/stack state, calling the entry wrapper returns exactly `N >= 8 and pyMod(N, 2) == 0`, restoring every other explicitly mentioned cell.
2. If `N >= 8` and `pyMod(N, 2) == 0`, the same call returns `true`.
3. If `N < 8`, it returns `false`.
4. If `N >= 8` and `pyMod(N, 2) != 0`, it returns `false`.

The universal claim has no precondition. The three corollaries partition the integers by threshold and parity.

Satisfying ground witnesses are `N=8` for the universal claim, `N=10` for claim 2, `N=7` for claim 3, and `N=9` for claim 4. Substitution gives respectively `true`, `true`, `false`, and `false` in the formal postconditions, trusted canonical, and candidate Python. `/audit-output/evidence/claim-witnesses.log` records these checks and constructive four-summand witnesses.

### Constructor-level program identity

The entry claim does not load the complete module. It expands the proof-only symbol to a call of a closure. That is acceptable only if the closure is the submitted function.

`/audit-output/evidence/pinning_check.py` parses both the submitted `.mpy` module and the exact `verification.k` rule with the fresh K definition, then compares their KAST constructors. It established:

- exactly one submitted `FuncDef`;
- binding name `"is_equal_to_sum_even"`;
- exactly one parameter `"n"`;
- constructor-identical parameter list;
- constructor-identical full statement/body tree;
- capture of initial scope 0;
- exactly one call argument, the same symbolic `N:Int`;
- preservation of an arbitrary continuation.

The submitted and proof body KAST hashes are both `7b21a850549b2821b6247ad31670eb213a19ab7ace72494e66440454bef9e1d8`. See `/audit-output/evidence/pinning-check.log`.

The wrapper skips only module-level creation of the function-name binding and instead constructs that exact closure directly. The body neither recurses nor reads the function's global name, so the skipped binding cannot affect its value, control, heap, exception state, or returned result. All property-bearing operations still execute under the supplied semantics.

### Control and state footprint

The wrapper itself only replaces a fresh proof entry symbol with `Call(exact-closure, N)` and retains the surrounding continuation. Fixed semantics then:

1. evaluates the callee and argument;
2. allocates a temporary function scope and pushes a frame;
3. binds `n` to `N`;
4. evaluates the exact `Return(BoolOp(...))` body;
5. performs lookup, ordered comparison, short-circuit control, modulo, and equality;
6. stores the return value, pops the frame, restores `env`, removes the temporary scope, and restores `scopeLoc`, stack, and `ret`.

No heap allocation, output, external state, or exception is possible on the `Int` domain. The claims pin the final environment, scopes, heap, heap location, stack, return state, exception state, and exit code, so the result is not free and state restoration is not omitted.

### Body sensitivity

I changed the threshold in the body actually executed by the claim from 8 to 10, rebuilt a separate proof definition successfully, and reran the original postcondition. `kprove` exited 1 with a stuck implication; `N=8` is the concrete counterexample. This changes the claim's executed constructor term, not merely external `solution.py`.

Evidence:

- `/audit-output/evidence/verification-body-mutated.k`
- `/audit-output/evidence/spec-body-sensitivity.k`
- `/audit-output/evidence/body-sensitivity.log`

Stage result: PASS. Manual duplication is a maintenance observation, not a substituted-program defect in the immutable artifact.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`/audit-output/evidence/rule-inventory.tsv` is the source-located exhaustive inventory generated by `/audit-output/evidence/inventory_rules.py`. It includes every declaration, rule, evaluation context, configuration, candidate claim, and proof-local rule in `semantics.k`, all 23 helper K files, `verification.k`, and `spec.k`.

Totals:

- 228 syntax declarations;
- 696 rules;
- 5 evaluation contexts;
- 1 configuration;
- 4 claims;
- 146 declarations marked `function`;
- 107 marked `total`;
- 45 priority rules;
- 26 `owise` rules;
- 35 `concrete` rules;
- 22 `no-evaluators` opaque declarations;
- 5 macro/macro-rec declarations;
- no local `functional` or `simplification` declaration/rule.

The per-file review is:

| File/module | Inventory summary | Disposition for this theorem |
|---|---:|---|
| `semantics.k` | assembly only | imports `MPY`; proof does not import `MPY-CONCRETE` |
| `syntax.k` | 16 syntax blocks | exact declarations for all submitted constructors and strictness/context generation |
| `core.k` | 37 syntax, 46 rules, 1 configuration | initial cells, sequencing, lookup, literals, argument evaluation, helpers reviewed; relevant rules are faithful |
| `int.k` | 1 syntax, 16 rules | `>=`, `%`, `==`, and `pyMod(_,2)` are exact for mathematical integers |
| `bool.k` | 13 rules, 1 context | correct value-returning left-to-right short-circuit `and`; ref-special cases are unreachable |
| `operators.k` | 10 rules, 2 contexts | correct operand order and dispatch; only Int cases can match |
| `call.k` | 3 syntax, 21 rules | generic call, argument evaluation, and exact closure call rule are relevant and state-faithful |
| `functions.k` | 4 syntax, 15 rules | ordinary parameter bind, `Return`, `#endcall`, and frame pop are relevant and faithful |
| `assert.k` | 3 rules | used only by independent concrete tests, not by the symbolic theorem |
| `builtins.k` | 38 syntax, 137 rules | no builtin is called by the submitted body; opaque `md5hexCodes` is unreachable |
| `comprehension.k` | 3 syntax, 7 rules | macros unused |
| `concrete.k` | 5 syntax, 16 rules | LLVM-only; mechanically absent from proof definition |
| `controls.k` | 3 syntax, 34 rules | assignments/branches/loops/imports unused by this body |
| `dict.k` | 12 syntax, 28 rules | unused and sort-disjoint |
| `float.k` | 34 syntax, 121 rules, 19 opaque declarations | no Float term can arise from an `Int` input in this body |
| `iter.k` | 1 syntax | iterator protocol unused |
| `list.k` | 5 syntax, 27 rules | unused; no list/ref value can arise |
| `methods.k` | 27 syntax, 75 rules | unused |
| `range.k` | 2 syntax, 6 rules | unused |
| `set.k` | 6 syntax, 12 rules | unused |
| `sort.k` | 6 syntax, 19 rules, 2 opaque declarations | `sortVS`/`sortKeyVS` never occur |
| `str.k` | 5 syntax, 28 rules | unused except inert imported declarations |
| `subscript.k` | 15 syntax, 40 rules | indexing and total OOB abstraction unused |
| `tuple.k` | 4 syntax, 21 rules | unused |
| `verification.k` | 1 syntax, 1 rule | definitional entry expansion to the exact submitted closure; no result summary or oracle |
| `spec.k` | 4 claims | all result-constraining and independently reconstructed |

### Used-construct map

| Submitted constructor | Declaration/evaluation |
|---|---|
| `Module`, `FuncDef`, `Params`, `Stmts` | `syntax.k`; module/statement sequencing in `core.k`; closure behavior in `functions.k` |
| `Call`, `closureVal`, parameter `"n"` | `call.k`, `core.k`, `functions.k` |
| `Return` | `[strict]` syntax plus `functions.k` return/pop rules |
| `BoolOp("and", ...)` | `bool.k` head-evaluation context and disjoint truthy/falsey rules |
| `Compare`, `CmpOp(">=")`, `CmpOp("==")` | `operators.k` contexts/dispatch and `int.k` cases |
| `BinOp("%", ...)` | `[seqstrict(2,3)]`, `operators.k`, `int.k`, fully defined `pyMod` equation |
| `Name("n")` | lexical lookup through the just-created callee scope in `core.k` |
| `Int(8)`, `Int(2)`, `Int(0)` | literal rules in `core.k` |

The applicable guards are disjoint or agree on overlaps. For this path:

- `BoolOp("and", ...)` truthy and falsey rules are complementary;
- integer comparison heads are operator-disjoint;
- closure and builtin/type/method call dispatch are constructor-disjoint;
- the proof's `pyMod` divisor is the nonzero positive constant 2;
- no priority rule preempts a material operation with a summary.

The proof-local rule introduces no fresh result-bearing symbol, no opaque value, no `total` assertion, no equation, no simplification, and no priority. It expands to fixed-semantics execution and preserves the continuation and all cells.

The supplied semantics intentionally contains limited or opaque behavior for other programs—for example symbolic float functions, sort, MD5, total out-of-bounds indexing, and simplified import/exception coverage. Those are recorded trust boundaries, not used premises. I do not label any of them a theorem-breaking unsound rule here because no intended integer input to this submitted program can produce their left-hand sides or let them affect a branch, result, state, or postcondition. Consequently there is no claimed material unsoundness requiring a false-conclusion witness.

Stage result: PASS for Gate A and for all semantics reachable by the real program.

## 6. Fresh non-vacuity test

The candidate supplied no vacuity artifact on which this review relies. I created `/audit-output/evidence/spec-vacuity.k` with the satisfiable precondition `N ==Int 8` and changed the required result to `false`. Python, the original K theorem, and elementary evaluation all give `true` at 8.

First:

```text
kprove spec-vacuity.k --definition verification-audit-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

exited 0, confirming that the mutation parsed and built.

Then the same command without `--dry-run` exited 1. It produced `WarnStuckClaimState`, with the residual `<k> true ~> .K </k>` unable to unify with the demanded `false`, followed by the expected prover error. This is an unmet reachable result obligation, not a parser error, timeout, missing import, or unrelated crash.

Evidence:

- `/audit-output/evidence/non_vacuity.sh`
- `/audit-output/evidence/non-vacuity.log`
- `/audit-output/evidence/spec-vacuity.k`

Stage result: PASS.

## 7. Proven versus assumed accounting

### What is formally proved

Under the supplied `MPY` semantics and K's builtin theories, for every K `Int N` in the clean entry configuration, executing the exact submitted function body through real call, binding, lookup, evaluation, return, and frame-pop rules reaches a Boolean equal to:

`N >=Int 8 andBool pyMod(N, 2) ==Int 0`.

The explicitly framed cells are restored to their stated final values. The three corollaries prove the threshold/parity cases separately. This is a reachability/partial-correctness result; it is not a claim about arbitrary Python objects or a complete CPython implementation.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K compiler, Haskell/LLVM backends, `kprove`, and K builtin Int/Bool/Map/List/String hooks | all formal execution | unavoidable low-level toolchain trust; fresh versioned reconstruction used K 7.1.293 |
| supplied reference semantics | operational meaning of `.mpy` | mandated fixed input; recursively integrity-checked and exhaustively statically reviewed |
| trusted `py2mpy.py` | source-to-`.mpy` bridge | acceptable; trusted mount and candidate copy match, and regeneration is byte-identical |
| manual proof entry constructor | program identity | acceptable for this immutable candidate after KAST equality of binding/parameters/body and successful body-sensitivity mutation; maintenance risk remains |
| `pyMod` equation and K integer arithmetic | modulo branch/postcondition | acceptable and fully defined on the used constant divisor 2 |
| natural-language characterization | equivalence between “four positive evens” and `n >= 8` plus evenness | mathematically correct but informal, with constructive witness `2+2+2+(n-6)`; this is the reason for `CONCERNS` |
| finite differential/concrete tests | empirical source/semantics support | supportive only; 25,022 Python cases and boundary K assertions do not replace the universal K proof |
| unused opaque functions (`sortVS`, float abstractions, MD5, etc.) | none | excluded from the dependency cone; no effect on this theorem |

### Gate summary

- Gate A, real-program soundness: PASS.
- Gate B, intent adequacy and full intended integer domain: PASS, with the documented informal arithmetic-to-English bridge.
- Gate C, evidence and trust auditability: PASS; all relied-on experiments are reproducible and finite evidence is not presented as universal proof.

The proof is not vacuous, does not narrow the unrestricted integer domain, does not use bounded unrolling or examples as the theorem, does not prove a substituted body, and does not depend on a result-bearing oracle. The remaining concern is non-fatal and does not permit a false conclusion.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
