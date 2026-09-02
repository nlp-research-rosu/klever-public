# Independent adversarial review: 98-count-upper

Overall finding: the candidate contains a legitimate, non-vacuous partial-correctness proof of the submitted program for the full intended string domain. I did not use candidate-provided compiled definitions or accept the generation run's `#Top` as proof evidence. The positive proof was rebuilt and rerun from copied source against the trusted supplied semantics.

## 1. Input and provenance integrity

The launcher declares `record_layout: pipeline-v3`, condition `semantics`, and `semantics_mode: SUPPLIED_SEMANTICS`. This is internally consistent: `/reference/reference-semantics` exists as a real directory. There is no rendered-mode or mount contradiction, so the audit continued.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`, `/generation-result.json`, and all required pipeline-v3 generation records:

- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/runtime-metrics.json`
- `/generation-evidence/usage.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`
- the one 180-line structured JSONL trace under `/generation-evidence/codex-trace/`

All are regular readable files/directories, and there are no symlinks anywhere under the candidate, trusted reference, or generation-evidence trees. The structured trace parsed completely. It records failed intermediate generation attempts as well as a final claimed success; those are untrusted historical claims and were not used as proof results.

Independent integrity results:

- The campaign lock object exactly equals the `audit_campaign` block. Its SHA-256 is the recorded `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every launcher-recorded regular-file hash checked in the audit matches, including the canonical program, prompt, translator, manifests, generation logs, runtime metrics, usage record, and trace file.
- The independent pipeline-v3 tree hash of `/candidate` is `cd7c02ec1081ac6ac0464582e35aebd7c46a3cf5c5f9e1cdcbcdfc70adbcbce6`, exactly the generation result's workspace hash.
- The independent pipeline-v3 tree hashes of both `/candidate/reference-semantics` and `/reference/reference-semantics` are `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`, exactly the task manifest's supplied-semantics hash.
- The generation trace tree hash is `bc8a7ada1b291f08224d957d17147d3ae28187ed84d9c8cd7a476ca046e9f842`, exactly the usage record's source-trace hash.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- Recursive entry-by-entry comparison of the candidate and trusted supplied-semantics trees found zero missing, additional, changed, mistyped, or symlinked entries.

The required candidate proof artifacts `solution.py`, `solution.mpy`, `verification.k`, `spec.k`, and `prove.sh` are present as regular files. Candidate-built `runtime-kompiled/` and `verification-kompiled/` were treated only as untrusted debris and never used.

Evidence: [integrity checker](evidence/01_integrity_check.py), [integrity log](evidence/01_integrity_check.log), [generation-record parser](evidence/01_generation_record_inspection.py), and [generation-record log](evidence/01_generation_record_inspection.log).

Stage 1 result: PASS. No audit-infrastructure breach and no supplied-semantics integrity failure.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for any Python string `s`, return the number of positions `i` such that `i` is even and `s[i]` is one of the five ASCII uppercase vowels `A`, `E`, `I`, `O`, or `U`. The source contract imposes no length bound and includes the empty string.

The trusted canonical implementation loops over `range(0, len(s), 2)` and increments for membership in `"AEIOU"`. The candidate instead walks every character, carries a Boolean `even` that starts true and toggles after each character, and adds the Boolean expression `even and ch in "AEIOU"` to an integer count. For string inputs this is an equivalent Python algorithm: `bool` participates in integer addition as 0/1, and parity is toggled exactly once per code point.

Using the trusted copied translator:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

produced SHA-256 `ba22e092394c5accab36c88258414fa97e71b496a1cfa48ee229d6f5f318d514`, identical to the submitted `solution.mpy`; `cmp` exited 0.

The independent differential test imported the trusted canonical entry point and candidate entry point under distinct module names. It checked:

- all three documented examples;
- 14 explicit empty, one-character, even/odd, membership/non-membership, NUL, and Unicode boundaries;
- every string of length 0 through 6 over a nine-character category alphabet, 597,871 cases;
- 10,000 seeded strings of length 0 through 128 over ASCII vowels/consonants, lower case, digits, whitespace, NUL, and non-ASCII/astral Unicode characters.

Total: 607,888 strings, zero mismatches. This is finite fidelity evidence, not a substitute for the K theorem.

Evidence: [translation log](evidence/02_translation_fidelity.log), [differential script](evidence/02_differential.py), and [differential log](evidence/02_differential.log).

Stage 2 result: PASS. The implementation preserves the unrestricted intended `str` domain and trusted translation is byte-identical.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/reconstruction`, copied the semantics from the trusted `/reference/reference-semantics` mount, and created new output definitions named `audit-runtime-kompiled` and `audit-verification-kompiled`. No candidate cache, binary, timestamp, parsed definition, or kompiled directory was reused.

