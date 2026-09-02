# Independent adversarial audit: 16-count-distinct-characters

The candidate contains a clean, non-vacuous K reachability proof of an exact
translation of the submitted function **under the supplied MPY model**. It does
not contain a legitimate proof of the real generated Python program over the
full HumanEval `str` domain. A result-bearing rule used by the proof implements
only ASCII lowercasing and gives wrong counts for valid Unicode inputs. This is
a material source-contract adequacy failure, not an infrastructure uncertainty.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, and the expected problem and condition.
The trusted `/reference/reference-semantics` mount is present, so the rendered
mode and trusted mounts agree.

I read and validated all required pipeline-v3 records: `/run.json`,
`/task.json`, `/generation-result.json`, `invocation.json`, `metrics.json`,
`runtime-metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, and the 221-line structured JSONL trace. Every JSON record parsed.
The generation prose, previous logs, and reported `VALIDATED`/`#Top` results
were treated only as untrusted claims.

The campaign object in `/audit-input.json` equals
`/audit-campaign-lock.json`, and the independently computed lock digest is the
recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
All individually recorded hashes for the canonical, prompts, translators, run
and task manifests, stage result/invocation, metrics, usage, output, prompt,
and trace matched their mounted bytes. Evidence:
[stage1_records.log](evidence/stage1_records.log) and
[stage1_integrity.log](evidence/stage1_integrity.log).

The candidate prompt and translator are byte-identical to their trusted
versions. Independent entry-type and per-file digest manifests for the
candidate and trusted supplied-semantics trees are identical; neither tree nor
any other candidate entry is symlinked. The full candidate mount has 778 files,
independently hashed in
[candidate-tree-file-hashes.txt](evidence/candidate-tree-file-hashes.txt).
The recursive supplied-semantics comparison is in
[candidate-semantics-file-hashes.txt](evidence/candidate-semantics-file-hashes.txt)
and [trusted-semantics-file-hashes.txt](evidence/trusted-semantics-file-hashes.txt).
No required record, trusted mount, or proof artifact was missing or unreadable.
There is no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires
`count_distinct_characters(string: str) -> int` to return the number of
distinct characters after ignoring case. Its examples are `"xyzXYZ" -> 3`
and `"Jerry" -> 4`. The trusted canonical implementation is:

```python
return len(set(string.lower()))
```

The candidate implementation is exactly that expression with the required
signature. Running the trusted `/reference/py2mpy.py` over the copied
`solution.py` exited 0 and produced bytes identical to submitted
`solution.mpy`; both constructor files hash to
`2e97b9f354373f39763938a074e4f09fb6a259868fdc704ed07b670ed65ccfc9`.
See [stage2_fidelity.log](evidence/stage2_fidelity.log).

The independent differential script imports the trusted canonical and candidate
entry points separately. It covers both documented examples, empty and
length-one boundaries, case pairs, whitespace, punctuation, NUL, combining
forms, several Unicode case boundaries, lengths around powers of two, a
4,096-character input, randomized mixed-alphabet strings, and 500 randomized
Unicode strings. All 802 cases matched. The deterministic input-set digest is
`7716e2702a251b13d6e4f459c98d7cd106b0a27df734733ad354031b7edf183b`.
The script and complete inputs/results are
[differential_test.py](evidence/differential_test.py) and
[differential-results.jsonl](evidence/differential-results.jsonl).

Thus the generated Python implementation itself is faithful to the canonical.
The defect found below is in the formal model-to-real-program bridge.

## 3. Clean proof reconstruction

All source needed for execution was copied to
`/tmp/audit-work/reconstruction`. Candidate-built `runtime-kompiled`,
`verification-kompiled`, caches, outputs, and traces were not copied or used.
K v7.1.293 was available.

Fresh commands and results were:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
exit 0

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
exit 0

kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC
#Top
exit 0
```

The bounded logs are
[stage3-build-concrete.log](evidence/stage3-build-concrete.log),
[stage3-build-proof.log](evidence/stage3-build-proof.log), and
[stage3-positive-proof.log](evidence/stage3-positive-proof.log). There is one
positive target claim, so every positive claim was independently rerun.

A reviewer-authored constructor program was concretely executed with the fresh
LLVM definition. Empty, both examples, a case pair, and a punctuation case
produced 0, 3, 4, 1, and 5 respectively, all with exit 0. See
[stage3-concrete-execution.log](evidence/stage3-concrete-execution.log) and the
[final configuration](evidence/stage3-concrete-final-config.txt).

The fresh builds emitted only supplied-source warnings: non-exhaustive
`mapStrVS`, float helpers, `joinCodes`, and `valSeqAt` in the LLVM build and
unused variables in `strLt`. None is on this target's path.

## 4. Adequacy and real-program pinning

### Formal entry claim

The sole entry claim has no `requires` clause. In plain language, for every
finite symbolic `CS:IntSeq`, it starts from a pristine configuration where
scope 0 binds `count_distinct_characters` to a one-parameter closure, calls that
closure on `str(CS)`, and requires the final `<k>` value to be:

```k
isLen(dedupCodes(mapLower(CS)))
```

This is deterministic in `CS`; it is neither a free result, tautology, nor
one-way implication. Empty, `"xyzXYZ"`, and the Unicode witnesses below are
concrete satisfying states. The other cells pin the current environment,
scopes, allocation counters, empty heap and stack, return and exception states,
and exit code.

### Mechanical body and binding pinning

The regenerated module's function name, parameter, and body were compared with
the claim closure. Surface syntax differs only because the claim spells the
empty expression-list unit as `.Exprs`; after K parsing, the two body terms have
identical KORE bytes and the same SHA-256
`a7ffc8036837a24436d57baee9038ed8a663fdb339171e11e59d9e87fbc10090`.
See [constructor-compare.log](evidence/constructor-compare.log) and
[stage4-constructor-kore-compare.log](evidence/stage4-constructor-kore-compare.log).

A fresh auxiliary claim starts from `#loadAll(Module(FuncDef(...)))` using the
regenerated exact constructor body and proves that module loading creates
exactly the closure placed in the entry claim. It printed `#Top` and exited 0.
See [pinning-spec.k](evidence/pinning-spec.k) and
[stage4-pinning-and-witness.log](evidence/stage4-pinning-and-witness.log).
This establishes real constructor/body pinning for the immutable candidate;
there is no substituted program.

### Material source-domain mismatch

Pinning does not make the supplied execution model CPython-faithful. The entry
precondition accepts the following valid Python `str` inputs, but the claimed
model result differs from both trusted and submitted Python:

| Input | Code sequence supplied to the claim | Fresh K result | Canonical Python | Candidate Python |
|---|---|---:|---:|---:|
| `"éÉ"` | `[233, 201]` | 2 | 1 | 1 |
| `"İ"` | `[304]` | 1 | 2 | 2 |

The first is an ordinary one-code-point uppercase-to-lowercase mapping; the
second also exercises Python's one-to-many lowercase mapping. The fresh K
outputs are in
[stage4-unicode-final-config.txt](evidence/stage4-unicode-final-config.txt);
the independent Python results are in
[stage4-python-witnesses.jsonl](evidence/stage4-python-witnesses.jsonl).
These witnesses show that the formal postcondition is not the intended result
of the real generated program on the material HumanEval `str` domain.

## 5. Rule-by-rule static soundness review

The exhaustive inventory covers the trusted top-level semantics file, all 23
helper K files, candidate `verification.k`, and `spec.k`. It contains 1,096
located records, including every syntax/function/total/opaque declaration,
configuration/context, priority/ordinary/concrete/owise rule, import, and
claim. Counts and full normalized text are preserved in
[rule-inventory.md](evidence/rule-inventory.md) and
[rule-inventory.tsv](evidence/rule-inventory.tsv). There are:

- 589 ordinary, 26 `owise`, 45 priority, and 35 concrete rules;
- 38 function, 85 function+total, and 22
  function+total+`no-evaluators` syntax blocks;
- no local `[simplification]` rules and no `[functional]` declarations.

The submitted constructor-to-rule mapping is
[used-construct-map.md](evidence/used-construct-map.md), and the review
classification is detailed in
[stage5-static-review.md](evidence/stage5-static-review.md).

`verification.k` merely imports `MPY`; it contributes no syntax, function,
opaque symbol, equation, priority, simplification, semantic rule, operational
bridge, or auxiliary claim. Accordingly, no task answer was inserted
proof-locally and no program operation was bypassed. The actual selected path
does name lookup, callee/argument evaluation, closure frame creation and
binding, receiver evaluation, lower method dispatch, `set`, `len`, return, and
frame restoration. The relevant recursion decreases, `dedupFrom` guards are
complementary, and the concrete builtin bindings disambiguate dispatch.

