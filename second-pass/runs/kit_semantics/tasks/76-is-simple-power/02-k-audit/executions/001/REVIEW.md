# Independent audit: 76-is-simple-power

Overall finding: **CONCERNS / LEGIT**. The candidate contains a fresh-reconstructible, non-vacuous K reachability proof of the actual translated integer program. The two proof-local simplification rules are sound consequences of the recursive result predicate, and the target claim constrains the return value for arbitrary K integers. The concern is limited to the last intent bridge: equivalence between the recursive `simplePower` predicate and the English existential-power property is justified by ordinary induction but is not itself a K theorem. The prompt also does not expressly state the positive-integer domain on which the trusted canonical implementation is meaningful. Neither limitation permits a false conclusion about the submitted integer program or narrows the usual HumanEval domain.

## 1. Input and provenance integrity

I treated all candidate and generation records as untrusted evidence. I first read `/audit-input.json`. It declares `record_layout = pipeline-v3`, `semantics_mode = SUPPLIED_SEMANTICS`, problem `76-is-simple-power`, and the expected container mounts. `/reference/reference-semantics` is present, so the trusted mounts agree with the rendered semantics mode; this is not an infrastructure-error case.

All pipeline-v3 records required by the prompt are present, readable, and regular files: `/run.json`, `/task.json`, `/generation-result.json`, `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace. The trace contains 344 valid JSONL records. I inspected its record kinds, function-call list, and completion records. No required record, candidate proof artifact, or provenance mount is missing or mistyped, and recursive `lstat` inspection found no symlink or unsupported entry under `/candidate`, `/reference`, or `/generation-evidence`.

The campaign block in `/audit-input.json` is byte-for-byte the same JSON object as `/audit-campaign-lock.json`; the lock's independently computed SHA-256 is `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`, matching the recorded hash. All recorded per-file hashes checked in the integrity script match the mounted bytes. The independently recomputed launcher-style tree hashes are:

- candidate: `399a442a3f278b7b0453de046416fc8daeec3b5ff4f37118cd0fc3b1747983c9`, matching the generation workspace hash;
- candidate and trusted semantics, separately: `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`, matching the task manifest;
- structured trace: `091c14e9724a8a003937594ca7a4ccbdd1055c3a9a11fc1cb66eca7b2b8a9fdb`, matching `usage.json`.

Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted mounts. A recursive, no-symlink-following comparison of the complete candidate `reference-semantics/` and `/reference/reference-semantics` returns zero, including names, entry types, modes, and bytes. Thus the supplied-semantics integrity gate passes; this comparison does not bless the proof-specific additions in `verification.k`.

Commands, statuses, all checked hashes, manifest cross-checks, and bounded trace inspection are in [stage1-integrity.log](/audit-output/evidence/stage1-integrity.log); the reviewer-authored driver is [stage1_integrity.sh](/audit-output/evidence/stage1_integrity.sh).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract asks whether `x` is a simple power of `n`, expressed as `n**int = x`, and gives `1 = 4^0` as a positive example. The ordinary integer interpretation is therefore: return true iff there is a nonnegative integer exponent `e` with `n^e = x`. The trusted canonical program special-cases `n == 1`, then multiplies a running `power`, initially 1, by `n` while `power < x`.

The submitted `solution.py` is a factor-removal implementation. It handles `x == 1` and bases `0`, `1`, and `-1` explicitly; for every other nonzero integer base it repeatedly replaces `x` by `x // n` while `x % n == 0`, then returns whether the remainder is 1. Exact divisibility makes Python floor division equal exact integer division in the loop. For `|n| >= 2`, each iteration strictly reduces `|x|`, so the algorithm terminates on its claimed integer domain.

I copied source artifacts, not caches or compiled definitions, to `/tmp/audit-work/76-is-simple-power`. Running the trusted translator on the copied `solution.py` produced SHA-256 `93a94af76fbc21071079fa4fd389ee7b803508175709d48678f79ecf3789d5b8`, byte-identical to the submitted `solution.mpy`.

