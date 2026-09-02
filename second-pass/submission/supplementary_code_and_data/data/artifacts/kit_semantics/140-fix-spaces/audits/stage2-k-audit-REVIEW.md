# Independent adversarial audit: 140-fix-spaces

This audit used the required `using-kit` and `validating-proof` procedures. I
treated every candidate report, prior trace, compiled definition, and `#Top` as
an untrusted claim. All executable artifacts were copied to
`/tmp/audit-work`, and all definitions used below were rebuilt from source.
The exact command record is [evidence/COMMANDS.md](evidence/COMMANDS.md).

The proof is legitimate under the supplied MPY semantics and covers every
string in the prompt's domain. The concern is an incompatibility between two
trusted task inputs: the prompt says a two-space run becomes two underscores,
while `canonical.py` emits only one underscore when that run is the final run.
The candidate follows the prompt, not that canonical edge behavior. In
addition, the final bridge from the recursive K summary `fixedSpaces` to the
natural-language run specification is an audited mathematical argument with
finite differential support, not a separate K theorem.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, condition `kit-semantics`, and problem
`140-fix-spaces`. The trusted `/reference/reference-semantics` mount is present,
so the rendered mode and mounts agree. There is no infrastructure breach.

I read and checked all required pipeline-v3 records:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the complete structured trace, one JSONL file containing 273 valid records.

The audit campaign block exactly equals `/audit-campaign-lock.json`; its
SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the recorded value. Every recorded regular-file hash checked by
[the independent checker](evidence/integrity_check.py) matched. The
launcher-compatible whole-tree hashes also matched:

- candidate tree:
  `fdc05e9172174bb7981c928757711a135c95132c133e48d01871aaedced7fd86`;
- each supplied-semantics tree:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- structured trace tree:
  `6b149a1ca846aa4cddbd69ad59b88fb790caaa35a7783294edbe91e8a6b045ea`.

An additional independent path/type/mode/content digest was identical for the
trusted and candidate semantics trees
(`b93aaeb11647105c20cf2b3dac7b6512413f6b4de9453f932acc10db5656c807`).
Recursive entry comparison found the same 25 entries, all regular
files/directories, with no missing, additional, changed, mistyped, or symlinked
entry. Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
mounts. The detailed hashes and all 24 semantics file hashes are in
[01-integrity-v4.log](evidence/01-integrity-v4.log); the structured-trace
inspection is in [01-trace-summary.log](evidence/01-trace-summary.log).

The required proof sources (`solution.py`, `solution.mpy`, `verification.k`,
`spec.k`, `prove.sh`, and `PROOF.md`) are regular files. Candidate-provided
compiled directories and caches were not copied or used.

Stage result: PASS.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For every input string, preserve all non-space characters in order. Replace a
maximal run of one or two U+0020 spaces by the same number of underscores.
Replace a maximal run of at least three U+0020 spaces by one hyphen. This
includes leading and trailing runs; empty input returns empty output. This is
the direct reading of [prompt.py](/reference/prompt.py:2).

[solution.py](/candidate/solution.py:1) maintains:

- `result`: output through the last completed non-space character;
- `spaces`: `""`, `"_"`, `"__"`, or the saturated marker `"-"` for the
  pending space run.

A space advances/saturates `spaces`; a non-space flushes it with the character;
the return flushes a trailing run. This covers all branches and has no input
size bound.

### Translation identity

The trusted translator regenerated `solution.mpy` with exit 0. Regenerated and
submitted files are byte-identical, both SHA-256
`1bc0cbde9674e4357b29b5a38b64910e147af495f58944d6c1533afd7c488e44`;
see [02-translation.log](evidence/02-translation.log).

### Independent differential

[differential_test.py](evidence/differential_test.py) independently imports
the trusted canonical and generated entry points. Its direct contract oracle
is `re.sub(r" {3,}", "-", text).replace(" ", "_")`, which does not reuse the
candidate's state machine or K equations. The preserved corpus
[02-differential-inputs.jsonl](evidence/02-differential-inputs.jsonl) has
SHA-256
`e9c7038563ad36362131a4398b87fd93a3d265911d943999fb42d47882b900c9`
and contains 10,366 distinct inputs:

- all four documented examples;
- empty, Unicode, control-character, and explicit run-length boundaries;
- run lengths 0 through 6 in prefix, suffix, interior, only-run, and two-run
  positions;
