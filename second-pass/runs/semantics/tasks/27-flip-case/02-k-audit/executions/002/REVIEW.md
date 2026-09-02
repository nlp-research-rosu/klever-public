# Independent adversarial review: 27-flip-case

The candidate reconstructs cleanly, executes the submitted constructor tree, and
has a result-sensitive K claim. It nevertheless does **not** prove the full
HumanEval contract. The source contract accepts unrestricted Python `str`,
whereas the supplied K method semantics implements `swapcase` only for ASCII
letters. The claim has no ASCII precondition and equates execution with that
ASCII-only `mapSwap` result. A satisfying input `"é"` is therefore a direct
counterexample to the proof-to-source bridge: K proves that code point 233 is
unchanged, while both the trusted canonical program and submitted Python program
return code point 201 (`"É"`). The same mismatch occurs for `"ß"` (Python
returns `"SS"`) and `"Σ"` (Python returns `"σ"`).

This is a sound, non-vacuous theorem under the supplied MPY rewrite system, but
it is materially limited to the wrong character-case model. Under the benchmark
decision rule, that material source-contract domain/model restriction is
`FAIL / NOT_LEGIT`, not a non-fatal concern.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- `record_layout = legacy-selected-stage1`
- `semantics_mode = SUPPLIED_SEMANTICS`
- problem `27-flip-case`, condition `semantics`
- K version `7.1.293`

The mode and mounts are consistent: `/reference/reference-semantics` exists.
There is no infrastructure breach.

I read the launcher-owned audit input and campaign lock, then all records
required for `legacy-selected-stage1`: `/run.json`, `/task.json`,
`/generation-result.json`, `invocation.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the structured trace. `usage.json` is
present and was also inspected. Historical runtime metrics are not required for
this layout. The trace contains 114 JSONL records; every line parses. The
selected usage event, line 113, exists.

The campaign block is byte-for-byte equivalent as parsed JSON to
`/audit-campaign-lock.json`, whose independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching `/audit-input.json`. Every launcher-recorded regular-file hash checked
in the integrity script matches, including the run/task/result/invocation
records, generation logs and trace, prompt, canonical source, and translator.
The complete candidate file manifest with individual hashes is in the log.

The recursive candidate/trusted semantics comparison found exactly 25 entries
on each side, identical entry types and file bytes, no missing or additional
entries, and no symlinks. Candidate `prompt.py` and `py2mpy.py` are byte-identical
to their trusted mounts. Evidence:

- `/audit-output/evidence/check_integrity.py`
- `/audit-output/evidence/stage1-integrity.log` (exit 0)

Generation prose, prior `#Top` output, and the generation trace were treated
only as untrusted historical claims. None was used to establish proof success.

## 2. Program fidelity and candidate-versus-canonical checks

The contract in `/reference/prompt.py` is: for a given Python string, change
each lowercase character to uppercase and each uppercase character to
lowercase. The only example is `flip_case("Hello") == "hELLO"`. There is no
ASCII, length, or alphabet restriction. The trusted canonical implementation
returns `string.swapcase()`.

The candidate preserves the required signature and also returns
`string.swapcase()`. Thus the generated Python implementation is extensionally
the same algorithm as the canonical implementation over the intended Python
`str` domain.

Fresh translation used:

```text
python3 /reference/py2mpy.py /tmp/audit-work/27-flip-case/solution.py > /tmp/audit-work/27-flip-case/audit-regenerated.mpy
cmp /tmp/audit-work/27-flip-case/solution.mpy /tmp/audit-work/27-flip-case/audit-regenerated.mpy
```

Both files have SHA-256
`f34d90ab871c6106c87ea64aa17e5ae4da5bfd5e86ca7ce805959554f8ae8620`;
`cmp` exited 0.

The independent differential test imports the trusted canonical module and the
scratch candidate module separately. It covers the documented example, empty
input, ASCII case boundaries and immediate neighbors, digits, punctuation,
whitespace, NUL/DEL, non-Latin alphabets, Unicode characters with one-to-many
case maps, lone surrogates, the maximum code point, and 500 deterministic
generated strings (seed 270027, lengths 0 through 32). All 514 cases agree.
This establishes finite implementation/canonical evidence, not a K theorem.

- `/audit-output/evidence/differential_test.py`
- `/audit-output/evidence/stage2-fidelity.log` (exit 0, mismatches 0)
- `/audit-output/evidence/stage2-differential-inputs-and-results.log`
  (all 514 concrete inputs, exit 0)

## 3. Clean proof reconstruction

I copied source artifacts into `/tmp/audit-work/27-flip-case`, taking the
semantics from the trusted reference mount. No candidate compiled definition or
cache was copied or reused. Tool versions are recorded in
`/audit-output/evidence/toolchain-versions.log`.