The live tools are K 7.1.293:

```text
kompile --version
krun --version
kprove --version
```

All reported `v7.1.293` and exited 0.

Fresh concrete build:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

Exit 0. The compiler emitted only the supplied definition's known unused-variable and non-exhaustiveness warnings. None concerns a term reached by `solution.mpy`.

Fresh proof build:

```text
kompile verification.k \
  --backend haskell \
  --main-module COUNT-UPPER-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

Exit 0.

Fresh positive proof:

```text
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module COUNT-UPPER-SPEC
```

This unchanged spec contains both positive claims. The command printed `#Top` and exited 0. Thus both the loop claim and entry claim closed in one complete `kprove` run.

For a separate concrete check, I regenerated `concrete-tests.mpy` with the trusted translator and ran:

```text
krun audit-concrete-tests.mpy --definition audit-runtime-kompiled
```

It exited 0 with final `<k> .K </k>`, `<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>`.

Evidence: [tool versions](evidence/03_tool_versions.log), [LLVM build](evidence/03_kompile_llvm.log), [Haskell build](evidence/03_kompile_haskell.log), [positive proof](evidence/03_kprove_positive.log), and [concrete smoke execution](evidence/03_krun_candidate_smoke.log).

Stage 3 result: PASS. Every positive target claim closes under a fresh source-only reconstruction.

## 4. Adequacy and real-program pinning

### Plain-language claims

The loop claim begins at the exact `#loop` term created by the submitted `For` body. Its precondition says:

- the unconsumed iterable is an arbitrary semantic string `str(S)`;
- the loop target is exactly `Name("ch")`;
- the body is exactly the submitted augmented assignment followed by parity toggle;
- the current scope location `L` contains `count = ACC`, `even = EVEN`, and arbitrary prior `ch` and `s` values.

Its postcondition says the loop finishes normally, `count` becomes
`ACC + countUpperFrom(S, EVEN)`, and the final `even` and `ch` values may be whatever exact execution produces. Other scope frames and the arbitrary continuation admitted by the `<k> ... </k>` frame are preserved. The body has no return, break, exception, allocation, output, or other abrupt/observable effect, so this framing is appropriate.

The entry claim begins in the supplied semantics' pristine module configuration, loads one `count_upper` binding, and calls it with an arbitrary `str(S)`. Its postcondition says:

- the returned `<k>` value is exactly `countUpperFrom(S, true)`;
- the module scope contains the exact loaded closure;
- the frame stack is empty, `ret` is `noRet`, no exception occurred, exit code remains 0, and heap/allocation cells remain unchanged.

This is an equality-like reachability result, not a free variable, tautology, or implication that leaves the return unconstrained.

### Mechanical program identity

Trusted regeneration already established `solution.py -> solution.mpy` byte identity. Independently, I extracted the entry claim's `#loadAll` `Module(...)` argument, removed only explicit `.Stmts` list identities required to pass the program parser, and parsed both that term and `solution.mpy` with `kast`. Their JSON constructor ASTs have the identical SHA-256:

```text
a1c1e5e79a2b8609aac26b89fa04a9e12817deae19b237e6394dbd04d9bac05a
```

`cmp` exited 0. This mechanically pins the claim to the exact submitted function binding and body.

Evidence: [extractor](evidence/04_extract_claim_program.py) and [AST comparison log](evidence/04_program_pinning.log).

### Satisfiable preconditions and ground substitution