- all strings of length 0 through 6 over `{space, a, tab, é}`;
- 5,000 deterministic generated strings of length 0 through 80 over 13 code
  points.

Results:

| Comparison | Mismatches |
|---|---:|
| generated vs direct prompt contract | 0 |
| generated vs trusted canonical | 285 |
| trusted canonical vs direct prompt contract | 285 |

Every mismatch is the same material boundary: a final maximal run of exactly
two spaces. For example, input `"  "` gives generated/contract `"__"` but
canonical `"_"`. The cause is [canonical.py](/reference/canonical.py:32):
its final `elif end - start > 0` appends one underscore for both one and two
spaces. The full result and exit 1 used to surface, not suppress, this
disagreement are in [02-differential.log](evidence/02-differential.log).

Judgment: the candidate implements the unambiguous natural-language contract
and documented transformation, while the trusted canonical has a conflicting
trailing-two-space edge behavior. This is not a candidate domain restriction
or program bug relative to the prompt, but it prevents an unqualified PASS
against all trusted evidence.

Stage result: PASS for program/translation fidelity to the prompt, with the
canonical discrepancy carried as a final concern.

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/candidate-src`. Neither
`runtime-kompiled` nor `verification-kompiled` from `/candidate` was reused.
The installed `kompile` and `kprove` both report K v7.1.293.

Fresh Haskell build:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
Exit 0
```

The focused loop claim then printed `#Top` and exited 0
([03-kprove-loop-invariant.log](evidence/03-kprove-loop-invariant.log)).
The complete `SPEC` module, which supplies the loop circularity while proving
both the loop claim and target, also printed `#Top` and exited 0
([03-kprove-all-claims.log](evidence/03-kprove-all-claims.log)). Selecting the
target alone would remove its required loop claim from the proof set; the
complete-module invocation is therefore the independent target-proof command.

I also rebuilt the LLVM definition from the same source with `MPY-KRUN`.
Eleven auditor-authored normal/boundary assertions translated successfully and
executed to `.K`, `NoExc`, exit code 0; see
[concrete_cases.py](evidence/concrete_cases.py),
[03-kompile-llvm.log](evidence/03-kompile-llvm.log), and
[03-krun-concrete-v2.log](evidence/03-krun-concrete-v2.log). LLVM warnings
identified incomplete total declarations in unrelated imported collection and
float helpers; none is on this program's path.

Stage result: PASS.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.loop-invariant` starts at the exact internal string-loop head with:

- arbitrary remaining codes `CS`, accumulated result `R`, pending sequence
  `P`, prior loop target `CH`, text `T`, active location `L`, and parent;
- the exact four-binding active local scope;
- an arbitrary continuation and automatically framed untouched cells.

It consumes the loop and changes the three written locals to
`resultAfter(CS,R,P)`, `pendingAfter(CS,P)`, and `charAfter(CS,CH)`, while
preserving text, environment, parent, outer scopes, continuation, heap,
allocation counters, stack, return state, exception state, and exit code.

`SPEC.target` has no value-domain `requires`; its precondition is the exact
reachable initial module/call configuration. For every `CS:IntSeq`, it looks up
the exact one-parameter `fix_spaces` closure, executes the call, and returns
exactly:

```text
str(fixedSpaces(CS))
```

where `fixedSpaces` concatenates the exact final completed and pending
sequences. The postcondition is an equality to a determined recursive function,
not a free variable, implication, or unconstrained oracle.

### Real-program identity

Four independent checks pin the submitted program:

1. trusted regeneration is byte-identical to submitted `solution.mpy`;
2. LLVM execution of that regenerated module reaches the exact closure binding
   and state used by `SPEC.target`
   ([04-krun-module-load.log](evidence/04-krun-module-load.log));
3. two auditor-authored constructor claims expand `#fixSpacesLoopBody` and
   `#fixSpacesBody` to the complete trusted-regenerated AST and close with
   `#Top` ([pinning-compare.k](evidence/pinning-compare.k),
   [04-kprove-pinning-compare-v2.log](evidence/04-kprove-pinning-compare-v2.log));
4. a material body mutation changes the body installed in the claim, reaches
   `"X"` for empty input, and fails the original empty result
   ([06-kprove-body-sensitivity.log](evidence/06-kprove-body-sensitivity.log)).