Fresh concrete definition:

```text
kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled
```

Exit 0. The LLVM compiler reported pre-existing non-exhaustive-match warnings
for unrelated helpers and unused-variable warnings in `strLt`; it did not fail.
Both fresh concrete runs exited 0:

```text
krun solution.mpy --definition audit-runtime-kompiled
krun concrete-tests.mpy --definition audit-runtime-kompiled
```

The module-loading run and the three-assert smoke program both terminate at
`.K`, `NoExc`, and exit code 0. Logs:

- `/audit-output/evidence/stage3-kompile-llvm.log`
- `/audit-output/evidence/stage3-krun-solution.log`
- `/audit-output/evidence/stage3-krun-tests.log`

Fresh proof definition:

```text
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION --output-definition audit-verification-kompiled
```

Exit 0. The exhaustive claim inventory finds one and only one positive target
claim. It was independently run as:

```text
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
```

It exited 0 and printed `#Top`. Logs:

- `/audit-output/evidence/stage3-kompile-haskell.log`
- `/audit-output/evidence/stage3-kprove-positive.log`

Clean reconstruction therefore passes. This result alone does not validate the
source-level theorem.

## 4. Adequacy and real-program pinning

### Formal claim in plain language

The entry precondition has no side condition. `S` ranges over every algebraic
`IntSeq`. The machine state is the exact initial state: environment 0; empty
module scope whose parent is the builtins scope; fresh scope location 1; empty
heap; heap location 0; empty call stack; `noRet`; `NoExc`; exit code 0.

The postcondition requires the `<k>` result to be exactly
`str(mapSwap(S))`. It also requires the call environment, heap, heap location,
stack, return state, exception state, and exit code to be restored, while the
module scope contains the loaded `flip_case` closure with the claimed exact
body. This is an equality-bearing result, not a free variable, implication, or
tautology.

The precondition is satisfiable. Examples include:

- `S = .IntSeq` (the empty Python string)
- `S = [72,101,108,108,111]` (`"Hello"`)
- `S = [233]` (`"é"`)

### Constructor-level program identity

The claim does not textually begin with the module, but `#runFlipCase` rewrites
to `#loadAll(solutionModule)` followed by a normal call through the loaded
binding. I parsed both the trusted-regenerated `solution.mpy` and the
macro-expanded `solutionModule` with the fresh definition. Their complete KAST
outputs are byte-identical and share SHA-256
`12ac63791c78c80f0b440fb6945b6ae937c197ea59356a788fd59caf19737b54`.

- `/audit-output/evidence/kast-solution-audit.txt`
- `/audit-output/evidence/kast-claim-audit.txt`
- `/audit-output/evidence/stage4-pinning-and-ground.log`

There is no helper or loop claim. The actual path loads the submitted function,
looks it up by name, evaluates the string argument, allocates a normal call
frame, binds `string`, evaluates `Attribute(Name("string"), "swapcase")`,
dispatches the fixed method rule, returns, and pops the frame.

### Body sensitivity

The reviewer body mutation changes the constructor term actually loaded and
executed: the function returns `Name("string")` instead of calling `swapcase`.
Its separate definition builds successfully (exit 0), but the unchanged
`mapSwap` result obligation fails (exit 1) with the expected residual
`S #Equals mapSwap(S)`.

- `/audit-output/evidence/verification-body-mut.k`
- `/audit-output/evidence/spec-body-mut.k`
- `/audit-output/evidence/stage4-body-mutation-build.log`
- `/audit-output/evidence/stage4-body-mutation-proof.log`

This establishes that the positive proof is sensitive to the submitted body.

### Ground substitutions and source-level mismatch

| Satisfying input | Formal `mapSwap` result | Canonical Python | Candidate Python |
|---|---|---|---|
| `""` | `""` | `""` | `""` |
| `"Hello"` | `"hELLO"` | `"hELLO"` | `"hELLO"` |
| `"é"` | `"é"` | `"É"` | `"É"` |
| `"ß"` | `"ß"` | `"SS"` | `"SS"` |
| `"Σ"` | `"Σ"` | `"σ"` | `"σ"` |

The complete calculations are in
`/audit-output/evidence/adequacy_witness.py` and
`/audit-output/evidence/stage4-pinning-and-ground.log`.

Real-program pinning at the constructor level passes. Intent adequacy fails:
the formal result is not the real program's result on material inputs admitted
by the unrestricted `str` contract.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`/audit-output/evidence/rule-inventory.md` inventories every local declaration
in the trusted supplied tree, candidate `verification.k`, and `spec.k`: 230
syntax declarations, 698 rules, one configuration, five contexts, and one
claim, for 935 records. Each record includes source and line, complete
declaration text, attributes, role, reachability classification, and audit
determination. The generator and exact command log are:

- `/audit-output/evidence/rule_inventory.py`
- `/audit-output/evidence/stage5-inventory-command-v2.log` (exit 0)

Across the inventory there are 45 priority rules, 29 `owise` rules, 40
`concrete` rules, 22 `no-evaluators` declarations, and 25 explicitly named
`symbol(...)` declarations. There are no local simplification/simplifier rules
and no `functional` claims. The successful attribute inventory is
`/audit-output/evidence/attribute_inventory.py` with output in
`/audit-output/evidence/stage5-attributes-success.log`. A prior shell-only
attribute-summary attempt had a quoting error (the preserved
`stage5-attributes.log`, exit 2); it was not a build, proof, or evidentiary
result and was replaced by the successful script.

Declarations and rules outside the reachable constructor slice were still
inventoried and inspected for priorities, overlaps, global symbols, and heads
that could match the proof state. They are marked `FIXED-UNREACHED-*` in the
inventory. Their heads cannot arise from this submitted module or claim and
none contributes an equation to closure. They remain part of the
launcher-supplied fixed-semantics trust boundary; this review does not promote
their comments or opaque contracts into facts about full Python.

### Material construct-to-rule map

| Submitted construct/step | Declaration and behavior |
|---|---|
| `Module`, `FuncDef`, `Params`, `Return`, `Call`, `Attribute`, `Name` | `semantics/syntax.k:9-61` |
| Values, scopes, configuration, `IntSeq`, `str` | `semantics/core.k:13-60` |
| Module loading and statement sequencing | `semantics/core.k:124-127` |
| Name lookup and parent-scope traversal | `semantics/core.k:130-154` |
| Left-to-right argument evaluation | `semantics/core.k:183-191`, `213-215` |
| Function definition and closure installation | `semantics/functions.k:14-16` |
| Attribute cooling and ordinary call routing | `semantics/call.k:16-24` |
| Closure frame creation | `semantics/call.k:69-75` |
| Parameter binding, return, frame pop | `semantics/functions.k:62-90` |
| `swapcase` method dispatch | `semantics/methods.k:10`, `19-21` |
| Character predicates and case maps | `semantics/methods.k:112-164` |
| Candidate macros and entry launcher | `/candidate/verification.k:8-24` |

The lookup rules select the module's `flip_case` binding and then the callee
frame's `string` parameter. The cell-specific lookup/binding rules are
inapplicable because these plain frames have no `$cells` marker. Callee and
argument evaluation are ordered. The closure rule saves the continuation and
caller environment on the stack; `Return` sets `retV`; `#pop` restores all
observable call state. The string receiver is a value, so no heap dereference
or allocation affects this path. No exception, output, or hidden state is
abstracted.

The two case predicates are disjoint (`65..90` and `97..122`). The three
`swapC` branches are therefore non-overlapping; the `owise` case is their
complement. `mapSwap` has disjoint empty/cons equations and structurally
descends, so it is total on algebraic `IntSeq`. There is no totality,
termination, or overlap defect inside this ASCII model.

The proof-local extensions are also sound relative to the fixed semantics:

- `flipCaseBody` and `solutionModule` are definitional macros. Mechanical KAST
  comparison establishes exact constructor identity.
- `#runFlipCase` is a launcher for a fresh symbol, not an operational bridge
  that preempts fixed program execution. It introduces no result, return,
  exception, allocation, or state summary. Its framed continuation is
  preserved and the target claim invokes it only in the exact initial context.
- There are no proof-local opaque values, lemmas, simplifications, priority
  rules, or answer-encoding equations.

### False-conclusion witness for the material semantics gap

The rule group

```text
applyMethod(str(CS), "swapcase", .Vals) => str(mapSwap(CS))
swapC(C) => C + 32 when 65 <= C <= 90
swapC(C) => C - 32 when 97 <= C <= 122
swapC(C) => C otherwise
```

is coherent as an explicitly ASCII abstraction, but it is false if used as the
semantics of Python `str.swapcase` over the source-contract domain. Concrete
witness: `C = 233` (U+00E9, `"é"`). Both guards are false, so the `owise` rule
concludes 233. Python concludes 201 (U+00C9, `"É"`).

This is not merely an informal calculation. The ground K claim in
`/audit-output/evidence/spec-unicode-witness.k` proves with exit 0 and `#Top`
that the candidate execution returns `str(iCons(233,.IntSeq))`; the independent
Python execution in Stage 4 returns code 201:

- `/audit-output/evidence/stage5-unicode-k-witness.log`
- `/audit-output/evidence/stage4-pinning-and-ground.log`