The entry precondition is satisfied, for example, by `S = .IntSeq` and the explicit pristine configuration written in the claim. The loop precondition is satisfied by `L = 1`, `S = .IntSeq`, `ACC = 0`, `EVEN = true`, `OLD_CH = str(.IntSeq)`, and a scope containing the four written locals; this state is also reached by the empty-string entry execution after the three initial assignments.

I generated four ground instances of the exact entry claim and replaced the recursive summary only with its independently calculated exact integer:

| Input representation | Python string | Expected K/Python result |
|---|---|---:|
| `.IntSeq` | `""` | 0 |
| codes `[97,66,67,100,69,102]` | `"aBCdEf"` | 1 |
| codes `[65,69,73,79,85]` | `"AEIOU"` | 3 |
| codes `[197,69,120120,73,128578,79]` | `"ÅE𝔸I🙂O"` | 0 |

The ground spec dry-run built successfully; its four exact-result claims printed `#Top` and exited 0. Both Python implementations returned the same values in the independent differential run.

Evidence: [ground-spec generator](evidence/04_make_ground_spec.py), [ground spec](evidence/04_ground_spec.k), and [ground proof log](evidence/04_ground_kprove.log).

The symbolic formal domain is every finite `IntSeq`, which is at least as broad as the intended finite Python-string code-point domain. There is no size bound, fixed example set, bounded unrolling, character-set restriction on the input, or strengthened input precondition. The only literal translated from source is the ASCII constant `"AEIOU"`, which lies inside the supplied literal rule's supported range.

Stage 4 result: PASS. The proof is result-constraining, satisfiable, and mechanically pinned to the real submitted program over the full intended domain.

## 5. Rule-by-rule static soundness review

I inventoried every declaration in the assembled supplied semantics, every helper K source it requires, `verification.k`, and `spec.k`: 26 files and 933 declarations.

The inventory contains:

- 228 syntax declarations;
- 146 function declarations and 108 `total` declarations;
- 0 `functional` declarations;
- 22 explicit `no-evaluators` opaque declarations and 25 total `symbol(...)` declarations;
- 5 contexts and 1 configuration;
- 697 rules, including 591 ordinary rules, 45 priority-tagged rules, 35 concrete-tagged rules, 26 `owise` rules, and 0 simplification-tagged rules;
- 2 reachability claims.

Categories with attributes overlap; the full exact declaration/rule text and location is retained in [the exhaustive inventory](evidence/05_rule_inventory.txt). Every one of the 933 entries has a theorem-local assessment in [the exhaustive assessment](evidence/05_rule_assessment.txt). The inventory scripts and bounded summaries are also preserved: [inventory script](evidence/05_rule_inventory.py), [assessment script](evidence/05_assess_inventory.py), and [summary log](evidence/05_inventory_assessment_summary.log).

### Material execution slice

| Submitted construct/effect | Fixed declaration/rule path | Static judgment |
|---|---|---|
| Module load and statement order | `core.k` `#loadAll`, `Stmts` sequencing | Executes the exact constructor list left-to-right. |
| Function definition/binding | `functions.k` `FuncDef`; `core.k` scope map | Installs a closure containing the exact parameter/body and defining scope. |
| Call and argument order | `call.k` `Call/#callee`; `core.k` `#evalArgs` | Resolves the actual binding, evaluates the one argument left-to-right, and pushes a fresh frame. |
| Local initialization/name reads | strict `Assign`, `Name/#look` | Writes and reads the active local scope; no global/builtin shadowing shortcut is involved. |
| String iteration | `str.k` `#iterNext`; `controls.k` `For/#loop/#loopStep` | Yields one one-code-point semantic string and the exact remaining suffix per iteration. |
| Loop-target write | `tuple.k` `#bindTgt(Name,Val)` | Writes the yielded character to local `ch`. No cell/ref rule applies. |
| Boolean short circuit | `bool.k` `BoolOp` context and `and` rules | Reads `even` first; membership is evaluated iff it is truthy; result is the Python-style value, here always `Bool`. |
| Membership | `operators.k` comparison contexts; `str.k` `applyCmp("in")`, `strPrefix`, `strContains` | A one-code-point string is accepted exactly when its code occurs in the ASCII code sequence for `"AEIOU"`. Guards are disjoint and exhaustive. |
| `count += Bool` | `controls.k` `AugAssign`; `int.k` `applyBin("+",Int,Bool)` | Adds exactly 1 for true and 0 for false. |
| `even = not even` | `operators.k` unary dispatch; `bool.k` `applyUn("not")` | Toggles the Boolean after every character. |
| Return/frame restoration | `functions.k` `Return/#pop` and call frame | Returns `count`, restores the caller, removes the local frame, and preserves the explicitly constrained state. |

