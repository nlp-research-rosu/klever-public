# Independent adversarial review: 71-triangle-area

The candidate's seven claims do close from a clean build, and the claims execute a constructor term mechanically identical to the trusted translation of `solution.py`. That is not a legitimate proof of the real generated Python program. The generated numeric semantics replaces Python binary floating-point execution with exact rational arithmetic and exact decimal square-root rounding. This produces a false result on a valid, terminating integer input. The formal claims also cover only `VInt` arguments although the source contract does not restrict side lengths to integers and both Python implementations accept finite float side lengths.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout = legacy-selected-stage1` and `semantics_mode = GENERATED_SEMANTICS`. The mounted inputs are consistent with that boundary: `/reference/reference-semantics` is absent. I did not infer or use any hidden semantics.

All records required for this layout are readable real files, not symlinks: `/run.json`, `/task.json`, `/generation-result.json`, `invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the JSONL trace. Optional `usage.json` is present and was inspected. Historical `runtime-metrics.json` is absent, which is permitted for this legacy layout. The candidate, generation-evidence, trace, and reference roots are real directories without linked entries.

The campaign object in `/audit-campaign-lock.json` is byte-hashed to the recorded `ad5dfc...d745` value and is structurally identical to the campaign block in `/audit-input.json`. Every launcher-recorded file hash checked independently matches. The pipeline tree digest of the mounted candidate is `7cfdec...c88f`, equal to both the selected result and invocation workspace digests; the trace digest is `29d9c7...a9cf`, equal to `usage.json`'s source-trace digest. The single trace file has the per-file hash recorded in the selected result. The 268 JSONL records all parse; the trace and 23,038-line rendered log were treated only as untrusted construction history.

`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their trusted mounted versions. All required proof artifacts are regular files. Full evidence is in [stage1_provenance.log](evidence/stage1_provenance.log), [stage1_trace_summary.log](evidence/stage1_trace_summary.log), and [stage1_generation_log_markers.log](evidence/stage1_generation_log_markers.log). No infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

The contract says: given three side lengths, return `-1` when any pair sum is at most the remaining side; otherwise compute Heron's area and return it rounded to two decimal places. The trusted canonical implementation uses Python's ordinary `/`, `** 0.5`, and `round(..., 2)` operations.

`solution.py` implements the same three guards in the same order, then the same semiperimeter, Heron product, square root, and rounding calculation. Regeneration with the trusted translator is byte-identical to submitted `solution.mpy`; see [translation_regeneration.log](evidence/translation_regeneration.log).

The independent differential test covers the two documented examples, zero and negative lengths, equality and just-valid cases at all three guard boundaries, all 13,824 triples in `[-3,20]^3`, a 1,728-case finite-float grid, and 2,000 seeded generated float triples. The API has three required scalars, so there is no empty collection input; `(0,0,0)` is the scalar boundary analogue. All 17,568 comparisons have zero mismatches. This finite evidence establishes source-rewrite fidelity over the tested inputs, not a theorem. See [differential_test.py](evidence/differential_test.py) and [python_differential.log](evidence/python_differential.log).

## 3. Clean proof reconstruction

I copied source artifacts to `/tmp/audit-work/candidate-fresh` and used no candidate-built definitions or caches. K 7.1.293 was available independently; versions and paths are in [tool_versions.log](evidence/tool_versions.log).

Fresh results:

- LLVM concrete compilation of `semantic.k`: exit 0 ([kompile_concrete.log](evidence/kompile_concrete.log)). Invalid paths execute, but valid paths fail at runtime with exit 113 because `sqrtHundredths(...)` remains unsupported on this backend ([concrete_semantics_cases.log](evidence/concrete_semantics_cases.log)).
- Haskell concrete compilation of `semantic.k`: exit 0 ([kompile_concrete_haskell.log](evidence/kompile_concrete_haskell.log)). Normal, guard-boundary, zero, negative, and small irrational-area integer cases terminate and match Python after interpreting `VRounded(N)` as `N/100`. A valid float case stops at `BinOp("+", VFloat(3.0), VFloat(4.0))` with `NoResult` ([concrete_semantics_haskell_cases.log](evidence/concrete_semantics_haskell_cases.log)).
- Haskell proof compilation of `verification.k`: exit 0 ([kompile_proof.log](evidence/kompile_proof.log)).
- The one positive target command covers all seven claims in `spec.k`; it exits 0 and prints `#Top` ([kprove_all_positive.log](evidence/kprove_all_positive.log)).