The `"ß"` witness additionally shows that Python case conversion may change
length, something the pointwise one-code-to-one-code `mapSwap` representation
cannot express.

Thus there is no smuggled proof-local oracle, but the fixed primitive's
ASCII-only contract is materially inadequate for the real source operation.

## 6. Fresh non-vacuity test

No candidate mutation was trusted. I created a fresh module that leaves the
precondition and execution unchanged but falsely requires a leading exclamation
mark:

```text
str(iCons(33, mapSwap(S)))
```

This is demonstrably false at the satisfying input `S = .IntSeq`: the actual
program result is empty, not `"!"`. The spec parses and executes under the
already clean-built proof definition; `kprove` exits 1 with
`WarnStuckClaimState`. The residual is the expected unmet result equality:

```text
iCons(33, mapSwap(S)) #Equals mapSwap(S)
```

It is not a parser failure, missing import, timeout, crash, or unreachable
mutation.

- `/audit-output/evidence/spec-vacuity-audit.k`
- `/audit-output/evidence/stage6-vacuity-proof.log`

The target claim is therefore non-vacuous and result-constraining.

## 7. Proven versus assumed accounting

### What the successful proof establishes

Under the supplied MPY rewrite system, for every algebraic `IntSeq S` in the
exact initial configuration, executing the exact translated candidate module
through `#runFlipCase(S)` reaches `str(mapSwap(S))`; the loaded closure remains
in module scope, the caller environment and stack are restored, the heap is
unchanged, `ret` is `noRet`, no exception is set, and the exit code remains 0.
The theorem is discriminating and body-sensitive.

This is a theorem about the fixed MPY model. It does not establish that
`mapSwap(S)` equals Python `str.swapcase()` for unrestricted Python strings.

### Trust ledger

| Boundary | Effect/dependents | Evidence and judgment |
|---|---|---|
| K parser, compiler, Haskell prover, LLVM runtime, and built-in Int/Bool/String/Map/List hooks | All builds and proofs | External toolchain trust; version 7.1.293 recorded. Acceptable baseline, not proved here. |
| Trusted supplied MPY operational semantics | Entire reachability theorem | Integrity-checked and freshly compiled. Acceptable as the selected fixed theory, but its Python adequacy must still be audited. |
| Trusted translator | Source-to-`solution.mpy` bridge | Fresh byte-identical regeneration. Acceptable mechanical bridge. |
| Candidate macros | `solution.mpy`-to-claim program identity | Expanded KAST byte identity and body-sensitivity failure. Proven/audited, not merely assumed. |
| `str.swapcase` fixed primitive and `mapSwap` equations | Entire returned value and postcondition | Fully defined for ASCII codes, but the bridge to Python Unicode behavior is false. This is the illegitimate material boundary. |
| Python canonical implementation | Source-intent executable oracle | Trusted mounted input; candidate/canonical differential has zero mismatches. It supports implementation fidelity, not universal K adequacy. |
| Mapping `IntSeq` codes to Python string characters | Human-facing interpretation of the K result | Valid for exhibited scalar code points; arbitrary K `Int` values need not denote Python characters. This further shows the formal domain is not identical to Python `str`. |
| Finite differential and concrete tests | Candidate/canonical and selected execution evidence | Reproducible and useful only for tested inputs; not substituted for the K proof. |

The 25 explicitly named symbols imported by the fixed theory are:
`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
`roundFN`, `sqrtF`, `sortVS`, and `sortKeyVS`. Twenty-two have
`no-evaluators`; the remaining three have concrete-only defining cases over
their supported sorts. None occurs in the submitted program, entry claim,
normalized result, or reachable proof slice. They affect neither branch,
control, state, exception, nor result here. They are inventoried trust
boundaries of the broad supplied semantics, not assumptions used to close this
claim.

There are no proof-local opaque symbols or trusted proof lemmas. The only
informal semantic interpretation needed for the requested property is that
`mapSwap` means the natural-language case flip. That interpretation is valid
for ASCII letters and refuted on admitted Unicode strings.

### Gate and benchmark decision

- Gate A, fixed-theory real-term soundness: **PASS**. The clean theorem is
  non-vacuous, result-constraining, executes the exact generated term, and has
  no unsound proof-local extension.
- Gate B, intent adequacy: **FAIL**. The theorem's ASCII-only case model does
  not cover the material unrestricted Python `str` contract.
- Gate C, evidence auditability: **PASS**. Commands, sources, exits, and both
  positive and negative results are preserved; the failed source bridge is
  explicitly exposed rather than trusted.

The generic Kit characterization would be `SOUND-BUT-LIMITED`. The benchmark
prompt explicitly maps such a material HumanEval source-contract narrowing to
`FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
