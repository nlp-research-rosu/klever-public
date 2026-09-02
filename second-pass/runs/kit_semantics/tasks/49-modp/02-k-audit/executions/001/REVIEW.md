# Independent adversarial audit: HumanEval 49-modp

## Outcome

The candidate contains a legitimate, freshly reconstructible partial-correctness proof of the submitted program. The proof executes the exact translated function body under the supplied semantics and constrains its result to `pyMod(2 ^Int N, P)` for all symbolic integers satisfying `N >= 0` and `P != 0`. It uses no candidate-authored semantic rule, lemma, simplification, oracle, summary, or operational bridge.

The non-fatal concern is a trusted-input specification discrepancy. The natural-language contract says to return `2^n modulo p`, and the generated implementation agrees with Python's modular-power primitive throughout the formal domain. The trusted canonical loop, however, returns the unnormalized initializer `1` when `n = 0`; it therefore disagrees with the generated implementation at `(n, p) = (0, 1)` and at zero exponent with negative moduli. The canonical also returns `1` for negative `n`, while the generated implementation uses Python negative-exponent behavior. Negative exponents and zero modulus are outside the ordinary defined modular-exponent domain, but the zero-exponent/modulus-one conflict is real and is why this audit does not issue an unqualified `PASS`.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `49-modp`;
- condition `kit-semantics`;
- record layout `pipeline-v3`;
- semantics mode `SUPPLIED_SEMANTICS`;
- mounted candidate `/candidate`;
- trusted prompt, canonical, translator, and supplied semantics below `/reference`.

The mounted mode is internally consistent: `/reference/reference-semantics` exists, as required for `SUPPLIED_SEMANTICS`. No infrastructure stop condition was found.

The audit campaign object embedded in `/audit-input.json` is JSON-equal to `/audit-campaign-lock.json`, and the lock's direct SHA-256 is the recorded `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`. See `evidence/stage1-campaign-match.log` and `evidence/stage1-file-hashes.log`.

All required `pipeline-v3` records were present, readable, and of the correct regular-file or directory type:

- `/run.json`
- `/task.json`
- `/generation-result.json`
- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/runtime-metrics.json`
- `/generation-evidence/usage.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`
- `/generation-evidence/codex-trace/`

The type and symlink audit found no symlink anywhere in the required provenance inputs, trusted reference tree, or candidate tree. Evidence: `evidence/stage1-required-types.log`.

Direct hashes of all individually declared records match their launcher and generation manifests. In particular, the trace file hashes to `c85b008d6ff4bf20c537c70aabf6d340b3e50ff60f34b15b0a44ee13eb445167`, parses as all 236 JSONL records, and contains the expected complete task lifecycle. The generation log and trace were inspected only as untrusted historical claims. Evidence: `evidence/stage1-file-hashes.log`, `evidence/stage1-trace-inspection.log`, `evidence/stage1-generation-output-inspection.log`, and reviewer script `evidence/inspect_generation_trace.py`.

The candidate prompt and translator are byte-identical to `/reference/prompt.py` and `/reference/py2mpy.py`. Recursive `diff -r --no-dereference` between the candidate and trusted `reference-semantics/` trees exits 0. Per-file manifests confirm the same paths and hashes, with no additional, missing, mistyped, or symlinked entry. Evidence:

- `evidence/stage1-input-cmp.log`
- `evidence/stage1-semantics-diff.log`
- `evidence/stage1-semantics-types.log`
- `evidence/stage1-reference-semantics-manifest.log`
- `evidence/stage1-candidate-semantics-manifest.log`

The candidate-provided compiled definitions and caches were not trusted or reused.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The prompt's contract is: `modp(n, p)` returns `2^n` modulo `p`. The examples include `n = 0` and otherwise use nonnegative exponents and positive nonzero moduli. Modular exponentiation ordinarily requires `n >= 0` and a nonzero (usually positive) modulus.

The trusted canonical initializes `ret = 1`, repeats `ret = (2 * ret) % p` over `range(n)`, then returns `ret`. The generated implementation is:

```python
def modp(n: int, p: int):
    return 2 ** n % p
```

The trusted translator regenerates:

```text
Module(
  FuncDef("modp", Params("n", "p"),
    Return(BinOp("%", BinOp("**", Int(2), Name("n")), Name("p")))))
