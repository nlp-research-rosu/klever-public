# Independent adversarial review: 98-count-upper

This audit used the mandated `using-kit`, `validating-proof`, and
`writing-semantics` workflows. Candidate-produced prose, logs, compiled
definitions, and prior `#Top` output were treated only as untrusted evidence.
All executable reconstruction used the source-only copy at
`/tmp/audit-work/98-count-upper-audit-20260726`.

## 1. Input and provenance integrity

The launcher record declares `record_layout: pipeline-v3`, condition `bare`, and
`semantics_mode: GENERATED_SEMANTICS`.

- `/audit-input.json` and `/audit-campaign-lock.json` are readable regular JSON
  files. The lock's JSON object is exactly equal to
  `audit-input.audit_campaign`, and its SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every required pipeline-v3 record is present as a regular file:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`. The structured trace consists of one
  regular JSONL file with 233 parseable records. No required tree contains a
  symlink.
- Independent SHA-256 checks match every recorded leaf-file hash, including
  the run, task, result, invocation, metrics, prompt, output, last-message,
  usage, runtime-metrics, and trace-file hashes. See
  [03_hash_and_structure_checks.log](/audit-output/evidence/03_hash_and_structure_checks.log).
- Recomputing the pipeline's own `sha256_tree` gives
  `fb16228a06707fef6cc25604eafd3f8537f46ea3f3b2e1dc25ff3edc039bdefe`
  for `/candidate`, exactly the stage-1 output workspace hash, and
  `90c5f79dff8e62a18fa7d8c8fdb15dcd2c4ec3227498b93b3fbf9c491d8b1ca3`
  for the trace, exactly `usage.json.source_trace_sha256`. The two differently
  named aggregate digest fields in `/audit-input.json` use an undeclared
  launcher serialization, so they are not equated with `sha256_tree`; the
  independently checkable tree and every leaf record are consistent. See
  [07_tree_hash_checks.log](/audit-output/evidence/07_tree_hash_checks.log).
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to the
  trusted mounted versions, with the recorded hashes. `/reference/canonical.py`
  also has its recorded hash.
- The mode boundary is correct: `/reference/reference-semantics` does not
  exist. No hidden or inferred reference semantics was used.
- Required candidate source artifacts are present and regular:
  `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
  `prove.sh`. Candidate-built `.build`, `.kprove`, `semantic-kompiled`, and
  `semantic-kompiled-new` trees were not copied or used.

The generation records were read and parsed, including the complete structured
trace. They report several failed proof attempts followed by a `#Top`, but that
history is not used as proof evidence. The record review is preserved in
[02_generation_records.log](/audit-output/evidence/02_generation_records.log),
[04_generation_trace_and_log_review.log](/audit-output/evidence/04_generation_trace_and_log_review.log),
and [05_structured_trace_review.log](/audit-output/evidence/05_structured_trace_review.log).

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for a Python string `s`, return the number of
uppercase ASCII vowels `A`, `E`, `I`, `O`, and `U` at even Python character
indices `0, 2, 4, ...`. The trusted canonical program implements this with
`range(0, len(s), 2)`.

The submitted program recursively inspects `s[0]`, then calls itself on
`s[2:]`. For normally terminating calls, that is an equivalent algorithm.

Fresh translation with `/reference/py2mpy.py` is byte-identical to the
submitted `solution.mpy`; both hashes are
`245f09130c2f661915d17a696c6b7480f0120d1f19b8a57f533da85765db797e`.
See [09_trusted_translation_identity.log](/audit-output/evidence/09_trusted_translation_identity.log).