The independent differential test covers all six documented examples, 19 explicit branch-boundary cases, 4,020 cases with `x = 0..200` and `n = 1..20`, 1,331 signed-grid cases, and 1,000 deterministic generated cases: 6,003 unique pairs. The generated program has zero mismatches against an independent repeated-multiplication oracle and zero mismatches against the canonical program over the positive grid. Outside that material positive domain, it also exposes evidence rather than hiding it: the canonical program times out on 178 sampled zero/negative-base inputs and differs on 13 cases such as `(-8,-2)` and `(0,0)`, while the generated program agrees with the mathematical oracle. This is evidence that the canonical implementation is not an executable oracle for all signed integers, not a divergence on the usual intended domain.

The complete command log and results are in [stage2-fidelity.log](/audit-output/evidence/stage2-fidelity.log). The preserved test and driver are [independent_differential.py](/audit-output/evidence/independent_differential.py) and [stage2_fidelity.sh](/audit-output/evidence/stage2_fidelity.sh).

## 3. Clean proof reconstruction

I did not copy or reuse a candidate-built definition or cache. From the source-only scratch tree I ran:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled

kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC --claims SPEC.loop-invariant

kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC
```

Both compilations exit zero. The independently selected helper claim exits zero and prints `#Top`. The full proof, containing both the helper and target claim, exits zero and prints `#Top`. The bounded logs are [stage3-kompile-llvm.log](/audit-output/evidence/stage3-kompile-llvm.log), [stage3-kompile-haskell.log](/audit-output/evidence/stage3-kompile-haskell.log), [stage3-kprove-loop-invariant.log](/audit-output/evidence/stage3-kprove-loop-invariant.log), and [stage3-kprove-all.log](/audit-output/evidence/stage3-kprove-all.log).

For completeness, selecting only `SPEC.is-simple-power` leaves a stuck loop state because that filtering removes its helper claim; the nonzero diagnostic is preserved in [stage3-kprove-entry.log](/audit-output/evidence/stage3-kprove-entry.log). It is not a failed target set: the dependency is independently proved, and the ordinary full spec invocation proves the target with that dependency. This is analogous to filtering an imported lemma out of a theorem run.

I also translated and concretely ran [concrete_program.py](/audit-output/evidence/concrete_program.py), whose function AST is identical to the submitted function and whose assertions exercise documented, degenerate, signed, and large cases. `krun` terminates with `.K`, `NoExc`, and exit code 0; see [stage3-concrete.log](/audit-output/evidence/stage3-concrete.log). Compiler warnings concern unused variables in a supplied string rule and unused/non-exhaustive supplied helpers outside this program's dependency cone, not a proof failure.

## 4. Adequacy and real-program pinning

The helper claim says: for any local scope location `L`, initial nonzero integer `X`, and integer `N` with `|N| >= 2`, execute the real `%`-guarded `#while` that assigns `x = x // n`; if the final local is `XF`, then `(XF == 1)` is exactly `simplePower(X,N)`. A concrete satisfying state is `L=1`, local map `{x:8,n:2}`, parent 0. The loop ends at 1 and both sides of the postcondition are true.

The entry claim has no logical precondition beyond the K sorts `X:Int` and `N:Int`. It starts in a fully ground top-level state with the `is_simple_power` closure installed, executes `Call(Name("is_simple_power"), (X,N))`, and requires the result to be the defined Boolean `simplePower(X,N)`. A satisfying state is obtained with `X=8,N=2` and the exact ground cells shown in the claim. The result is not a free variable, tautology, or one-way implication.

I mechanically parsed both the submitted `solution.mpy` and the compiled JSON form of the spec. There is exactly one translated `FuncDef`, exactly one claimed closure, the parameters are constructor-identical, the capture environment is 0, and the normalized body constructor trees have the same SHA-256, `4faec87fe27497a6342f23688be7a62587cf2aee0f4821fb92812f971444c1e0`. The claim contains the same five `If` statements, `%` guard, `//` assignment, and final comparison in the same order. This is constructor-level pinning through the supplied `FuncDef`-to-closure rule, not resemblance to a substituted algorithm.

Concrete substitutions agree between the claim summary and generated Python: `(8,2) -> true`, `(3,2) -> false`, `(-8,-2) -> true`, and `(0,0) -> true`. The first two also agree with the trusted canonical on its meaningful positive domain. Fresh ground K claims for all four summaries return `#Top`.