The aliases only expand syntax. Fixed rules still perform module binding,
lookup, callee/argument evaluation, frame creation, parameter binding,
assignments, string iteration, comparisons, branches, concatenations, loop
control, return, and frame cleanup.

### Satisfiability and concrete substitution

The module-load execution exhibits an actual state satisfying the target
precondition. Five ground instances of that exact state all close with `#Top`
([ground-witness.k](evidence/ground-witness.k),
[04-kprove-ground-witnesses.log](evidence/04-kprove-ground-witnesses.log)):

| Input | Claimed/K result | Generated Python | Canonical Python |
|---|---|---|---|
| `""` | `""` | `""` | `""` |
| `" "` | `"_"` | `"_"` | `"_"` |
| `"  "` | `"__"` | `"__"` | `"_"` |
| `"   "` | `"-"` | `"-"` | `"-"` |
| `"a  b"` | `"a__b"` | `"a__b"` | `"a__b"` |

The formal domain is every K `IntSeq`, which is broader than valid Unicode code
sequences and therefore does not narrow the prompt's all-string domain.
Program literals are ASCII, and symbolic inputs arrive directly as `str(CS)`,
so the semantics' ASCII-only concrete literal conversion does not restrict the
theorem.

Stage result: PASS.

## 5. Rule-by-rule static soundness review

The exhaustive machine-generated inventory is
[04-rule-inventory.tsv](evidence/04-rule-inventory.tsv), produced by
[k_rule_inventory.py](evidence/k_rule_inventory.py). It covers all 24 supplied
K source files plus `verification.k` and `spec.k`: 26 files and 1,122
declarations. It enumerates every syntax/configuration/context/module/import,
all 709 rules, and both claims. Rule/declaration categories are:

- 605 ordinary rules, 26 `owise` rules, 41 priority rules, 35 concrete rules,
  and 2 simplification rules;
- 152 function-bearing syntax declarations, 114 of them marked `total`;
- 25 symbolic/opaque declarations (22 explicitly `no-evaluators` and three
  symbolic declarations with only concrete equations);
- 5 source contexts and no `[functional]` declaration.

The complete material constructor/rule map, per-file disposition, and
proof-local equation checks are in
[04-used-construct-map.md](evidence/04-used-construct-map.md). The material
findings are:

- Configuration and calls: the exact module scope selects the submitted
  binding; callee evaluation precedes the one argument; a fresh local frame is
  made and later removed; pinned heap, stack, return, exception, and exit cells
  are restored.
- Evaluation order: generated `strict`/`seqstrict` contexts evaluate `Str`,
  `Name`, comparison operands, binary operands, RHS expressions, loop iterable,
  conditions, and return expression in the required order. The simple-name
  augmented assignments evaluate their RHS before the rule's scope read; in
  this body those RHS expressions cannot mutate the assigned binding, so this
  supplied-semantics choice agrees with the real program.
- Loop control: string `#iterNext` consumes exactly one `iCons`; `#bindTgt`
  writes `char`; the body completes before `#loopLbl` resumes. There is no
  return, break, continue, exception, output, allocation, or heap effect inside
  the loop, so the invariant's arbitrary continuation is preserved.
- Priorities: no proof-local priority rule exists. Imported ref/cell/list,
  special-call, and concrete priority rules are excluded by the exact
  string-valued, cell-free path. `MPY-CONCRETE` is not imported into the
  Haskell proof definition.

`verification.k` has exactly 14 equations:

- two unconditional, total AST expansions that match the full generated body;
- three exhaustive, pairwise-disjoint `pendingSpace` cases;
- empty/space/non-space exhaustive cases for each of `resultAfter` and
  `pendingAfter`, with recursion strictly decreasing `CS`;
- two exhaustive, decreasing `charAfter` cases;
- one unconditional `fixedSpaces` equation.

The non-space `resultAfter` equation uses `R + (P + char)`, exactly the
translated evaluation tree. The two `[simplification]` attributes are on these
truthful defining equations; they introduce no extra proposition. There is no
proof-local opaque symbol, trusted primitive, call interception, priority
shortcut, fabricated result, or operation-skipping bridge.

The loop claim is the bridge-free universal connection theorem for the pure
summaries: it symbolically executes one actual loop iteration over the complete
claim domain and uses the same claim only at the shorter remaining loop head.
Its complete accepted continuation and state footprint are also present in its
justification domain.

