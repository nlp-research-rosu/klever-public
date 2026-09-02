# Independent adversarial review: 138-is-equal-to-sum-even

## Decision

The candidate's positive claims reconstruct cleanly and its Python implementation is correct on the intended integer domain. Nevertheless, the proof is not legitimate as a proof of the real Python program because the generated semantics gives Python `%` the meaning of K's signed remainder. On the valid input `n = -3`, Python computes `-3 % 2` as `1`, while the candidate semantics computes `IntValue(-1)`. A fresh reachability claim asserting the Python-false result `-3 % 2 == -1` closes with `#Top` under the candidate theory.

This is not an infrastructure uncertainty, a timeout, or merely a testing gap. It is a concrete false-conclusion witness for `semantic.k` line 61 on the intended input domain. The later comparison with zero happens to erase the discrepancy for this particular return value, so ordinary result differential tests do not expose it. The required static soundness gate, however, does not permit a globally false operational rule merely because the submitted postcondition is insensitive to this instance of the wrong intermediate value.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount is consistent with that mode:

- `/reference/reference-semantics` does not exist.
- `/reference/prompt.py`, `/reference/canonical.py`, and `/reference/py2mpy.py` are regular files.
- No candidate path is a symlink.
- All required source/provenance artifacts are regular files: `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`.
- Candidate `prompt.py` is byte-identical to trusted `/reference/prompt.py`.
- Candidate `py2mpy.py` is byte-identical to trusted `/reference/py2mpy.py`.

The matching hashes are:

- prompt: `e49218abe89b2b138512731659d96115b045637b8cebe43d2407656209332e58`
- translator: `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

`run-input.json` identifies problem `138-is-equal-to-sum-even`, condition `bare`, and no supplied semantics. `metrics.json` claims generation exit 0 with no timeout. `codex-last.txt`, `codex-output.log`, and the single 138-line structured trace claim a successful `#Top`; those claims were not trusted. The trace also shows that the final proof-local arithmetic checker was introduced late in generation. The candidate contains extra generated/cache artifacts (`semantic-kompiled/`, `verification-kompiled/`, and `__pycache__/`); these are not source-integrity failures in generated-semantics mode, but they were ignored completely.

Evidence:

- `evidence/stage1_inventory.sh`
- `evidence/stage1_inventory.log`
- `evidence/summarize_generation_trace.py`
- `evidence/generation_trace_summary.log`

The live toolchain was independently identified as K `v7.1.293`. There is no trusted-mount contradiction, so this is a candidate audit rather than `AUDIT_ERROR`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

For integer `n`, the natural-language contract asks whether there exist exactly four positive even integers whose sum is `n`. Such a decomposition exists exactly when `n` is even and `n >= 8`:

- Necessity: each positive even summand is at least 2, so four sum to at least 8; a sum of evens is even.
- Sufficiency: for even `n >= 8`, the four values `n - 6, 2, 2, 2` are positive even integers and sum to `n`.

The trusted canonical entry point returns `n % 2 == 0 and n >= 8`. Candidate `solution.py` returns `n >= 8 and n % 2 == 0`. On integers these differ only in the order of two pure Boolean tests and are extensionally equivalent.

### Trusted regeneration

The trusted translator was run on the copied `solution.py`. The regenerated file and submitted `solution.mpy` are byte-identical, both with SHA-256:

`4be6b3778909ca1c91506046bb2f1925cb4f689dad0162b5f8faa007e84eee8d`

The translated term is exactly:

```text
Module(
  FuncDef("is_equal_to_sum_even", Params("n"),
    Return(
      BoolOp(
        "and",
        Compare(Name("n"), CmpOp(">=", Int(8))),
        Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(0)))))))
```

### Independent differential testing

`evidence/differential_test.py` independently imports the trusted canonical module and copied candidate module. It records all inputs and tests:

- documented examples `4, 6, 8`;
- no empty case, because the formal/intended input is a scalar integer;
- threshold, sign, and parity boundaries;
- every integer from `-256` through `256`;
- 200 deterministic generated integers with seed 138;
- very large positive and negative Python integers.

There were 718 distinct inputs, zero result mismatches, and no non-Boolean returns. A separate brute-force four-positive-even oracle checked every integer from `-20` through `100` and found zero contract mismatches.

Evidence:

- `evidence/stage2_fidelity.sh`
- `evidence/stage2_fidelity.log`
- `evidence/differential_test.py`

These tests establish finite implementation/canonical agreement. They do not prove the K semantics sound.

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/review-138/candidate-src`; no candidate definition, cache, or binary was copied. Before compilation, checks confirmed that the fresh output directories did not exist.

Fresh builds:

```text
kompile .../semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition .../build/semantic-kompiled
[exit 0]