Thus verification under the candidate theory reconstructs. The generated semantics does not faithfully execute all source-contract inputs and, as Stage 5 shows, disagrees with the real program even on a valid integer input.

## 4. Adequacy and real-program pinning

The seven entry claims mean:

1. `(3,4,5)` returns `VRounded(600)`.
2. `(5,12,13)` returns `VRounded(3000)`.
3. `(2,2,2)` returns `VRounded(173)`.
4. Every integer triple satisfying all strict triangle inequalities returns `VRounded(sqrtHundredths(heronRadicand(A,B,C)))`.
5. Every integer triple with `A+B <= C` returns `VInt(-1)`.
6. When the first guard is false but `A+C <= B`, the result is `VInt(-1)`.
7. When the first two guards are false but `B+C <= A`, the result is `VInt(-1)`.

Every precondition is satisfiable. Witnesses are respectively the three fixed inputs, `(3,4,5)` for the universal valid claim, `(1,2,10)`, `(2,5,3)`, and `(5,2,3)`. Concrete K and both Python results for these witnesses are recorded in [concrete_semantics_haskell_cases.log](evidence/concrete_semantics_haskell_cases.log).

Trusted regeneration plus a mechanical constructor comparison establishes program pinning: after deleting K whitespace outside string tokens, submitted `solution.mpy` and the RHS of `rule solutionProgram` are both 708 bytes and have the identical SHA-256 `0c8a60...642a`; see [program_term_comparison.log](evidence/program_term_comparison.log).

A body-sensitivity mutation changed the first return in the executed `solutionProgram` term from `-1` to `-2`. The mutated definition builds, concretely returns `VInt(-2)` for `(1,2,10)`, and the original claim fails with a stuck residual containing `VInt(-2)` ([verification-body-mutation.k](evidence/verification-body-mutation.k), [body_mutation_kompile.log](evidence/body_mutation_kompile.log), [body_mutation_concrete.log](evidence/body_mutation_concrete.log), and [body_mutation_kprove_expected_failure.log](evidence/body_mutation_kprove_expected_failure.log)).

Pinning does not make the theorem adequate. Claim 4's result symbol is the same exact-rounding abstraction introduced by the semantics, not a proved characterization of Python floating-point execution. Moreover, every symbolic claim requires `VInt` arguments. The natural-language source contract has no integer restriction, and the valid input `(3.0,4.0,5.0)` terminates with `6.0` in both Python implementations while the K program gets stuck. This is a material domain narrowing, not a harmless representation choice.

## 5. Rule-by-rule static soundness review

The complete numbered sources and declaration search are preserved in [k_sources_numbered.log](evidence/k_sources_numbered.log).

### Syntax, configuration, attributes, and functions

Every local declaration is inventoried here:

| File/lines | Declaration | Assessment |
|---|---|---|
| `semantic.k:14` | `Program ::= Module(Stmts)` | Matches the submitted module constructor. |
| `semantic.k:15` | empty-delimiter `Stmts` list | Matches translator juxtaposition. |
| `semantic.k:16-19` | `FuncDef`, empty-else `If`, `Assign`, `Return` | Exactly the statement constructors used. |
| `semantic.k:21-22` | `Params` and comma-separated `Strings` | Matches the function signature. |
| `semantic.k:24-27` | `Int`, `Float`, `Name`, `Call` expressions | Exactly the remaining used expression constructors. |
| `semantic.k:28-30` | strict unary, left-to-right `seqstrict` binary, strict comparison-left | Correct evaluation order for the submitted body. |
| `semantic.k:31-32` | `CmpOp` and comma-separated `Exprs` | Covers the single-link comparisons and call arguments. |
| `semantic.k:34-41` | `NumValue`, `Value`, `Values`, `Args` | Includes integers/rationals, a float token, symbolic square root, rounded cents, and booleans. Float input values are declared but material arithmetic rules are missing. |
| `semantic.k:51-57` | `<k>`, `<env>`, `<functions>`, `<result>` configuration | Sufficient for the one-module, one-call program; no call stack is modeled. |
| `semantic.k:59-63` | `Result`, values as `Exp`/`KResult`, stored `Function` | Internally consistent for this subset. |
| `semantic.k:64-72` | launch/execution/binding/branch/assignment/return/comparison/round continuations | Makes the used control states explicit. |
| `semantic.k:116` | `asRat(NumValue) [function,total]` | The two disjoint rules cover all `NumValue` constructors. |
| `semantic.k:156-159` | four `[function]` exact-square-root helpers | Not declared total. Ground nonnegative uses are algorithmically covered; the entry equation is restricted to concrete `R`. |
| `verification.k:10` | `solutionProgram [function]` | One exhaustive constant equation; mechanically equal to the translated program. |
| `verification.k:11` | `heronRadicand [function]` | One unguarded exact-rational Heron equation. |