The 22 opaque `no-evaluators` symbols are `md5hexCodes`, `intFloatDiv`, `divII`,
`floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, and `sortKeyVS`. None appears in the program, entry claim,
guards, selected execution rules, state cells, or result, so none can affect
this theorem.

The material unsound rule relative to the real Python execution model is
[methods.k](/candidate/reference-semantics/semantics/methods.k:143):

```k
rule lowerC(C:Int) => C [owise]
```

For `C = 201`, this rule leaves `É` unchanged; on the satisfying source input
`"éÉ"` the model therefore deduplicates two codes and concludes 2, while
CPython lower maps both to `é` and the real program returns 1. For `C = 304`,
the rule concludes a one-code string/result 1 while CPython produces two lower
code points/result 2. This is the required concrete false-conclusion witness
on the intended domain. The related literal loader at
[str.k](/candidate/reference-semantics/semantics/str.k:12) is explicitly
ASCII-only, an additional model-coverage boundary.

Rules outside the submitted path are inventoried but are not labeled unsound
without a task-domain false-conclusion witness. That narrower evidence gap does
not mitigate the witnessed result-bearing mismatch on the actual path.

## 6. Fresh non-vacuity test

I did not reuse the candidate mutation. The fresh
`SPEC-FRESH-FALSE.false-constant-zero-result` mutation keeps the exact body and
precondition but changes the result obligation to constant `0`. It is false,
for example, for satisfying `CS = iCons(65, .IntSeq)` (`"A"`), where the real
and modeled result is 1.

The mutation's `kprove --dry-run` exited 0, proving it parsed and built.
The actual proof exited 1 with `WarnStuckClaimState`; the residual reports the
expected failed implication between `0` and
`isLen(dedupFrom(mapLower(CS), .IntSeq))`. This is an unmet result obligation,
not a parser error, timeout, missing import, or unrelated crash. Artifacts:
[spec-fresh-false.k](evidence/spec-fresh-false.k),
[stage6-fresh-nonvacuity.log](evidence/stage6-fresh-nonvacuity.log), and
[mutation residual](evidence/stage6-fresh-mutation-proof.log).

The positive theorem is therefore non-vacuous and result-constraining under its
model.

## 7. Proven versus assumed accounting

### What is machine-checked

Conditional on the copied supplied K definition and K toolchain, the successful
reachability proof establishes partial correctness of the exact constructor
body: for every finite K `IntSeq`, if the modeled call terminates, its returned
K value is `isLen(dedupCodes(mapLower(CS)))`, with the pinned configuration
restored as claimed. The separate pinning theorem checks that module loading
creates the exact closure. The false mutation demonstrates that the result
cannot be freely changed.

It does **not** establish that `mapLower` is CPython `str.lower`, nor that the
K result equals the trusted canonical result for arbitrary Python strings.

### Trust and evidence ledger

| Boundary | Influence | Accounting |
|---|---|---|
| K v7.1.293 compiler, Haskell/LLVM backends, SMT reasoning, and K built-in integer/list/map/string theories | All parsing, execution, and proof closure | Ordinary low-level proof trust boundary; fresh builds and independent negative/positive runs support operation but do not prove the toolchain. |
| Trusted `py2mpy.py` | Source AST to constructor identity | Byte regeneration plus parsed constructor/body equality and the pinning theorem provide strong mechanical evidence for this program. |
| Supplied MPY lookup, call, frame, method, set, and length semantics | Control, state, and final result | Fixed and executed rather than bypassed. Structurally adequate for the selected term. |
| Supplied `lowerC/mapLower` as a model of Python lowercasing | Final result and human-facing theorem meaning | **Illegitimate for the full source contract:** the two executable Unicode witnesses falsify the bridge. |
| Twenty-two opaque fixed-semantics symbols listed above | Potential values in unrelated constructs | Acceptable here because none is reachable from or mentioned by this proof; no target result or control dependence. |
| Python differential testing | Candidate-versus-canonical implementation bridge on 802 inputs | Finite empirical support only, not a universal theorem. Zero mismatches show the implementation is not the source of the witnessed K divergence. |
| Concrete K tests and Unicode witnesses | Ground behavior of the fresh model | Finite evidence; decisive as counterexamples to universal real-program adequacy, but not a replacement for the positive K proof. |
| Termination | Whether calls finish | No separate total-correctness/liveness theorem; the candidate appropriately claims only partial correctness. |

There is no proof-local primitive, abstraction, summary oracle, empirical
rewrite, or informal body substitution. The proof's narrow formal statement is
honest under MPY, but the candidate's use of it as a proof of the HumanEval
program is not. Because a used semantics rule enables false return conclusions
for valid, satisfying source-contract inputs, this is a material adequacy and
language-semantics failure. It cannot be downgraded to a non-fatal trust
limitation.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