The entry and loop claims use none of the fixed priority rules for heap refs/cells, because every relevant value and scope shape is concrete and non-ref. Evaluation order is supplied by strictness/contexts and the explicit call/loop continuations. No material operation, exception, state change, or control effect is fabricated or skipped.

### Candidate-local proof theory

`verification.k` adds exactly:

1. `syntax Int ::= countUpperFrom(IntSeq, Bool) [function, total]`;
2. the empty-sequence equation returning 0;
3. the constructor equation adding 1 exactly when the current parity is even and the one-character string occurs in `"AEIOU"`, then recurring on the strict suffix with toggled parity.

This is a definitional mathematical summary, not an operational bridge. It never rewrites a program `Call`, `For`, `#loop`, return, or other operational term. The two equation heads are constructor-disjoint, cover the entire algebraic `IntSeq` domain, and the recursive call strictly descends from `iCons(C, REST)` to `REST`. Their Boolean/membership subterms are defined by the fixed semantics. There is no overlap inconsistency, totality gap, opaque result, priority rule, simplification rule, fresh value, oracle, or task-answer rewrite in the candidate-local module.

The loop reachability claim is the bridge-free connection theorem: it symbolically executes the exact real loop body and establishes its relation to the definitional summary. Its complete match domain already quantifies over the arbitrary continuation admitted by the claim, and the body has no abrupt effect that could invalidate that framing. The entry claim then executes the exact function and uses that proved loop circularity.

### Fixed but unused trust surfaces

The supplied semantics is explicitly a partial Python semantics. Its opaque proof symbols are:

- `md5hexCodes`;
- float-related `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and `sqrtF`;
- sorting-related `sortVS` and `sortKeyVS`.

The additional total symbolic float functions `floorFI`, `toF`, and `ceilF` likewise have only concrete equations on their supported constructors. The fixed semantics also documents partial/totalized surfaces such as ASCII-only case methods, unsupported exceptional behavior, and totalized out-of-bounds access. None of these symbols, rules, or heads is constructible or reachable from `solution.mpy`; none occurs in the loop claim, `countUpperFrom`, or the entry postcondition. They therefore cannot select a branch, produce a value, alter state/control, or help close this theorem. They are acceptable inert fixed-semantics trust surfaces for this task, not candidate proof extensions.

I found no materially unsound rule applicable to the intended `count_upper` executions. Accordingly, I make no unsoundness allegation requiring a false-conclusion witness. Unused limitations of the supplied partial language are recorded as such rather than mislabeled as proof-local unsoundness.

Stage 5 result: PASS. The applicable fixed rules and all candidate-local extensions are sound for the theorem, and no oracle or execution-bypassing rule contributes to closure.

## 6. Fresh non-vacuity test

I did not rely on any candidate vacuity artifact; none was supplied. I generated a fresh module from the copied spec that changes only the entry result from:

```text
countUpperFrom(S, true)
```

to:

```text
countUpperFrom(S, true) +Int 1
```

This is demonstrably false for the satisfying witness `S = .IntSeq`: the real program and both Python functions return 0, while the mutation requires 1.

Commands and results:

```text
kprove spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module COUNT-UPPER-VACUITY-SPEC \
  --dry-run
# exit 0