There are no local `[functional]` declarations, priority rules, explicit opaque declarations, or proof-only ordinary/simplification rules. The only local `total` is `asRat`; the only `owise` rules are numeric promotion and comparison fallbacks; the only local simplification is `sqrtHundredths` with `[concrete(R), simplification]`.

### Ordinary and simplification rules

| Rule line(s) | Decision over its complete role |
|---|---|
| 75 | Loads the real module before invoking the named entry point; sound for the submitted single module. |
| 78 | Empty statement execution terminates; sound. |
| 79 | Executes the head statement before the tail; sound. |
| 81 | Stores the translated function binding; sound. |
| 84 | Looks up that binding, binds arguments, then executes its exact body; sound on the actual arity. |
| 87 | Empty parameter/value binding terminates; sound. |
| 88 | Left-to-right parameter binding updates the environment; sound on equal-length lists. |
| 92 | Evaluates an `if` guard before branching; sound. |
| 93 | Executes the true body; sound. |
| 94 | Empty-else false branch does nothing; sound. |
| 96 | Evaluates an assignment RHS before writing; sound. |
| 97 | Writes the translated name; sound. |
| 100 | Evaluates the return expression first; sound. |
| 101 | Discards the remaining one-call continuation and clears local/function maps; sound for this program's only active call, but deliberately not a reusable nested-call semantics. |
| 107 | Integer literal to `VInt`; sound. |
| 108 | Float literal to `VFloat`; sound only as token injection; no side-input float arithmetic follows. |
| 109 | Environment lookup; sound. |
| 112 | Integer unary minus; sound. |
| 113 | Exact-rational unary minus; internally sound. |
| 117 | `asRat(VInt(I)) = I`; sound exact embedding. |
| 118 | `asRat(VRat(R)) = R`; sound and disjoint from line 117. |
| 120 | Integer addition; sound and selected before the fallback. |
| 121-123 | Exact rational-promotion addition fallback; internally coherent, though not Python float promotion after true division. It is not exercised after division by this body. |
| 125 | Integer subtraction; sound. |
| 126-128 | Exact rational-promotion subtraction; follows the candidate exact model but skips Python binary-float rounding on the real valid path. |
| 130 | Integer multiplication; sound. |
| 131-133 | Exact rational-promotion multiplication; materially unfaithful once Heron's intermediates exceed binary64 precision. |
| 135-136 | Models Python true division as exact `Rat`, not binary64 `float`; materially unfaithful in general and the source of the later exact arithmetic path. |
| 137-138 | Replaces `x ** 0.5` with unevaluated `VSqrt(exact-x)`; a result-bearing abstraction, not execution of Python's float power. |
| 142 | Evaluates the right comparison operand after the left; sound order. |
| 143-144 | Integer `<=`; sound for all claim guards. |
| 145-147 | Exact-rational comparison fallback; internally sound, unused by the submitted integer guard path, and incomplete for declared `VFloat` inputs. |
| 152 | Recognizes the syntactic built-in `round` call and evaluates its argument; binding is fixed only by the minimal semantics. The actual program does not shadow `round`. |
| 153 | Converts the abstract square root directly to exact rounded cents. This is the critical unsupported/false bridge to Python behavior. |
| 154 | `round(integer,2)` remains the integer; consistent with CPython for this unused form. |
| 161-163 | Starts exact cents rounding; mathematically sound for the candidate exact model, but `[concrete(R)]` leaves the universal proof's symbol opaque and fails on LLVM. |
| 165-167 | Stops exponential upper-bound search once `H² > R`; sound on the reachable nonnegative invariant. |
| 168-170 | Doubles positive `H` otherwise; disjoint from line 165 and terminates for reachable finite nonnegative rationals. |
| 172-173 | Returns the lower bound when the interval width is at most one; sound under the reachable bracket invariant. |
| 174-177 | Moves the lower bound to a midpoint whose square is at most `R`; sound and descending under that invariant. |
| 178-181 | Otherwise moves the upper bound to the midpoint; guard is disjoint/exhaustive with line 174. |
| 183-184 | Rounds above the midpoint upward; sound exact arithmetic. |
| 185-186 | Rounds below the midpoint downward; sound exact arithmetic. |
| 187-189 | Exact tie with even lower cent rounds down; sound ties-to-even. |
| 190-192 | Exact tie with odd lower cent rounds up; sound and disjoint from line 187. |
| `verification.k:13-17` | Defines the exact-rational Heron radicand; algebraically sound, but it is a specification summary rather than Python-float semantics. |
| `verification.k:19-52` | Defines the exact submitted AST constant; sound and mechanically checked. |