```

The regenerated file is byte-identical to the submitted `/candidate/solution.mpy`; both hash to `e815171fcb4b817936481b4efe76524d0eef3d17aab8a5e08c74690a34adba7a`. Evidence: `evidence/stage2-regeneration.log`.

### Independent differential testing

`evidence/stage2_differential.py` imports the scratch copy of the trusted canonical and the generated entry point independently. It covers all prompt examples, the canonical loop boundaries `n = -3, -1, 0, 1, 2, 3`, positive/negative/zero modulus boundaries, systematic ranges, a fixed-seed random sample, and large exponents. The exact 4,832-case input set is recorded by hash in `evidence/stage2-differential.log`.

Results:

- all five documented examples: 0 mismatches;
- all sampled `n >= 0, p != 0` cases: 21 canonical/generated mismatches;
- all sampled nonnegative positive-modulus cases: one mismatch, `(0, 1)`;
- negative exponents: many expected divergences because the canonical's `range(n)` is empty while Python exponentiation returns a float or raises;
- zero modulus with `n = 0`: canonical returns `1` without taking a remainder, while the generated implementation raises.

The 21 formal-domain mismatches all arise from the canonical's unnormalized zero-iteration initializer: for `n = 0`, generated `1 % p` differs from canonical `1` when `p = 1` or `p < 0`.

A second independent oracle uses CPython's three-argument `pow(2, n, p)`, rather than the candidate expression or K equations. Across 36,761 distinct cases with `n >= 0` and `p != 0`, it reports zero generated/oracle mismatches. Evidence: `evidence/stage2_contract_oracle.py` and `evidence/stage2-contract-oracle.log`.

Judgment: the submitted program implements the natural-language modular-arithmetic result throughout the proof domain. The canonical conflict is a trusted-input adequacy ambiguity, not evidence that the K theorem proves a substituted program. It remains a material review concern and is carried into the final verdict.

All executable sources used later were copied explicitly to `/tmp/audit-work/49-modp`; candidate kompiled directories and caches were excluded. Evidence: `evidence/stage2-scratch-copy.log`.

## 3. Clean proof reconstruction

The installed tools are K v7.1.293. Fresh build and proof commands were run under `/tmp/audit-work/49-modp`.

Fresh proof definition:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

Result: exit 0. Evidence: `evidence/stage3-kompile-verification.log`.

The spec contains one positive claim, `SPEC.modp`. It was independently run both as the whole spec and by exact claim selection:

```text
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.modp
```

Both commands print `#Top` and exit 0. The Haskell backend emits numerous `DecidePredicateUnknown` warnings while attempting optional symbolic-integer decisions; those warnings do not become a stuck state, and the required success signal is present. Evidence:

- `evidence/stage3-kprove-spec.log`
- `evidence/stage3-kprove-modp-claim.log`

A separate LLVM definition was also rebuilt from the trusted supplied semantics:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

Reviewer-authored concrete assertions cover prompt examples plus `(0, 1)`, zero exponent with a negative modulus, and a negative modulus after one multiplication. Translation and execution finish at `.K`, with `NoExc` and exit code 0. Evidence:

- `evidence/stage3_concrete.py`
- `evidence/stage3-concrete-translate.log`
- `evidence/stage3-kompile-runtime.log`
- `evidence/stage3-krun-concrete.log`

Thus the clean dynamic reconstruction gate passes.

## 4. Adequacy and real-program pinning

### Plain-language claim

Precondition:

- `N` and `P` are K mathematical integers;
- `N >= 0`;
- `P != 0`;
- the module scope at location 0 binds `"modp"` to the closure shown in the translated submission;
- heap and call stack are empty, there is no return or exception in flight, and exit code is 0.

Postcondition:

- executing `Call(Name("modp"), Int(N), Int(P))` produces exactly `pyMod(2 ^Int N, P)` in `<k>`;
- the other displayed state cells are restored to their initial values.

This is result-constraining. The RHS is neither a fresh variable nor an existential nor an implication; it is the exact modular-power expression.

### Mechanical pinning

`evidence/stage4_pinning.py` removes only whitespace, extracts the function body from the trusted regenerated `.mpy`, and requires the exact same constructor term, parameter order, closure binding, function name, symbolic call, result expression, and complete state cells in `spec.k`. Every check is true. Evidence: `evidence/stage4-pinning.log`.

The claim starts after module installation rather than at `#loadAll(Module(...))`. This normalization is justified mechanically and dynamically:

- the translated module contains exactly one `FuncDef("modp", Params("n", "p"), BODY)`;
- the fixed module-load and `FuncDef` rules install `closureVal(("n", "p"), BODY, 0)` in scope 0;
- fresh `krun solution.mpy` reaches the exact closure body, parent scope, locations, empty heap/stack, `noRet`, `NoExc`, and exit code 0 used by the claim.