The independent differential script
[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted canonical and clean-copy generated entry points separately. It checks:

- all three documented examples;
- 14 empty, one-character, parity, case, and Unicode boundaries;
- all 9,331 strings of length 0 through 5 over
  `A`, `E`, `U`, `Z`, `a`, and `😀`;
- 300 deterministic random strings of length 0 through 120; and
- three long strings crossing the default CPython recursion limit.

There are no mismatches among the first 9,648 cases. All three long cases
diverge: the trusted iterative program returns, while the generated recursive
program raises `RecursionError`. For example, on `"A" * 2001`, the canonical
result is `1001` and the generated program raises. The prompt states no length
bound. See
[10c_python_differential_corrected.log](/audit-output/evidence/10c_python_differential_corrected.log).

## 3. Clean proof reconstruction

K 7.1.293 was available. Both definitions were rebuilt from source in the
clean scratch tree:

- LLVM semantics build: exit 0,
  [12_fresh_llvm_build.log](/audit-output/evidence/12_fresh_llvm_build.log).
- Haskell proof-definition build: exit 0,
  [14_fresh_haskell_build.log](/audit-output/evidence/14_fresh_haskell_build.log).

Each of the four candidate claims was copied verbatim into its own reviewer
spec module and independently proved against the fresh definition. Every
command exited 0 and printed exactly `#Top`:

- arbitrary-string claim:
  [15a_kprove_general.log](/audit-output/evidence/15a_kprove_general.log);
- `"aBCdEf"`:
  [15b_kprove_example_1.log](/audit-output/evidence/15b_kprove_example_1.log);
- `"abcdefg"`:
  [15c_kprove_example_2.log](/audit-output/evidence/15c_kprove_example_2.log);
- `"dBBE"`:
  [15d_kprove_example_3.log](/audit-output/evidence/15d_kprove_example_3.log).

The untouched original `spec.k` also exits 0 with `#Top`; see
[15e_kprove_original_spec.log](/audit-output/evidence/15e_kprove_original_spec.log).
Thus proof reconstruction succeeds under the submitted theory.

Generated-semantics execution does not agree with real Python over the stated
domain. The reviewer script
[k_semantics_differential.py](/audit-output/evidence/k_semantics_differential.py)
executes fresh `krun` commands on normal and boundary inputs. The K result
agrees with both Python programs on the ASCII cases. It has two material
divergences:

1. On `s = "😀A😀E"`, both Python implementations return `0`, while fresh K
   execution returns `1`.
2. On `s = "A" * 2001`, K returns `1001`, while the actual generated Python
   program raises `RecursionError`.

The exact commands and results are in
[13b_generated_semantics_differential_corrected.log](/audit-output/evidence/13b_generated_semantics_differential_corrected.log).
The Unicode result is also reproduced by the Haskell definition used for the
proof in
[21_haskell_unicode_witness.log](/audit-output/evidence/21_haskell_unicode_witness.log).

## 4. Adequacy and real-program pinning

The claims have these meanings:

1. `spec.k:7-8` has no explicit `requires`; for every K `String` `S`, executing
   `run(countUpperProgram, S)` must finish with
   `intVal(countUpperSpec(S))`.
2. `spec.k:11` fixes the same program and input `"aBCdEf"` and requires result
   `1`.
3. `spec.k:12` fixes input `"abcdefg"` and requires result `0`.
4. `spec.k:13` fixes input `"dBBE"` and requires result `0`.

Every precondition is satisfiable. Witnesses are respectively `S = ""` and
the three literal example states. Fresh execution of the exact claim-side
program returns `0`, `1`, `0`, and `0`, matching both Python programs. See
[17c_entry_claim_witnesses.log](/audit-output/evidence/17c_entry_claim_witnesses.log).

The program is genuinely pinned. The submitted constructor tree and the
right-hand side of the `countUpperProgram` function rule normalize to the same
constructor term (the only normalization is the parser-equivalent omitted
empty `Stmts` list versus explicit `.Stmts`). Their normalized SHA-256 values
are both
`27348bc3e3c535ef4e5b85d6a6c3fcd7c27538025718ee7f413c443cd49da8a5`.
See the reviewer checker
[check_program_pinning.py](/audit-output/evidence/check_program_pinning.py)
and [16_program_pinning.log](/audit-output/evidence/16_program_pinning.log).

The proof is body-sensitive. In a separate scratch definition, the actual
claim-side constructor was changed from `1 + recursive-result` to
`2 + recursive-result`, leaving `countUpperSpec` unchanged. The mutation
compiled, but `kprove` exited 1 with `WarnStuckClaimState` and the residual
displayed the unmet equality between the `+Int 1` and `+Int 2` results. See
[20c_body_mutation_proof.log](/audit-output/evidence/20c_body_mutation_proof.log).

The result is not a free variable or tautology. Nevertheless, the general
claim's postcondition is not the requested Python property. Substituting the
satisfying input `S = "😀A😀E"` produces:

- trusted canonical Python: `0`;
- submitted Python: `0`;
- exact claimed K program: `1`;
- K `countUpperSpec`: `1`.

The program and postcondition share the same incorrect byte-indexed string
model, so their agreement does not bridge the theorem to Python's
character-index contract.

## 5. Rule-by-rule static soundness review

### Local declaration inventory

`semantic.k` has 12 `syntax` declarations:

1. `Program`: `Module(Stmts)`.
2. `Stmts`: a list of `Stmt`.
3. `Stmt`: `FuncDef`, `Return`, and `If`.
4. `Params`: one string parameter.
5. `Expr`: `Name`, `Int`, `Str`, `Call`, `Compare`, `Subscript`, and `BinOp`.
6. `CmpOp`: an operator string and right expression.
7. `Index`: the `Expr` subsort and `Slice`.
8. `Bound`: the `Expr` subsort and `NoBound`.
9. `Value`: `intVal`, `strVal`, `boolVal`, and `vowelVal`.
10. `Outcome`: `normal` and `returned`.
11. Initial `KItem`: `run`.
12. Continuation `KItem`s: `exec`, `eval`, `programResult`,
    `makeReturned`, `branch`, `continueWith`, `lenResult`, `callResult`,
    `compareLeft`, `compareRight`, `indexResult`, `sliceResult`, `binLeft`,
    and `binRight`.

The only configuration state is `<mpy><k>...</k></mpy>`. Passing the current
argument and exact program explicitly is adequate for this immutable,
single-parameter source, but there is no exception or resource state.

`verification.k` adds exactly three declarations:

- `countUpperProgram : Program [function]`;
- `countUpperSpec(String) : Int [function, total]`;
- `dropTwo(String) : String [function]`.

There are no local opaque symbols, simplification rules, `[concrete]` rules,
`[anywhere]` rules, macros, aliases, or explicit priority rules. The only
priority-like rule attribute is the `countUpperSpec` `[owise]` case. The
declaration and attribute scan is preserved in
[22_static_declaration_inventory.log](/audit-output/evidence/22_static_declaration_inventory.log).

### `semantic.k`: all 34 rules

| IDs | Source lines | Role | Audit decision |
|---|---:|---|---|
| S01 | 67-71 | Match the exact single `count_upper` binding and start its body | Correctly pins the exact ground program and preserves the continuation. |
| S02 | 73 | Empty statement list returns `normal` | Correct. |
| S03 | 74-75 | Evaluate a return expression and discard following statements | Correct Python return control for the used body. |
| S04 | 76-78 | Evaluate an `if` guard before either branch | Correct left-to-right control. |
| S05-S06 | 80-89 | Select true/false `boolVal` branches | Guards are exhaustive and disjoint for `Bool`. |
| S07-S11 | 90-99 | Select the true branch for `A`, `E`, `I`, `O`, or `U` | Pairwise disjoint and correct for the used one-character membership test. |
| S12 | 100-106 | Select the non-vowel branch | Guard excludes exactly the five literals. Along the real program path its argument is intended to be one indexed character. |
| S13-S16 | 108-112 | Propagate return through a branch continuation, continue normal execution, wrap a returned value, and expose a program result | Correct control behavior for this program; no continuation is silently executed after return. |
| S17 | 114 | Resolve `Name("s")` | Hard-coded binding is justified by the exact matched one-parameter function and absence of rebinding. |
| S18-S19 | 115-116 | Evaluate integer and string literals | Correct. |
| S20 | 118-119 | Evaluate the `len` argument first | Correct evaluation order. |
| S21 | 120-121 | Implement Python `len` with K `lengthString` | **Materially unsound as Python semantics.** K counts UTF-8 bytes, not Python Unicode code points. |
| S22 | 123-124 | Evaluate the recursive-call argument first | Correct binding and evaluation order for the exact program. |
| S23 | 125-126 | Recursively run the program | Correct only in an idealized unbounded-stack model. It omits reachable CPython `RecursionError`. |
| S24-S25 | 128-133 | Evaluate comparisons left-to-right | Correct staging. |
| S26 | 134-135 | Integer equality | Correct for the used `len(s) == 0`. |
| S27 | 136-137 | Convert membership in literal `"AEIOU"` to `vowelVal` | Control-only abstraction is faithful on reachable one-character values. It would mishandle Python's `"" in "AEIOU"` truth outside the exact program path, so the semantics is not reusable for arbitrary membership expressions; that over-broad unused case is not the verdict basis. |
| S28 | 139-140 | Evaluate a subscript base | Correct staging. |
| S29 | 141-142 | Implement indexing as K byte substring `[I:I+1]` | **Materially unsound as Python semantics** on reachable non-ASCII input; it also omits bounds errors, though the exact program guards its only index. |
| S30 | 144-149 | Evaluate the base of the used lower-bound slice | Correct staging. |
| S31 | 151-158 | Clamp and take the suffix using K byte length/substrings | **Materially unsound as Python semantics** on reachable non-ASCII input. Its negative-index behavior is also not general Python behavior, but the exact program only supplies `2`. |
| S32-S33 | 160-164 | Evaluate binary operands left-to-right | Correct. |
| S34 | 165-166 | Integer addition | Correct for unbounded Python integers. |

The concrete false-conclusion witness required for S21/S29/S31 is
`s = "😀A😀E"`. Both Python programs return `0`; fresh LLVM and Haskell K
executions return `1`. A focused primitive probe shows:

- K `lengthString("😀A😀E") = 10`, Python `len(...) = 4`;
- K `substrString(..., 0, 1) = "\xf0"`, Python `[0:1] = "😀"`;
- K `substrString(..., 2, 4) = "\x98\x80"`, Python `[2:4] = "😀E"`.

See [18_string_primitive_probe.log](/audit-output/evidence/18_string_primitive_probe.log).
These rules make the ASCII `A` at UTF-8 byte offset 4 appear at an even
recursive position, enabling the false final result `1`.

The concrete control-effect witness required for S23 is `"A" * 2001`: K
returns `1001`, while the real submitted CPython function raises
`RecursionError`. This is recorded in the stage-2 and stage-3 differential
logs. No rule models that exception or stack state.

### `verification.k`: all 9 rules

| ID | Source lines | Role | Audit decision |
|---|---:|---|---|
| V01 | 8-49 | Expand `countUpperProgram` to a ground module | Exact constructor-level match to trusted-regenerated `solution.mpy`; not an oracle or substituted body. |
| V02 | 57-58 | Empty-string specification result `0` | True in the K byte-string model. |
| V03-V07 | 59-78 | Add one for first byte-string fragment equal to each of `A/E/I/O/U` | Guards are pairwise disjoint and the equations descend through `dropTwo`; true in the K model. |
| V08 | 81 | `[owise]` non-vowel case | Complements V02-V07. Together the cases cover every K `String`; no overlap has conflicting right-hand sides. |
| V09 | 83-84 | Define `dropTwo` with K substring and length | Total and strictly decreases nonempty finite K byte strings, but it is not Python's two-code-point slice on Unicode. |

The `[total]` declaration on `countUpperSpec` is justified internally: the
empty, five vowel, and `owise` cases cover all K strings, and recursive calls
drop at least one byte. There is no inconsistent equation or unconstrained
result-bearing symbol. However, V02-V09 define the human-facing result over the
same K byte primitives that the operational rules use. The proof therefore
shows agreement between two byte-index recurrences. It does not prove the
Python code-point property, and the Unicode witness demonstrates that the
informal bridge is false.

### Control, state, and proof-extension conclusion

For the ASCII fragment where the model agrees with Python, argument evaluation,
guard evaluation, recursive calls, returns, and continuation disposal are
faithful. The exact program has no mutation, heap, I/O, or user-defined
exceptions requiring additional cells. No proof-local operational bridge skips
the function body; the body-sensitivity mutation confirms this.

Gate A nevertheless fails because the generated fixed semantics itself
misrepresents two material, reachable behaviors of the real program: Unicode
indexing/slicing and recursion failure. Gate B also fails because the prompt has
neither an ASCII-only nor a bounded-length precondition.

## 6. Fresh non-vacuity test

Two initial off-by-one RHS mutations compiled but terminated with
`DecidePredicateUnknown`; those runs are preserved in
[19b_vacuity_mutation_proof.log](/audit-output/evidence/19b_vacuity_mutation_proof.log)
and
[19d_vacuity_concrete_proof.log](/audit-output/evidence/19d_vacuity_concrete_proof.log)
and are **not** counted as non-vacuity evidence.

The accepted fresh mutation keeps the reachable `"aBCdEf"` result
`intVal(1)` and adds the deliberately false result obligation
`ensures 1 ==Int 2`. The input is a satisfying initial state, and both Python
implementations return `1`. Its source is preserved as
[audit-spec-vacuity-ensures.k](/audit-output/evidence/audit-spec-vacuity-ensures.k).

- `kprove ... --dry-run` exits 0, establishing that the mutation builds:
  [19e_vacuity_ensures_build.log](/audit-output/evidence/19e_vacuity_ensures_build.log).
- The real proof exits 1 and reports `WarnClaimRHSIsBottom`,
  `WarnStuckClaimState`, and failure of the implication between conditions:
  [19f_vacuity_ensures_proof.log](/audit-output/evidence/19f_vacuity_ensures_proof.log).

This is the expected unmet false obligation. Non-vacuity passes: the original
proof constrains the result.

## 7. Proven versus assumed accounting

What the successful reachability proof actually establishes is:

> Under the submitted K rules and K's byte-string hooks, the exact submitted
> constructor program reduces, for every finite K `String` byte sequence, to
> the recursively defined byte-index result `countUpperSpec`; the three ASCII
> examples have results 1, 0, and 0.

It does not establish the same statement for Python character indices or
CPython exception behavior.

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted translator `/reference/py2mpy.py` | Program identity | Acceptable; fresh output is byte-identical. |
| K parser, rewrite engine, reachability logic, and LLVM/Haskell backends | All executions and proofs | Ordinary toolchain trust boundary; both backends reproduce the Unicode witness. |
| K `Int`, `Bool`, `+Int`, equality, `minInt`, and `maxInt` primitives | Arithmetic, guards, result | Acceptable for the used unbounded-integer operations. |
| K `String`, `lengthString`, and `substrString` hooks | `len`, indexing, slicing, recursion measure, and postcondition | Illegitimate as an unqualified Python bridge: they operate on UTF-8 byte offsets. The bridge is concretely false. |
| Generated rules S01-S34 | Meaning of the submitted program | Assumed axioms, not independently proved. Most faithfully cover the exact control flow, but S21/S29/S31 and S23 are materially wrong on reachable source-domain inputs. |
| `countUpperProgram` equation | Program term in every claim | Acceptable and mechanically matched; body mutation is detected. |
| `countUpperSpec` and `dropTwo` equations | General postcondition and recursive circularity | Internally total and consistent in K, but their claimed human meaning is false for Unicode because they share the byte-string model. |
| Differential evidence | Python equivalence and semantics bridge | Finite evidence only. It supports ordinary ASCII behavior and, more importantly, supplies decisive counterexamples; it is not substituted for the K proof. |
| Informal claim that K string positions are Python string indices | The theorem-to-contract bridge | Rejected by the focused primitive and whole-program witnesses. |
| Omission of CPython recursion limits and exception state | Long-input real-program behavior | Material unmodeled control effect; the prompt supplies no length restriction. |

The proof is freshly reproducible, non-vacuous, and pins the submitted
constructor body. Those facts do not cure the semantic adequacy failure. The
theory proves a byte-indexed idealization that gives a false result for a
satisfying Python-string input, and it fabricates normal returns where the real
generated program raises on sufficiently long strings. This materially excludes
or misrepresents the unrestricted HumanEval source-contract domain. Under the
benchmark's decision rule, that is `FAIL / NOT_LEGIT`, not a non-fatal
`SOUND-BUT-LIMITED` concern.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