The exact helper equations are ordinary mathematics; the illegitimate step is using their exact result as if it were the Python program result. No bridge-free universal connection theorem establishes that equivalence, and it is false. On the valid input

`(A,B,C) = (6,341,614, 3,071,071, 7,848,477)`,

all three strict inequalities hold. Trusted canonical Python and generated Python both terminate with `9268091090989.04`. The candidate exact arithmetic rules and rebuilt K execution produce `VRounded(926809109098905)`, corresponding to `9268091090989.05`. This is a concrete false-conclusion witness for the exact-promotion/multiplication, abstract-power, and exact-round bridge at lines 126-138 and 153. The witness calculation and actual `krun` output are in [numeric_semantics_witness.py](evidence/numeric_semantics_witness.py), [numeric_semantics_witness_python.log](evidence/numeric_semantics_witness_python.log), and [numeric_semantics_witness_krun.log](evidence/numeric_semantics_witness_krun.log).

The rules do not encode fixed task examples, but they replace the property-bearing computation with a materially different one. Finite small-case agreement cannot repair that false universal bridge.

## 6. Fresh non-vacuity test

I created a fresh universal valid-triangle claim whose expected cents are deliberately increased by one. `(3,4,5)` satisfies the precondition and demonstrates falsity (`600`, not `601`). The mutation parses and dry-runs successfully with exit 0 ([vacuity_dry_run.log](evidence/vacuity_dry_run.log)). The actual proof exits 1 with `WarnStuckClaimState`; its residual explicitly contains the failed equality between `sqrtHundredths(...) +Int 1` and `sqrtHundredths(...)` ([spec-vacuity.k](evidence/spec-vacuity.k), [vacuity_proof_expected_failure.log](evidence/vacuity_proof_expected_failure.log)).

This passes the discrimination check: the theorem is result-constraining inside its own theory. It does not validate the meaning of the result-bearing abstraction.

## 7. Proven versus assumed accounting

What the successful reachability proof actually establishes is:

- for the mechanically pinned AST and `VInt` arguments, the three guards follow K integer comparisons;
- invalid paths return K integer `-1`;
- valid paths return the same `sqrtHundredths(heronRadicand(...))` symbol that the candidate semantics introduces for exact-rational Heron arithmetic;
- three small ground instances reduce to the listed exact-cent integers.

Trusted or assumed boundaries are:

- K 7.1.293's compiler, Haskell backend, matching-logic prover, and builtin `INT`, `RAT`, `BOOL`, and `MAP` implementations;
- the trusted CPython-AST translator, whose output identity was checked;
- the mechanically checked `solutionProgram` constructor copy;
- an informal interpretation of `VRounded(N)` as the Python return `N/100`;
- an informal claim that exact rational Heron arithmetic plus exact square-root rounding equals CPython's binary-float `/`, multiplication, power, and `round`;
- ground termination/correctness of the concrete-only square-root helper;
- exclusion of float side inputs and other Python numeric behavior.

The first three boundaries are ordinary and acceptable. The source differential test supports only implementation-to-canonical fidelity on its finite sample. The last three are result-bearing and material. The `VRounded`/Python bridge is refuted by the valid integer witness, while float-side exclusion materially narrows the unrestricted source contract. The rebuilt `#Top`, generation trace, and finite tests therefore prove neither the real Python numeric behavior nor the full input domain.

The candidate is non-vacuous and program-pinned, but it proves a materially substituted numeric execution model and a narrowed theorem. Under the benchmark's decision boundary, either defect is `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