Evidence: `evidence/stage4-krun-module-binding.log` and the pinning log above. No external source-to-proof regeneration assumption is needed for this immutable artifact.

Satisfiable ground substitutions are recorded in `evidence/stage4-witnesses.log`. For `(3,5)`, `(1101,101)`, `(0,101)`, `(0,1)`, `(1,-5)`, and `(0,-5)`, the precondition holds and the claimed value equals the generated Python result. The same artifact makes the canonical zero-iteration discrepancies explicit.

There is no helper claim or loop claim to pin; the program has no loop.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer read all 2,211 lines of `reference-semantics/semantics.k` and its helper files, plus `verification.k` and `spec.k`. `evidence/stage5_inventory.py` records every declaration with source line and normalized full text. The resulting inventory contains:

- 695 explicit rules;
- 227 syntax declarations;
- 5 contexts;
- 1 configuration;
- 1 claim;
- 146 records carrying `[function]`;
- 107 carrying `[total]`;
- 25 carrying `[symbol]`;
- 22 carrying `[no-evaluators]`;
- 45 carrying a priority;
- 26 carrying `[owise]`;
- 35 carrying `[concrete]`;
- no `[functional]` declaration;
- no simplification rule.

Evidence: `evidence/stage5-rule-inventory.log`.

`evidence/stage5_assess_inventory.py` assigns a disposition to every one of the 929 inventory records. The assessment log records 20 target-used operational/equational rules, four pinning-only module rules, 25 target structure declarations, one target claim, 22 fixed opaque but unreachable declarations, 21 LLVM-only records absent from the proof import graph, and 836 other fixed but target-unreachable records. Evidence: `evidence/stage5-rule-assessment.log`.

### Candidate proof extensions

`verification.k` only requires the supplied `semantics.k` and imports `MPY`. It declares no syntax, function, totality assertion, opaque value, rule, priority, simplification, or lemma. It imports `MPY`, not `MPY-CONCRETE`.

Therefore the proof-extension inventory is empty:

- no definitional summary;
- no derived lemma;
- no operational bridge;
- no candidate-added trusted primitive.

No rule encodes the task answer, bypasses the submitted function, or introduces an oracle shared circularly with the postcondition.

### Actual target rule path

The target path is:

1. `Call` evaluates the callee, then both arguments left-to-right.
2. `Name("modp")` resolves in scope 0 to the exact closure.
3. `Int(N)` and `Int(P)` cool to K integers and are appended in parameter order.
4. Closure dispatch allocates scope 1, pushes the caller continuation/environment, and starts exact parameter binding.
5. `n` and `p` bind in that new frame.
6. `[seqstrict(2,3)]` on nested `BinOp` evaluates base, exponent, then modulus in Python order.
7. `applyBin("**", 2, N)` rewrites to `2 ^Int N` only under `N >= 0`.
8. `applyBin("%", ..., P)` rewrites to `pyMod(..., P)`.
9. strict `Return` records the exact value and initiates frame pop.
10. pop deletes the temporary frame, restores environment and allocation location, clears return state, and places the value in the caller continuation.

The exact source excerpts are in `evidence/stage5-target-rule-excerpts.log`.

State footprint:

| Phase | Cells read/written | Review |
|---|---|---|
| Lookup/argument evaluation | `<k>`, `<env>`, `<scopes>` | Exact binding; left-to-right; no heap access |
| Call entry | `<k>`, `<env>`, `<scopes>`, `<scopeLoc>`, `<stack>` | Fresh frame 1 and saved empty continuation |
| Parameter binding | `<scopes>` | Exact two parameters and arguments |
| Arithmetic | `<k>` only | Fixed integer exponent and remainder operations |
| Return/pop | `<k>`, `<ret>`, `<stack>`, `<env>`, `<scopes>`, `<scopeLoc>` | Return value preserved; caller state restored |
| Unchanged | `<heap>`, `<heapLoc>`, `<exc>`, `<exit-code>` | No matching target operation mutates them |

The higher-priority cell-lookup and cell-binding rules are pruned because the ordinary closure frame has no `"$cells"` key. No special `Call(Attribute(...))`, builtin, collection, float, sort, md5, assertion, loop, or exception rule can match the target. The generic `Call` rule's `[owise]` status therefore does not hide a competing bridge.