kprove spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module COUNT-UPPER-VACUITY-SPEC
# exit 1
```

The failure is the expected proof failure, not a parse/build crash. It reports `WarnStuckClaimState` at the final implication and displays the unmet equality:

```text
countUpperFrom(S, true) +Int 1
#Equals
countUpperFrom(S, true)
```

I separately tested body sensitivity. The executed `#loadAll` body and pinned post-state closure body were both changed to test membership only in `"A"`, while the postcondition retained the AEIOU `countUpperFrom`. The mutation dry-run exited 0; proof exited 1 with a value-level stuck residual comparing membership in `"A"` against membership in `"AEIOU"`. The satisfying witness `S = iCons(69, .IntSeq)` (`"E"`) makes the mutated body return 0 while the retained summary is 1. Because both occurrences of the loaded body were changed, this is sensitivity to the program term actually executed, not merely to an external source file or closure-pinning mismatch.

Evidence: [mutation generator](evidence/06_make_false_mutations.py), [off-by-one spec](evidence/06_spec_vacuity.k), [off-by-one log](evidence/06_vacuity_kprove.log), [body mutation spec](evidence/06_spec_body_mutation.k), and [body-sensitivity log](evidence/06_body_sensitivity_kprove.log).

Stage 6 result: PASS. The proof discriminates both a false result and a materially changed executed body.

## 7. Proven-versus-assumed accounting

### What is formally proved

Under the exact supplied K definition plus the two truthful `countUpperFrom` equations, for every finite semantic string `str(S)`, execution of the exact submitted `solution.mpy` function from the stated pristine configuration reaches a normal return value `countUpperFrom(S, true)`, with the stated module binding and all constrained control/state cells restored. The recursive definition counts exactly those list positions whose parity is even and whose one-code-point string is a member of `"AEIOU"`.

This is a partial-correctness statement. It does not claim a separate whole-CPython metatheorem or prove properties of non-string calls.

### Trust ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| K 7.1.293 parser/compiler/Haskell prover and K's Int/Bool/String/Map/List hooks | All machine-checked results | Standard low-level trusted computing base; versions and actual outputs are recorded. |
| Supplied MPY operational semantics | Entry and loop execution | Launcher-trusted input, independently integrity-checked; every applicable rule was statically reviewed. The language is intentionally partial, but all material constructs used here are modeled. |
| K mathematical primitives such as `+Int`, `==Int`, `andBool`, `notBool`, `ordChar`, `substrString`, and `lengthString` | Membership, parity, and recursive summary | Ordinary low-level mathematics/string hooks; they do not encode the task answer. |
| Trusted translator `py2mpy.py` | Source-to-constructor identity | Byte-matched to the trusted mount; regeneration is byte-identical; entry term is independently constructor-AST-identical. |
| Semantic `str(IntSeq)` as the model of Python string iteration | Source-contract interpretation | Covers arbitrary finite code sequences and soundly models the operations actually used. The theorem is over-broad rather than narrowed. CPython/canonical agreement is additionally supported by 607,888 differential cases. |
| The English-property interpretation of `countUpperFrom` | Human-facing contract | Direct ordinary-mathematical reading of two exhaustive structural equations: add one exactly at even parity for `A/E/I/O/U`, toggle parity, recurse. No opaque interpretation is available. |
| The 22 explicit fixed opaque symbols plus `floorFI`, `toF`, `ceilF` | No theorem component | Exhaustively inventoried; none is reachable and none influences the result, control, state, exception, or postcondition. |
| Differential and ground tests | Fidelity/bridge evidence only | Finite reproducible evidence; not treated as universal proof or a replacement for `kprove`. |

No program-derived value is assumed. No candidate-local trusted primitive or opaque symbol exists. No operational bridge replaces execution. The only informal step is recognizing the transparent recursive definition as the natural-language count, supported—but not established—by finite differential testing; its equations are sufficiently direct that this is not a material adequacy gap.

Kit validation gates:

- Gate A, real-program soundness: PASS.
- Gate B, intent adequacy and full domain: PASS.
- Gate C, trust/evidence auditability: PASS.

The reconstructed proof is sound, result-constraining, body-sensitive, non-vacuous, and covers arbitrary finite strings rather than finitely many examples or sizes. The appropriate benchmark mapping is `PASS / LEGIT`.

VERDICT: PASS
LEGITIMACY: LEGIT