The generated KASTs, comparison script, exact commands, witnesses, and ground checks are [stage4-solution-kast.json](/audit-output/evidence/stage4-solution-kast.json), [stage4-spec-kast.json](/audit-output/evidence/stage4-spec-kast.json), [program_pinning_check.py](/audit-output/evidence/program_pinning_check.py), [spec-ground-eval.k](/audit-output/evidence/spec-ground-eval.k), and [stage4-adequacy.log](/audit-output/evidence/stage4-adequacy.log).

## 5. Rule-by-rule static soundness review

The exhaustive inventory is [rule-inventory.tsv](/audit-output/evidence/rule-inventory.tsv), generated by [rule_inventory.py](/audit-output/evidence/rule_inventory.py). It contains an assessment for every one of the 940 local sentences across supplied `semantics.k`, all supplied helper K files, candidate `verification.k`, and `spec.k`:

- 228 syntax declarations;
- 1 configuration;
- 5 contexts;
- 704 rules;
- 2 claims.

The attributes include 147 `function`, 108 `total`, 25 `symbol`, 45 priority, 26 `owise`, 5 syntax macros, 2 simplifications, and the strictness declarations. There are no `functional` declarations. [used-construct-map.tsv](/audit-output/evidence/used-construct-map.tsv) maps every submitted constructor—module/function/parameters, calls and names, integers and Booleans, conditionals and comparison, unary minus, while, `%`, `//`, assignment, return, and statement sequencing—to its declarations and operational rules.

The used operational dependency cone has ordinary sequential evaluation and state behavior:

- `FuncDef` allocates the exact closure; call setup binds the two arguments in a fresh scope and return/pop rules restore the caller.
- Strict/heating contexts evaluate guards and operands in the supplied order.
- `If` selects by supplied truthiness; `#while` rechecks the guard and sequences its body.
- name lookup and assignment read and update the actual local map.
- `%` reaches supplied `pyMod`; `//` reaches supplied floor division; both are evaluated only in the branch where the source program has already excluded `n = 0, 1, -1`.
- return writes the computed Boolean and unwinds normally. The proof pins empty heap/stack, no exception, and exit code 0; no state or control effect is silently fabricated.

All proof-local rules were separately assessed:

1. The seven defining equations for total `simplePower` are disjoint and exhaustive over two integers. Degenerate bases are explicit. For `|N| >= 2`, nonzero/nonunit `X` either has nonzero Python modulus and returns false or has exact modulus zero and recurses on `X/N`; the latter strictly decreases `|X|`. These equations define the nonnegative-exponent power predicate.
2. The nondivisibility simplification `((X == 1) == simplePower(X,N)) => true` is sound. If `X=1`, the first equation gives true; otherwise, the guards exclude zero and the nondivisible equation gives false.
3. The exact-factor simplification `simplePower(X,N) => simplePower(X / N,N)` is sound under its guards. They imply `X != 1`, and `pyMod(X,N)=0` makes `(X-pyMod(X,N))/N` exactly `X/N`.

To avoid circularly accepting those two simplifications, I compiled [verification-base.k](/audit-output/evidence/verification-base.k), which contains the defining equations but omits both candidate simplifications. Three split universal claims—covering `X=1`, the nonzero/nonunit nondivisible case, and the exact-factor case—then prove `#Top`; see [spec-derived-lemmas-split.k](/audit-output/evidence/spec-derived-lemmas-split.k) and [stage5-kprove-derived-lemmas-split.log](/audit-output/evidence/stage5-kprove-derived-lemmas-split.log). Z3 independently finds the two missing arithmetic guard counterexample queries unsatisfiable ([derived-lemma-arithmetic.smt2](/audit-output/evidence/derived-lemma-arithmetic.smt2), [stage5-z3-derived-arithmetic.log](/audit-output/evidence/stage5-z3-derived-arithmetic.log)). An initially unsplit formulation gets stuck because the prover does not synthesize the arithmetic partition; [stage5-kprove-derived-lemmas.log](/audit-output/evidence/stage5-kprove-derived-lemmas.log) records that automation limitation rather than presenting it as contrary evidence.