kompile .../verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition .../build/verification-kompiled
[exit 0]
```

The build commands and their zero statuses are in `evidence/stage3_rebuild_attempt1_parser_error.log`. The suffix records a reviewer-authored output parser error after both builds had already succeeded; it is not a candidate or K failure. The corrected comparison was then run against those freshly built definitions.

Fresh LLVM execution was compared with both Python implementations for:

`[-11, -10, -3, -2, 0, 4, 6, 7, 8, 9, 10, 12, 10**18]`

All 13 K final Booleans matched both Python implementations.

The submitted all-claims command independently produced:

```text
kprove .../spec.k --definition .../verification-kompiled --spec-module SPEC
#Top
[exit 0]
```

For claim-by-claim accountability, an audit copy added labels without changing any claim body. Each of the six claims was selected separately and each printed `#Top` with exit 0:

- `entry-general`
- `necessity-four-summands`
- `sufficiency-witnesses`
- `example-4`
- `example-6`
- `example-8`

Evidence:

- `evidence/stage3_rebuild.sh`
- `evidence/stage3_rebuild_attempt1_parser_error.log`
- `evidence/compare_krun.py`
- `evidence/stage3_prove_after_build.sh`
- `evidence/stage3_prove_after_build.log`

Thus reconstruction succeeds under the candidate theory. This does not discharge the independent soundness obligation for that theory.

## 4. Adequacy and real-program pinning

### Plain-language claim inventory

1. **Universal entry claim (`spec.k` lines 7–17).** With no additional precondition, for every K integer `N`, execute the submitted translated function on input `N`, terminate, and return `sumFourPositiveEvens(N)`.
2. **Necessity claim (lines 20–34).** If `A`, `B`, `C`, and `D` are positive even K integers, execute the submitted function on their sum and return true.
3. **Constructive sufficiency claim (lines 37–41).** If `N` satisfies `sumFourPositiveEvens(N)`, execute the proof-local checker and return true, meaning that `N - 6, 2, 2, 2` pass the explicitly defined positivity, parity, and sum checks.
4. **Example 4 (lines 44–54).** Execute the submitted function at 4 and return false.
5. **Example 6 (lines 56–66).** Execute it at 6 and return false.
6. **Example 8 (lines 68–78).** Execute it at 8 and return true.

The third claim is an auxiliary arithmetic claim, not a claim that executes the Python program. The universal, necessity, and example claims do execute the program term.

### Satisfiability and concrete substitution

Every precondition has a concrete witness:

- universal entry: `N = 8`;
- necessity: `A = B = C = D = 2`, giving input 8;
- sufficiency: `N = 8`, giving witnesses `2, 2, 2, 2`;
- examples: their fixed inputs.

Both Python implementations return false, false, and true at 4, 6, and 8. At the shared satisfying input 8, both return true.

### Real-program pinning

`evidence/check_program_pinning.py` balanced and normalized every `Module(...)` term in submitted `spec.k`. There are exactly five program-bearing claims, and each embedded term is structurally identical to submitted `solution.mpy`. Trusted regeneration already established that this `.mpy` is the exact translation of `solution.py`.

The result cell is constrained in every claim; there is no right-hand-side-only free result variable, unconstrained oracle, tautological implication, or omitted result. A body-sensitivity probe changed the threshold literal from 8 to 9. At input 8 the fresh semantics changed from `BoolValue(true)` to `BoolValue(false)`, showing that execution depends on the embedded body rather than a hard-coded final answer.

Evidence:

- `evidence/check_program_pinning.py`
- `evidence/stage4_5_static_checks.sh`
- `evidence/stage4_5_static_checks.log`

## 5. Rule-by-rule static soundness review

### Exhaustive local declaration inventory

`semantic.k` declares:

- `Program`: `Module(Stmt)`.
- `Stmt`: `FuncDef(String, Params, Stmt)` and `Return(Expr)`.
- `Params`: exactly one `String`.
- `Expr`: `Name(String)`, `Int(Int)`, `BinOp(String, Expr, Expr)`, `BoolOp(String, Expr, Expr)`, and `Compare(Expr, CmpOp)`.
- `CmpOp`: `CmpOp(String, Expr)`.
- `Value`: `IntValue(Int)` and `BoolValue(Bool)`.
- `Result`: `noResult` or a `Value`.
- A configuration with exactly `<k>`, `<input>`, and `<result>` cells.
- Four partial `[function]` symbols: `eval`, `evalBin`, `evalCompare`, and `evalBool`.

`verification.k` declares:

- `sumFourPositiveEvens(Int)` as `[function, total]`.
- `canonicalWitnessesAreValid(Int)` as `[function, total]`.
- the fresh `KItem` `checkCanonicalWitnesses(Int)`.

