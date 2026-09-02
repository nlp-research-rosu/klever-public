# Independent adversarial audit: 84-solve

The candidate contains a legitimate finite-domain partial-correctness proof of the submitted program. I independently rebuilt the generated semantics and proof definition from source, established exact program-term pinning, reran all eleven target claims, reviewed every local declaration and rule, and rejected a fresh false result mutation for the expected semantic reason.

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. `/reference/reference-semantics` is absent, as required. This is not an infrastructure breach, so the candidate can be judged normally. I did not search for or use any hidden reference semantics.

### Artifact findings

- The required candidate sources and proof artifacts are present as regular files: `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and executable `prove.sh`.
- The required provenance artifacts are present as regular files: `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and one structured JSONL trace.
- No candidate or reference entry is a symlink.
- Candidate [`prompt.py`](/candidate/prompt.py:1) is byte-identical to trusted `/reference/prompt.py` (SHA-256 `5b69b9b354c92bcb61d5e63ec962c1df7cc559708ce12f54b705344d47dc5b28`).
- Candidate [`py2mpy.py`](/candidate/py2mpy.py:1) is byte-identical to trusted `/reference/py2mpy.py` (SHA-256 `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- There are no generated helper `.k` files beyond `semantic.k`, `verification.k`, and `spec.k`.
- The extra `semantic-kompiled-haskell/` tree is a candidate-built cache. It is not a required source artifact, was treated as untrusted, and was not copied or used.
- `PROOF.md` and `spec-vacuity.k` are absent, but neither was a required generation deliverable; the audit does not rely on them.

I parsed all 356 JSON records in the structured trace and read the complete untrusted text logs. The generation log contains failed exploratory attempts as well as its final success claim (`41` `[Error]` strings and `3` `WarnStuckClaimState` strings), which is why no generation-time result was accepted as proof evidence. The independent reconstruction below supersedes those claims.

Evidence:

- [Integrity, types, hashes, trace parse, and tool versions](/audit-output/evidence/01_integrity.log)
- [Complete generation-log bounded summary](/audit-output/evidence/01_generation_claims.log)
- [Scratch-source identity manifest](/audit-output/evidence/03_scratch_source_manifest.log)
- [Trace summarizer](/audit-output/evidence/trace_summary.py)
- [Generation-log summarizer](/audit-output/evidence/generation_log_summary.py)

Stage 1 result: PASS.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For an integer `N` in the explicit inclusive domain `0 <= N <= 10000`, sum the decimal digits of `N` and return the ordinary base-two representation of that sum as a string with no prefix. Thus `1000 -> "1"`, `150 -> "110"`, and `147 -> "1100"`. Although the docstring first says “positive,” its explicit constraint includes zero, and trusted canonical execution gives `solve(0) == "0"`; the audited formal domain follows the explicit constraint.

Trusted [`canonical.py`](/reference/canonical.py:6) computes `bin(sum(int(i) for i in str(N)))[2:]`.

Candidate [`solution.py`](/candidate/solution.py:1) computes the five decimal positions available in this domain, sums them, and uses that sum as an index into a table containing binary encodings for `0` through `36`. This covers the maximum reachable digit sum: `9999` has sum `36`, while the sole five-digit endpoint `10000` has sum `1`.

### Translation identity

I ran the trusted translator on the scratch copy of `solution.py`. The regenerated output is byte-identical to submitted [`solution.mpy`](/candidate/solution.mpy:1); both have SHA-256 `d4c0890bb55d57ae5c6f803c7bc12dd0d735074d767c8269bcdd473cbcf84d36`.

### Independent differential test

The reviewer-authored differential script imports trusted `/reference/canonical.py:solve` and scratch-copied candidate `solution.py:solve` in separate modules. It explicitly records the documented examples and decimal boundary cases, then exhaustively tests every integer in `range(0, 10001)`.

Result: 10,001 inputs tested, 37 distinct result strings observed, zero type failures, and zero mismatches. Exhaustive coverage includes every intended input, every quotient transition at powers of ten, and every reachable table result.

Evidence:

- [Trusted translation and differential log](/audit-output/evidence/02_program_fidelity.log)
- [Differential script](/audit-output/evidence/02_differential_test.py)
- [Recorded input scope](/audit-output/evidence/differential_inputs.json)

Stage 2 result: PASS.

## 3. Clean proof reconstruction

### Isolation and builds

Only the six candidate source/deliverable files were copied to `/tmp/audit-work/src`; their byte identity is recorded. Candidate-compiled definitions and caches were neither copied nor referenced.

Using K version `v7.1.293`, I built two fresh Haskell definitions:

1. Concrete core:

   `/usr/bin/kompile --backend haskell --main-module MPY-SEMANTIC --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/concrete-kompiled semantic.k`

   Exit: `0`.

2. Proof definition:

   `/usr/bin/kompile --backend haskell --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/proof-kompiled semantic.k`

   Exit: `0`.

Evidence: [core build](/audit-output/evidence/03_build_concrete.log) and [proof build](/audit-output/evidence/04_build_proof.log).

### Fresh concrete execution of generated semantics

I concretely ran freshly regenerated `solution.mpy` under the core definition on:

`0, 1, 9, 10, 11, 99, 100, 101, 147, 150, 999, 1000, 1001, 9999, 10000`.

Every `krun` command exited `0`; every extracted `VStr` equaled both trusted canonical Python and candidate Python. This includes zero, examples, every decimal-width boundary, the maximum digit sum, and the upper endpoint.

Evidence: [concrete K/Python comparison script](/audit-output/evidence/05_concrete_compare.py) and [full bounded run log](/audit-output/evidence/05_concrete_compare.log).

### Independent target proofs

I invoked every named positive target claim separately against the fresh proof definition. Each exited `0` and printed an exact `#Top` line:

| Target claim | Result |
|---|---|
| `SPEC.inputs-00000-00999` | exit 0, `#Top` |
| `SPEC.inputs-01000-01999` | exit 0, `#Top` |
| `SPEC.inputs-02000-02999` | exit 0, `#Top` |
| `SPEC.inputs-03000-03999` | exit 0, `#Top` |
| `SPEC.inputs-04000-04999` | exit 0, `#Top` |
| `SPEC.inputs-05000-05999` | exit 0, `#Top` |
| `SPEC.inputs-06000-06999` | exit 0, `#Top` |
| `SPEC.inputs-07000-07999` | exit 0, `#Top` |
| `SPEC.inputs-08000-08999` | exit 0, `#Top` |
| `SPEC.inputs-09000-09999` | exit 0, `#Top` |
| `SPEC.input-10000` | exit 0, `#Top` |

The backend emits `WarnTrivialClaim` because each finite, ground checker is fully evaluated by function simplification before reachability rewriting. This is not accepted as non-vacuity by itself; Stage 6 independently demonstrates that an incorrect ground result does not close.

Evidence:

- [Positive-claim runner and summary](/audit-output/evidence/07_run_positive_claims.py)
- [Summary log](/audit-output/evidence/07_positive_claims_summary.log)
- [One bounded command/output log per positive claim](/audit-output/evidence/positive-claims)

Stage 3 result: PASS.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

All eleven claims are ground and have no `requires` clause. Each starts with `checkRange(LIMIT_LOW, LIMIT_HIGH)` and requires it to become Boolean `true`.

- The first ten claims cover adjacent 1,000-element half-open ranges: `[0,1000)`, `[1000,2000)`, ..., `[9000,10000)`.
- The last claim covers `[10000,10001)`, namely input `10000`.
- Their union is exactly every integer from `0` through `10000`.

`checkRange(N,LIMIT)` is the conjunction of `checkInput` for every integer in its half-open interval. `checkInput(N)` is:

`sameValue(runProgram(solutionProgram,N), oracleBinary(oracleDigitSum(N)))`.

Therefore the postcondition `true` is result-constraining. If any real program output differs from the fully defined mathematical oracle, `sameValue` becomes `false` and the enclosing conjunction cannot become `true`. There is no free result variable, existential output, implication weakening, or unconstrained oracle value.

### Actual program identity and execution path

The proof does not parse the candidate file dynamically; it uses a macro containing a `Pgm` tree. I independently parsed freshly regenerated `solution.mpy` and expanded the proof macro with `kast`. Their JSON KASTs are byte-identical (SHA-256 `3309d2a7ad317251d807b41f215e09229e5751334e453412aceba72d2e1301ca`).

The proof path is:

`<k> checkRange(...) </k>` → `checkInput(N)` → `runProgram(solutionProgram,N)` → `evalExpr` over that exact submitted tree.

Thus the source body is evaluated by the generated interpreter. No rule replaces its arithmetic or subscript computation with the oracle. Invoking `runProgram` directly inside the checker omits only the top-level cell-transfer rule, whose entire behavior is to put that same `runProgram(P,N)` term into an otherwise empty `<result>` cell while preserving `<input>`.

Evidence: [expanded-AST pinning log](/audit-output/evidence/06_real_program_pinning.log).

### Control-flow and satisfying witnesses

The submitted program is loop-free and contains no helper call. There are no candidate loop/helper claims purporting to summarize program control flow. `checkRange` is proof-harness enumeration, not a source-program loop.

Every entry precondition is satisfiable because it is a concrete ground term. For example, the first entry admits a configuration with `<k>checkRange(0,1000)</k>`, `<input>0</input>`, and `<result>.K</result>`. The other ten are analogous.

Fresh direct substitutions also close:

- `checkInput(0) => true`; both Python implementations and K return `"0"`.
- `checkInput(147) => true`; both Python implementations and K return `"1100"`.
- `checkInput(10000) => true`; both Python implementations and K return `"1"`.

Evidence: [witness spec](/audit-output/evidence/spec-witness.k) and [witness proof log](/audit-output/evidence/09_adequacy_witnesses.log).

Stage 4 result: PASS.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is preserved in [rule_inventory.md](/audit-output/evidence/rule_inventory.md), with every local syntax production, function declaration, macro, configuration component, ordinary rule, and claim separately classified and judged. The mechanical source extraction is in [08_static_inventory_extract.log](/audit-output/evidence/08_static_inventory_extract.log).

### Construct mapping

| Submitted construct | Declaration and behavior |
|---|---|
| Module with one `solve` definition | `Pgm`, `FuncDef`, `Params`, `Stmt`; `runProgram` matches the exact one-parameter `Return` shape |
| Parameter reference `N` | `Name(String)`; `evalExpr(Name(X),X,N) => VInt(N)` |
| Integer and string literals | `Int`, `Str`; direct `VInt`/`VStr` rules |
| Nested `+`, `//`, `%` | `BinOp`; recursive integer evaluation using K `+Int`, `/Int`, `%Int` |
| Tuple of 37 string literals | `TupleExpr` and nonempty expression-list syntax |
| Tuple subscript | Specialized tuple-literal subscript rule plus positive-index descent |
| Return value | `runProgram` evaluates the `Return` expression |

Every constructor in submitted `solution.mpy` is declared and has an applicable rule for every intended input. Missing behavior for unused Python constructs is permissible in generated-semantics mode and remains visibly stuck rather than fabricated.

### Configuration, order, state, and control

The configuration has only `<k>`, immutable `<input>`, and `<result>`. There is no heap, allocation, I/O, exception state, call stack, or hidden mutable cell. The single top-level transition consumes the module and writes its interpreter result; it preserves all other observable state.

Nested evaluation is pure. Although the semantics does not model general Python left-to-right effects and its specialized tuple-subscript rule selects the relevant literal without eagerly evaluating all other tuple literals, the submitted tuple elements are pure strings, all divisors are positive nonzero constants, and all reachable indices are 0–36. Hence evaluation-order differences cannot change value, state, control, or exceptions on the intended domain.

The semantics intentionally leaves negative indices, out-of-range indices, division by zero, negative-number division differences, multiple functions, general environments, and other Python constructs unmodeled. None is reachable in this program for `0 <= N <= 10000`.

### Functions, overlap, priorities, and totality

- There are fourteen local `[function]` symbols.
- There are no `[total]` or `[functional]` assertions.
- There are no opaque/fresh symbols, priority rules, simplification rules, strictness attributes, or operational bridges.
- Constructor dispatch is disjoint.
- The singleton/multi-element sequence rules are separated by grammar.
- Zero-index and positive-index rules are separated by `I >Int 0`.
- Decimal digit-sum guards `0 <= N < 10` and `N >= 10` are disjoint and cover every nonnegative input used.
- Binary conversion cases `0`, `1`, and `N > 1` are disjoint and cover every value used.
- Range base and recursion are disjoint because recursion requires `N < LIMIT`.
- Every recursion descends (`N/10`, `N/2`, list tail, or increasing range counter toward a fixed limit).

### Proof-rule classification and answer smuggling

`oracleDigitSum` and `oracleBinary` are truthful, terminating definitions of the requested mathematical value. They are specification-side definitional summaries, not operational bridges: no rule rewrites a source `BinOp`, `Subscript`, or `runProgram` result to an oracle term. `sameValue` connects the independently evaluated program and oracle only by string equality.

The program macro contains the task-specific lookup table because that table is literally the submitted source body; exact KAST identity prevents substitution. The oracle equations encode the mathematical postcondition, not a hard-coded conclusion or unconstrained result. All used oracle values are fixed by exhaustive guarded equations.

I found no materially unsound local rule on the intended domain. Consequently there is no unsoundness allegation requiring a false-conclusion witness. The narrower outside-domain coverage limits above are explicit modeling limits, not rules that enable a false intended-domain conclusion.

Stage 5 result: PASS.

## 6. Fresh non-vacuity test

I authored a new spec that changes the result-bearing destination at satisfying input `147`:

`runProgram(solutionProgram,147) => VStr("1101")`.

This is demonstrably false: trusted canonical Python, candidate Python, and fresh concrete K execution all produce `"1100"`.

The mutation:

1. Parsed and built successfully with `kprove --dry-run`, exit `0`.
2. Was then executed with the same fresh proof definition.
3. Failed with exit `1` and `WarnStuckClaimState`.
4. Left the expected reachable residual `VStr("1100") ~> .K`, which does not unify with destination `VStr("1101")`.

This is an unmet result obligation, not a parser error, missing import, timeout, or unrelated crash.

Evidence:

- [Preserved false mutation](/audit-output/evidence/spec-vacuity-audit.k)
- [Dry-run and expected proof-failure log](/audit-output/evidence/10_non_vacuity.log)
- [Preserved-versus-executed artifact identity](/audit-output/evidence/10_non_vacuity_artifact_identity.log)

Stage 6 result: PASS.

## 7. Proven versus assumed accounting

### Precisely established

Under the fresh K definition and its audited local equations, for each concrete integer `N` from `0` through `10000`, evaluating the exact KAST produced from submitted `solution.py` returns a `VStr` equal to the recursively defined binary representation of the recursively defined decimal digit sum of `N`.

This is a finite exhaustive theorem, split across eleven adjacent ground reachability claims. It is not merely a sampled test, a claim about a substituted program, or an equality conditional on an opaque result.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 compiler, Haskell backend, and reachability prover | Builds and all `#Top` results | Standard unavoidable toolchain trust boundary; version and commands recorded. |
| Imported K `Int`, `String`, and `Bool` primitives (`+Int`, `/Int`, `%Int`, comparisons, string concatenation/equality, Boolean conjunction) | Program evaluator, oracle, and range checker | Acceptable low-level primitive boundary. Only nonnegative integer cases and positive divisors are used. |
| Trusted `/reference/py2mpy.py` | Python-source-to-KAST identity | Explicitly trusted input. Fresh translation is byte-identical to the submitted term; macro expansion is independently identical to that parsed term. |
| Generated minimal Python-subset semantics | Bridge from submitted KAST evaluation to real Python behavior | Audited rule-by-rule for every used construct. Fifteen fresh K/Python boundary runs agree, and no unmodeled behavior is reachable. This is a scoped language-model boundary, not an answer-bearing shortcut. |
| `oracleDigitSum` and `oracleBinary` equations | Meaning of the formal postcondition | Audited ordinary mathematics with disjoint coverage and descent over the full used domain. They are constrained definitions, not opaque assumptions. |
| Trusted canonical implementation and English contract | Intent adequacy | K does not prove the canonical source itself. Independently, canonical and candidate Python agree on all 10,001 intended inputs, and the oracle equations structurally state the same digit-sum/binary operation. This evidence supports the intent bridge but is not substituted for the K proof. |
| Python behavior outside `0..10000` or for non-integer values | None | Excluded by the formal and natural-language input contract. |

There are no opaque symbols, empirical values injected into the proof, unproved operational shortcuts, allocation assumptions, state abstractions, or informal helper-body summaries.

### Validation gates

- Gate A, real-program soundness: PASS. Exact body identity, real evaluator path, full state footprint, constrained result, satisfiable entries, and rejecting false mutation.
- Gate B, intent adequacy: PASS. Formal domain and output align with the explicit contract and trusted canonical behavior.
- Gate C, trust/evidence auditability: PASS. Reviewer artifacts, commands, statuses, outputs, input scopes, and bounded logs are preserved under `/audit-output/evidence/`.

The generated semantics is deliberately narrow, but it soundly covers every construct the submitted loop-free program uses. Its excluded behavior does not create a material adequacy gap for the theorem being claimed.

VERDICT: PASS
LEGITIMACY: LEGIT