The used equations have disjoint operator/sort cases. `appendVal` covers both list constructors and descends structurally. The exponent rule is guarded exactly by the claim's `N >= 0`. `pyMod(a,p) = ((a %Int p) + p) %Int p` implements Python/floored remainder for nonzero positive and negative divisors; `P != 0` excludes its undefined divisor. Concrete negative-modulus execution and the independent Python oracle support this bridge.

The supplied semantics contains deliberately opaque or totalized facilities elsewhere, including float primitives, sorting, md5, and total out-of-bounds list access. Some have intentionally narrow concrete equations. They are part of the fixed trusted language boundary, not candidate proof extensions, and no target term reaches them. The static audit found no false conclusion witness that any such rule can enable on this claim's intended input domain; accordingly they are recorded as an unrelated language-scope evidence limitation, not labeled unsound.

## 6. Fresh non-vacuity test

The candidate's `spec-vacuity.k` was not trusted. Two reviewer-authored mutations were created:

- `evidence/audit-spec-vacuity.k`: exact original body, concrete satisfying input `(3,5)`, false demanded result `4`;
- `evidence/audit-spec-body-sensitivity.k`: executed closure body changes base `2` to `3`, concrete input `(1,5)`, but the demanded original result remains `2`.

Both mutations first pass `kprove --dry-run` with exit 0, showing that they parse and build against the fresh definition:

- `evidence/stage6-vacuity-dry-run.log`
- `evidence/stage6-body-dry-run.log`

The actual proofs then fail as intended:

- false-result mutation: exit 1, `WarnStuckClaimState`, residual `<k> 3 ~> .K </k>` rather than `4`;
- body mutation: exit 1, `WarnStuckClaimState`, residual `<k> 3 ~> .K </k>` rather than `2`, with the residual state displaying the executed base-3 closure.

Evidence: `evidence/stage6-vacuity-kprove.log` and `evidence/stage6-body-kprove.log`.

These are expected unmet result obligations, not parser errors, timeouts, or unrelated failures. Gate A5 and body sensitivity pass.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied `MPY` semantics and K v7.1.293 proof engine, for every mathematical integer pair `N, P` with `N >= 0` and `P != 0`, the exact submitted closure, started in the exhibited module state, returns:

```text
pyMod(2 ^Int N, P)
```

with the displayed non-result cells restored. This is a partial-correctness statement under the Kit contract.

### Trust ledger

| Boundary | Dependents | Status |
|---|---|---|
| K parser/compiler/Haskell prover and built-in logic | `#Top`, all symbolic rewriting | Necessary trusted proof engine; positive and negative runs discriminate |
| Supplied `MPY` call/frame semantics | Binding, evaluation order, return control, state restoration | Acceptable fixed semantics; exact tree integrity and static rule review completed |
| K mathematical integers, `^Int`, `%Int`, maps/lists | Arithmetic result and configuration operations | Acceptable low-level primitive boundary |
| `pyMod` equation for nonzero divisors | Human-facing Python modulo interpretation | Ordinary mathematical bridge, supported on positive and negative divisors by concrete and differential evidence |
| Trusted `py2mpy.py` | Python-source to constructor identity | Direct byte-identical regeneration; exact body mechanically pinned |
| Omitted Python type annotations in `.mpy` | Function constructor identity | Typing-only normalization; no runtime operation omitted |
| Interpretation `n >= 0`, `p != 0` as material modular-exponent domain | Gate B | Reasonable from the operation, examples, canonical loop, and undefined zero modulus; prompt does not state it explicitly |
| Trusted canonical implementation | Differential oracle | Conflicts with the natural-language result at zero exponent for modulus 1/negative moduli; documented concern |
| CPython `pow` differential | Empirical source-contract support | 36,761 finite cases, zero mismatches; not a universal proof |
| Supplied opaque float/sort/md5/other symbols | None | Unreachable and non-contributing |

The proof does not establish behavior for negative exponents or modulus zero, resource bounds, finite-memory termination for enormous exponents, or the correctness of unrelated supplied-semantics constructs.

Candidate `PROOF.md`, generation traces, prior compiled definitions, and earlier `#Top` reports were not used as substitutes for the reconstructed proof.

### Gate and decision summary

- Gate A, real-program soundness: PASS.
- Gate B, intent adequacy: PASS for the material modular-exponent domain, with the explicit canonical conflict above.
- Gate C, trust/evidence auditability: PASS.
- Benchmark decision: legitimate proof with a non-fatal trusted-input/intent ambiguity.

An index of reviewer artifacts and their SHA-256 hashes is in `evidence/evidence-index.log`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