There are no local `[functional]` declarations distinct from `[function]`, no opaque symbols, no priority rules or attributes, and no simplification, concrete, anywhere, macro, alias, associative, commutative, or idempotent rules. There are no generated helper K files beyond `semantic.k` and `verification.k`.

### Construct-to-rule map for the submitted term

| Used construct | Declaration and behavior |
|---|---|
| `Module` | `Program` production; entry rule at `semantic.k` lines 45–49 |
| `FuncDef`, `Params`, `Return` | `Stmt`/`Params` productions; matched by the same entry rule |
| `Name("n")` | `Expr` production; `eval(Name(X), X, N) => IntValue(N)` |
| `Int(8)`, `Int(2)`, `Int(0)` | `Expr` production; literal evaluation rule |
| `BinOp("%", ...)` | `Expr` production; binop dispatch plus `%` rule |
| `Compare(..., ">=")` | `Expr`/`CmpOp`; compare dispatch plus integer `>=` rule |
| `Compare(..., "==")` | `Expr`/`CmpOp`; compare dispatch plus integer equality rule |
| `BoolOp("and", ...)` | `Expr` production; Boolean dispatch plus `andBool` rule |

All constructs in `solution.mpy` parse and have an applicable rule. Missing semantics for translator constructs not present in this program is acceptable in generated-semantics mode.

### Operational and function rules

1. **Module/entry rule (`semantic.k` 45–49).** It recognizes the requested entry-point name, binds the sole parameter string, consumes the module term, preserves input, and places evaluation of the actual body into result. For the one-function/one-return submitted module this is a recognizable entry harness. It does not fabricate a value; the body remains structurally present and body sensitivity was demonstrated.
2. **Name lookup (56).** The repeated `X` requires the name to equal the bound parameter. This is correct for the only name in the body.
3. **Integer literal (57).** Truthfully wraps the K integer.
4. **Binary dispatch (59–60).** Recursively evaluates both operands under the same binding and input. For the pure submitted operands this preserves all modeled cells.
5. **Modulo (61–62).** **Unsound as a Python `%` rule.** It uses K `%Int`, whose signed remainder follows truncating division, not Python's divisor-signed modulo.
6. **Comparison dispatch (64–65).** Correctly evaluates the two actual integer operands.
7. **Integer `>=` (66–67).** Correct.
8. **Integer `==` (68–69).** Correct.
9. **Boolean dispatch (71–72).** It eagerly evaluates both operands, unlike Python's short-circuit `and`. In the submitted body both operands are pure comparisons and the right operand has a fixed nonzero divisor, so no result, state, exception, or control difference occurs for this program. The rule would be incomplete for other expressions, but no concrete false observable conclusion for the submitted term follows from eagerness.
10. **Boolean `and` (73–74).** Correct for two `BoolValue` operands.
11. **`sumFourPositiveEvens` equation (`verification.k` 10–11).** One unguarded nonrecursive equation covers all K integers, so the `[total]` declaration has complete, non-overlapping coverage. The equation is the correct arithmetic characterization at the Boolean level; equality to zero is unaffected by the signed representative of a nonzero remainder.
12. **`canonicalWitnessesAreValid` equation (14–18).** One unguarded nonrecursive equation covers all K integers. It explicitly checks positivity/evenness of `N - 6`, the positive-even literal 2, and the four-term sum equation. There is no overlap or descent issue.
13. **`checkCanonicalWitnesses` rule (21–22).** This fresh proof-local checker consumes only its own fresh K item, preserves the omitted input cell, changes `noResult` to the fully defined witness-validity Boolean, and is used only by the auxiliary sufficiency claim. It does not preempt fixed execution of any program term and is not an opaque result oracle. Its task-specific role is acceptable as an executable definitional checker, but it cannot repair an unsound language rule.

The six reachability claims listed in Stage 4 are the only local claims. There are no loop or helper-control claims because the program has no loop or call stack in this representation.

### Required false-conclusion witness

Take the valid intended input `n = -3`. The submitted program actually evaluates the used subexpression `n % 2`.

Python:

```text
python3 -c 'print(-3 % 2)'
1
[exit 0]
```

Candidate semantics:

```text
krun probe-modulo.mpy --definition fresh-semantic-kompiled -cN=-3
...
<result> IntValue ( -1 ) </result>
[exit 0]
```

More strongly, `evidence/spec-modulo-false.k` states that the translated Python fragment `return n % 2` returns `IntValue(-1)` at `n = -3`. The fresh candidate proof definition proves this Python-false conclusion:

```text
kprove .../spec-modulo-false.k \
  --definition .../verification-kompiled \
  --spec-module SPEC-MODULO-FALSE
#Top
[exit 0]
```

The corresponding negative-divisor probe also disagrees (`3 % -2` is `-1` in Python and `1` in the candidate semantics), although the positive-divisor `-3` witness alone is sufficient and occurs in the real submitted expression's domain.

For the submitted final expression, both `1 == 0` and `-1 == 0` are false, so the final Boolean happens to agree. That observational coincidence explains why Stages 2 and 3 pass; it does not make the rule a true semantics of the used Python construct. A later claim about the intermediate value is already demonstrably false and provable. Under the required soundness boundary, this is a material generated-semantics failure.

Evidence:

- `evidence/modulo_semantics_probe.sh`
- `evidence/modulo_semantics_probe.log`
- `evidence/spec-modulo-false.k`
- `evidence/modulo_false_claim.sh`
- `evidence/modulo_false_claim.log`

## 6. Fresh non-vacuity test

No candidate vacuity artifact was relied upon. A fresh mutation in `evidence/spec-vacuity.k` changes the fixed example at `n = 8` from the correct result `true` to the deliberately false result `false`.

The mutation's K frontend/dry run succeeded:

```text
kprove .../spec-vacuity.k --definition .../verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
[exit 0]
```

The actual proof then reached the expected concrete unmet obligation:

```text
WarnStuckClaimState
<input> 8 </input>
<result> BoolValue ( true ) </result>
[exit 1; expected nonzero]
```

This is a meaningful result mutation with the realizable input 8. It was reached, parsed, and rejected because the result was wrong—not because of an import, parser, timeout, or unrelated backend error.

Evidence:

- `evidence/spec-vacuity.k`
- `evidence/stage6_nonvacuity.sh`
- `evidence/stage6_nonvacuity.log`

## 7. Proven versus assumed accounting

### What `#Top` establishes under the candidate theory

Conditional on the supplied generated semantics and proof-local equations:

- the exact embedded translated term returns `N >= 8 and K-remainder(N, 2) == 0` for every K integer `N`;
- any sum of four positive even K integers is accepted;
- when the arithmetic characterization holds, `N - 6, 2, 2, 2` satisfy the encoded positivity, parity, and sum checks;
- the examples at 4, 6, and 8 have the claimed results.

The false-postcondition test shows these result obligations are discriminating rather than vacuous.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K parser, compiler, LLVM/Haskell backends, reachability engine, and SMT integration | Parsing, execution, and all proof closure | Normal low-level trust boundary; rebuilt live with K v7.1.293 |
| Built-in K `Int` and `Bool` operations | All arithmetic and Boolean conclusions | Acceptable as K primitives, but `%Int` is not interchangeable with Python `%` |
| Trusted `/reference/py2mpy.py` | Python AST-to-constructor identity | Acceptable trusted input; byte identity and regenerated term recorded |
| Candidate entry harness | Connects a one-function module plus `<input>` to body evaluation | Narrow and body-sensitive for this submitted program |
| Candidate expression rules | Connect translated constructs to Python behavior | Mostly faithful on the actual pure term; modulo rule is concretely false |
| `sumFourPositiveEvens` | Final postcondition and necessity/sufficiency accounting | Fully defined, total, and mathematically appropriate at parity/threshold level |
| `canonicalWitnessesAreValid` and checker | Auxiliary constructive sufficiency claim | Fully defined and result-constraining; not opaque and not a replacement for program execution |
| Natural-language interpretation of four explicit witnesses | Intent bridge | Straightforward ordinary mathematics and partly represented by the explicit checks |
| Python/canonical differential testing | Finite real-program bridge | 718 zero-mismatch inputs; empirical only |
| K/Python concrete comparison | Finite generated-semantics bridge | 13 final-result cases; empirical and too coarse to validate intermediate remainder values |

There are no opaque symbols, fresh unconstrained values, empirical oracles inside the proof, or unproved loop summaries. Candidate prose, the old `#Top`, old definitions, and generation traces contributed no trusted theorem.

### Why the successful final-result tests do not rescue the proof

The theorem's final parity test observes only whether the remainder is zero. Python modulo and K signed remainder agree on divisibility by 2 even when they disagree on the nonzero representative. Therefore the candidate implementation is correct and the submitted final-output claim is extensionally true, but the generated operational theory used to prove it contains a reachable false step and proves a concrete Python-false reachability claim. The required audit asks for a sound proof of the real generated program, not merely a true answer obtained through a theory whose wrong intermediate value is masked by the postcondition.

The soundness gate therefore fails. Clean `#Top`, program pinning, and non-vacuity are necessary but cannot substitute for a sound generated semantics.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