The 45 priority rules are all in the byte-matched supplied semantics. The applicable call, scope, control, and integer cases are non-overlapping on this program's typed, ground state; higher-priority reference/heap variants do not match its plain integers and empty heap. The candidate adds no priority rule or semantic call interception. All 22 supplied `no-evaluators` functions (float operations, sorting helpers, MD5, and related conversions) and other broad collection/string machinery are absent from the constructor and rule dependency cone. Potentially partial fixed helpers such as out-of-bounds sequence lookup are likewise unreachable. Those out-of-cone rules are inventoried as inspected trust surface/evidence gaps, not declared unsound. I found no unsound rule and therefore assert no unsupported false-conclusion witness.

Finally, a body-sensitivity mutation changes the actual closure's final comparator from `x == 1` to `x == 0` while retaining the result obligation `(8,2) -> true`. It parses and runs but exits 1 with a reachable residual `false`, as recorded in [spec-body-sensitivity-audit.k](/audit-output/evidence/spec-body-sensitivity-audit.k) and [stage5-body-sensitivity.log](/audit-output/evidence/stage5-body-sensitivity.log). The theorem therefore depends on the executed body, not merely an external source file or function name.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh mutation [spec-false-result-audit.k](/audit-output/evidence/spec-false-result-audit.k) retains the exact submitted closure and initial cells but asserts that `is_simple_power(16,-2)` returns false. This is demonstrably false because `(-2)^4 = 16`.

The mutation builds far enough to execute the proof, reaches a normal final state with `<k> true ~> .K </k>`, and fails specifically because that result does not unify with false. `kprove` exits 1 and reports `WarnStuckClaimState`; it is not a parser error, timeout, missing import, or unrelated crash. The exact command, complete bounded residual, `KPROVE_EXIT_STATUS=1`, and expected-warning check are in [stage6-false-result.log](/audit-output/evidence/stage6-false-result.log). This passes the fresh non-vacuity gate.

## 7. Proven versus assumed accounting

What the reachability proof establishes is precise: under the byte-matched supplied MPY semantics plus `verification.k`, for arbitrary K integers `X,N`, partial-correct execution of the actual submitted closure returns the Boolean computed by the total recursive `simplePower(X,N)` definition. The auxiliary claim establishes the corresponding factor-removal loop relation for every nonzero `X` and every `|N| >= 2`. The theorem is not a finite example set or bounded unrolling.

The trust ledger is:

- **Supplied semantic primitives:** K unbounded integers/Booleans, hooked integer arithmetic, `pyMod`, floor/exact division, maps/lists, strictness/heating, closure/scope/call/return rules, and the Haskell backend/SMT implementation are trusted. This is the approved low-level semantics/toolchain boundary, not a proof-local encoding of the answer.
- **Proof-local definitions:** `simplePower` and its two simplifications are not treated as opaque or empirical. Their guarded partitions, descent, and derived-rule consequences were statically checked and independently reconstructed without the simplifications.
- **Opaque or broad imported symbols:** the supplied `no-evaluators` float/sort/MD5 family and unused broad library rules are trust surface but cannot be reached from this program or these claims. No result depends on them.
- **Intent bridge:** equivalence between the recursive predicate and “there exists an integer exponent `e >= 0` with `N^e=X`” follows by elementary induction on the number of exact factor removals, with explicit `0`, `1`, and `-1` cases. The candidate did not formalize that separate existential/inductive theorem in K. This is the principal documented concern.
- **Domain bridge:** the claim quantifies over all K integers and thus does not narrow the material positive-integer HumanEval domain. The prompt's word “number” does not expressly exclude non-integers, while the translator, canonical algorithm, and examples make integers—normally positive integers—the reasonable source-contract interpretation. Python floats, arbitrary objects, and Boolean-subclass behavior are outside what this MPY theorem states. Signed-integer behavior is broader than the canonical executable domain and agrees with the ordinary mathematical oracle.
- **Empirical evidence:** regeneration, concrete execution, differential tests, ground substitutions, and mutations support source pinning and non-vacuity only. They are not substituted for the universal K proof.

Accordingly, Gate A (theorem integrity), Gate B (intent on the material integer domain), and Gate C (evidence honesty) pass. The unformalized but straightforward existential-predicate bridge and the prompt/canonical extra-domain ambiguity are non-fatal trust-boundary limitations, warranting `CONCERNS` rather than `PASS`. There is no material domain narrowing, substituted program, unconstrained oracle, or rule capable of proving a false result for the intended integer program.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