The 25 imported opaque/symbolic operations are:
`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, and `sortKeyVS`. No submitted constructor can invoke any of
them, and no positive claim or postcondition contains one. Other documented
fixed-semantics limitations (imports, heap collections, float behavior,
returned closures, and out-of-bounds/error cases) are likewise
constructor/guard-disjoint from this exact program. They are trust-boundary
limitations, not false conclusions enabled on the intended input domain. I
found no material unsound rule; consequently there is no unsoundness allegation
requiring a false-conclusion witness.

Stage result: PASS.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh
[audit-false-mutation.k](evidence/audit-false-mutation.k) uses the exact
satisfying target state and input `"  "`, but changes only the required return
from the true `"__"` to false `"_"`.

K parsed and executed the mutation. It reached:

```text
str(iCons(95, iCons(95, .IntSeq)))
```

then emitted `WarnStuckClaimState` and exited 1 because that term does not unify
with the demanded one-underscore destination. This is the expected unmet
result obligation, not a parser error, missing import, timeout, or unrelated
crash; see
[06-kprove-false-mutation.log](evidence/06-kprove-false-mutation.log).

The separate fresh body-sensitivity mutation changed the installed
initialization to `result = "X"`. It reached `"X"` for empty input and exited 1
against the original empty result, independently confirming that the theorem
depends on the body actually placed in the claim.

Stage result: PASS.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied MPY semantics and exact target configuration, for every
`CS:IntSeq`, execution of the submitted `fix_spaces` function reaches
`str(fixedSpaces(CS))` and restores the stated caller/module state. The loop
claim formally establishes the exact final `result`, `spaces`, and `char`
locals through actual fixed-semantics execution. This is a partial-correctness
reachability result; it is not a proof of the K implementation, translator, or
CPython.

### Trust and evidence ledger

| Boundary | Influence | Dependents | Assessment/evidence |
|---|---|---|---|
| Supplied MPY semantics | All material value, control, binding, and state transitions | Both claims | Acceptable fixed trust boundary for this condition. Exact tree integrity, exhaustive material-rule audit, clean Haskell proof, and clean LLVM executions support it. |
| K v7.1.293 frontend/Haskell/LLVM backends | Parsing, compilation, rewriting, proof result | All machine-checked evidence | Necessary infrastructure trust. Independent positive, ground, constructor-pinning, and negative runs discriminate success from failure. |
| Trusted `py2mpy.py` and CPython AST parsing | Python-to-constructor identity | Program pinning | Outside the K theorem. Byte-identical regeneration plus constructor-level K checks support the bridge. |
| Python string to `str(IntSeq)` representation; U+0020 as code 32 | Meaning of iteration, space test, and concatenation | Source-language adequacy | Informal model bridge, strongly supported by the operation-level audit and Unicode/control/random differential tests. |
| Meaning of `fixedSpaces` as maximal-run normalization | Human-facing postcondition | Final contract conclusion | The helper equations and invariant give a direct structural argument; 10,366 prompt-oracle cases provide finite support. There is no second, independent K theorem stating regex/maximal-run equivalence. This is a non-fatal validation limitation. |
| Imported opaque symbols and unused approximations listed in Stage 5 | None on the submitted path | No claim/result dependent | Inert here. Their presence broadens the definition's global trust boundary but cannot affect this theorem. |
| Trusted `canonical.py` | Independent expected-output evidence | Adequacy judgment | Conflicts with the prompt only for trailing runs of exactly two spaces. The candidate and K theorem follow the prompt. This unresolved trusted-input inconsistency is the principal concern. |

Gate A (real-program soundness): PASS. The proof is body-sensitive,
result-constraining, bridge-free, and pins the regenerated body.

Gate B (intent adequacy): PASS relative to the natural-language source
contract over all strings; no size bound or finite-domain restriction exists.
The incompatible canonical edge behavior remains explicitly unresolved.

Gate C (trust/evidence auditability): PASS. Reviewer sources, full input
corpus, exact commands, bounded logs, positive outputs, and expected negative
residuals are preserved under `/audit-output/evidence`.

The canonical conflict and informal summary-to-prose bridge are non-fatal
limitations of an otherwise sound, full-domain proof. They warrant
`CONCERNS / LEGIT`, not `FAIL / NOT_LEGIT`: the candidate does not narrow the
HumanEval contract, substitute another program, bypass execution, or use an
unsound result-bearing rule.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
