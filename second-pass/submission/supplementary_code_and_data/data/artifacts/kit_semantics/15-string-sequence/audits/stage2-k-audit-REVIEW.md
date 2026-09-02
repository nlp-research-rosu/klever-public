# Independent adversarial review: 15-string-sequence

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. I did not reuse either candidate
compiled definition. The proof was reconstructed from copied source in
`/tmp/audit-work/15-string-sequence`, the actual program term was compared at
constructor level, every candidate proof extension was reviewed, and a fresh
false result obligation was rejected for the expected reason.

## 1. Input and provenance integrity

The launcher record declares `record_layout = pipeline-v3`,
`condition = kit-semantics`, and `semantics_mode = SUPPLIED_SEMANTICS`.
`/reference/reference-semantics` is present, as required for that mode. There is
no rendered-mode contradiction and hence no audit infrastructure breach.

I read and checked all required pipeline-v3 records:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  and `/generation-result.json`;
- `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt` below
  `/generation-evidence`;
- the complete structured trace below
  `/generation-evidence/codex-trace`.

The campaign-lock JSON is structurally identical to the campaign block in
`audit-input.json`. Its independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
which equals the launcher-recorded hash. All independently computed hashes for
the mounted run/task/result records, invocation records, prompt, output log,
metrics, usage, trusted prompt, canonical implementation, translator, and
candidate copies of the prompt and translator equal their recorded values.

The generation trace consists of one 346-line JSONL file. Every line parses.
Its per-file hash is
`8b4f3e8e2347df9e940b835bfdd8990c7375fe2fa322ec3b54a10b47e8719778`,
matching `generation-result.json`. The 27,098-line generation output was read
in full by the integrity script. Those records report a successful generation,
but I used that only to inventory the untrusted construction history.

The candidate and trusted supplied-semantics trees each have the same 25
non-root entries. Recursive type, path, and content comparison is exact, and
neither tree contains a symlink. There are no missing, additional, mistyped, or
changed candidate semantics entries. Candidate `prompt.py` and `py2mpy.py` are
byte-identical to the trusted mounts. The six required proof deliverables are
ordinary nonempty files, and the candidate tree has no symlinks. Candidate
`runtime-kompiled`, `verification-kompiled`, logs, prose, and cached Python
objects were ignored as proof evidence.

Reproducible details, all computed from mounted container paths, are in:

- `evidence/stage1_integrity.py`
- `evidence/stage1-integrity.log` (command exit 0)
- `evidence/stage1-mounted-file-hashes.log` (complete 810-file mounted
  candidate/reference/generation manifest; exit 0)

Stage 1: **PASS**.

## 2. Program fidelity and canonical comparison

The trusted prompt requires:

> For an integer `n`, return one string containing the decimal numbers from
> `0` through `n`, inclusive, separated by one space.

The documented examples are `n=0 -> "0"` and
`n=5 -> "0 1 2 3 4 5"`. The trusted canonical implementation is
`" ".join(str(x) for x in range(n + 1))`. Thus its behavior on negative
integers is also well-defined: the range is empty and the result is `""`.

The candidate implementation uses:

1. an early `""` return when `n < 0`;
2. `result = "0"` and `i = 1`;
3. a loop appending `" " + str(i)` while `i <= n`.

This is a different but equivalent algorithm over the annotated integer
domain. It covers both branches and does not impose a finite bound.

I regenerated the translation in scratch with the trusted
`/reference/py2mpy.py`. The regenerated and submitted files are byte-identical:

```text
98fadde9bde7e3cb3cdbb845a3df01338e23695d020e174654121a6bb12afcec  solution.mpy
98fadde9bde7e3cb3cdbb845a3df01338e23695d020e174654121a6bb12afcec  solution-regenerated.mpy
translator_exit=0
cmp_exit=0
```

The independent differential test imports the trusted canonical entry point
and candidate entry point by absolute mounted paths. It covers the examples,
negative empty-range cases, the `-1/0` if boundary, zero/one/multiple loop
iterations, the `9/10` and `99/100` decimal-width boundaries, every integer
from -100 through 300, and 500 seeded values from -5000 through 5000. There
were 873 unique inputs, zero exceptions, and zero mismatches.

Evidence:

- `evidence/stage2-translation.log` (exit 0)
- `evidence/stage2_differential.py`
- `evidence/stage2-differential.log` (exit 0)

Stage 2: **PASS**.

## 3. Clean proof reconstruction

Only source artifacts were copied to scratch. The supplied semantics was copied
from `/reference`, not from a candidate compiled tree. Fresh output directories
were named `reviewer-runtime-kompiled` and
`reviewer-verification-kompiled`. The installed tools independently report K
7.1.293, matching the campaign.

### Concrete definition and execution

The exact function source is the byte-identical prefix of the reviewer-authored
concrete test. Trusted translation succeeded. The fresh LLVM command was:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled
```

It exited 0. The concrete MPY program asserts results for `-2`, `-1`, `0`, `1`,
`5`, and `10`. This command exited 0:

```bash
krun concrete-test.mpy --definition reviewer-runtime-kompiled
```

The final configuration has `.K`, environment 0, empty heap and stack,
`noRet`, `NoExc`, and exit code 0. The LLVM compiler emitted supplied-semantics
coverage warnings for unrelated total functions; none is used by this program.

Evidence:

- `evidence/stage3_concrete.py`
- `evidence/stage3-concrete-translation.log`
- `evidence/stage3-kompile-llvm.log`
- `evidence/stage3-krun.log`

### Proof definition and positive claims

The fresh Haskell command was:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled
```

It exited 0. Positive proof reconstruction produced:

| Command scope | Output | Exit |
|---|---:|---:|
| `--claims SPEC.loop-invariant` | `#Top` | 0 |
| `--claims SPEC.loop-invariant,SPEC.string-sequence` | `#Top` | 0 |
| all claims in `SPEC` | `#Top` | 0 |

The entry claim legitimately depends on the separately checked loop claim as a
reachability circularity. As a dependency diagnostic, I also selected only
`SPEC.string-sequence` while deliberately excluding its helper. That command
exited 1 and became stuck after the first iteration because the circularity was
not loaded. This is not an unclosed positive target: the explicit entry-proof
command selects both the entry and its only helper, and simultaneously checks
the helper. The helper also closes alone. The diagnostic makes the dependency
visible rather than silently assuming it.

Evidence:

- `evidence/stage3-kompile-haskell.log`
- `evidence/stage3-kprove-loop.log`
- `evidence/stage3-kprove-entry-with-helper.log`
- `evidence/stage3-kprove-all.log`
- `evidence/stage3-kprove-entry.log` (intentional helper-exclusion diagnostic)

Stage 3: **PASS**.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.loop-invariant` assumes:

- the recurring computation is the submitted loop's real `#while` term;
- local `n = N`, `i = I`, and `result = str(ACC)`;
- `I >= 1` and `N >= 0`;
- the exact submitted closure and its scope chain are installed.

It concludes that the loop is consumed, `result` becomes
`str(sequenceAcc(ACC,I,N))`, and `i` has some final integer value. The
existential final `i` is harmless because it is local and the function frame is
discarded immediately after return. All unrelated cells and the continuation
are framed.

`SPEC.string-sequence` has no `requires` clause, so its formal domain is every
K integer. It starts in the MPY initial state, loads the submitted module, calls
the installed `string_sequence` binding with `N`, and concludes that the return
value is `str(stringSequenceCodes(N))`. It also constrains normal cleanup:
environment 0, scope location 1, empty heap/stack, heap location 0, `noRet`,
`NoExc`, and exit code 0.

The postcondition is result-bearing and two-sided: it fixes the returned `str`;
it is not a free variable, tautology, or implication. `stringSequenceCodes` is
fixed by disjoint exhaustive equations:

- `N < 0`: empty code sequence;
- `N >= 0`: code 48 (`"0"`) followed by the exact accumulator fold from 1
  through `N`.

### Mechanical source-to-claim identity

The entry claim manually embeds a `Module` term, so I mechanically extracted
the exact argument under `#loadAll`. Both the submitted `solution.mpy` and the
extracted claim term were parsed with the fresh definition, using K's own macro
expansion. The submitted program KAST equals the extracted rule-LHS KAST
structurally:

```text
constructor_terms_equal=True
extract_exit=0
solution_kast_exit=0
claim_rule_kast_exit=0
constructor_compare_exit=0
```

This demonstrates that explicit `.Exprs`/`.Stmts` units in the claim and their
surface omission in translator output are semantically inert list
normalization. The theorem executes the submitted function binding and body.
The absence of an automatic source-to-spec generator is only a maintenance
observation for this immutable artifact, not an identity gap.

Evidence:

- `evidence/stage4_extract_claim_program.py`
- `evidence/stage4_compare_kast.py`
- `evidence/stage4-program-pinning-rule.log`

### Satisfying states and concrete substitution

The loop precondition is satisfiable with `ACC = "0"`, `I = 1`, and `N = 5`.
The entry precondition is satisfiable with `N = 5` (indeed, with every K
integer). I generated independent ground specializations of both claims at
that state, replacing the summaries in the destinations with the literal
character codes for `"0 1 2 3 4 5"`. The loop ground claim and the entry ground
claim each printed `#Top` and exited 0 when selected alone. Both Python
implementations return the same literal.

A first parallel entry-witness invocation failed before parsing with a
transient Java-version detection message. The exact same command, rerun alone,
printed `#Top` and exited 0; this was reviewer tooling noise, not candidate
evidence.

Evidence:

- `evidence/stage4_make_ground_witnesses.py`
- `evidence/stage4-ground-generate.log`
- `evidence/stage4-ground-loop.log`
- `evidence/stage4-ground-entry-rerun.log`

### Body sensitivity

I independently changed every actually executed separator literal in the
ground entry claim and pinned closure from space to comma, while retaining the
original result obligation. The external `solution.py` was not the mutation
target; the invoked K closure body itself changed. The proof exited 1 with
`WarnStuckClaimState`, and the residual return is the ASCII sequence
`48,44,49,44,50,44,51,44,52,44,53`, namely `"0,1,2,3,4,5"`. Thus changing
the material program body changes the executed result and invalidates the
original theorem.

Evidence:

- `evidence/stage4_make_body_mutation.py`
- `evidence/stage4-body-sensitivity.log`

Stage 4: **PASS**.

## 5. Rule-by-rule static soundness review

The reviewer-generated exhaustive inventory is:

- 938 total source items;
- 701 rules, 229 syntax declarations, five contexts, one configuration, and
  two claims;
- 928 fixed supplied-semantics items, eight candidate proof-extension items,
  and two candidate claims;
- 147 function declarations, 109 total declarations, zero `functional`
  declarations, 25 named `symbol(...)` declarations, 22
  `[no-evaluators]` declarations, 45 priority rules, 37 concrete rules, and
  four simplification rules.

`evidence/stage5-rule-inventory.log` records exact normalized text, file, line,
kind, attributes, and source class for every item. Per-file counts and the
complete used-rule map are in `evidence/stage5-static-review.md`.

### Submitted-program coverage

Every constructor used by `solution.mpy` maps to fixed declarations and rules:

- module loading and statement sequencing;
- exact closure creation, callee/argument evaluation, parameter binding,
  frames, return, and pop;
- lexical lookup through local/module/builtin scopes;
- integer/string literals and the discarded docstring expression;
- strict assignment, `if`, comparisons, and recurring `#while` control;
- left-to-right binary operations, string concatenation, and integer addition;
- ordinary lookup/call of builtin type `str`, with fixed `Int2String` and
  `strToCodes`;
- all configuration cells changed or preserved by call and return.

The fixed priority rules for closure cells and heap references are
inapplicable: this unannotated function creates neither. The generic `[owise]`
call route therefore handles `str(i)`. No candidate rule intercepts a `Call`,
program AST, continuation, return, frame, or state cell. The supplied ASCII
string model is adequate because every literal and every output character is
ASCII. K and Python integer values are unbounded on this domain.

The 25 supplied named symbols are:

`absF`, `addF`, `ceilF`, `decStrToF`, `divF`, `divFloatIntV`, `divII`, `eqF`,
`floatLt`, `floatMod`, `floorFI`, `gtF`, `intFloatDiv`, `intToF`,
`md5hexCodes`, `mulF`, `powF`, `roundF`, `roundFN`, `sortKeyVS`, `sortVS`,
`sqrtF`, `subF`, `toF`, and `truncF`.

None is reachable from this program or either claim. Likewise, unused
fixed-semantics rules for containers, iteration, comprehensions, slices,
methods, sort, float, MD5, assertions, and imports cannot contribute to claim
closure. They remain part of the selected trusted semantics but are not hidden
task-specific proof assumptions.

### Candidate rules

The candidate contributes only two mathematical functions and six rules:

1. `sequenceAcc(IntSeq,Int,Int) [function,total]`.
2. Base definition `sequenceAcc(ACC,I,N) = ACC` under `I > N`.
3. Step definition under `I <= N`: append space and the fixed decimal rendering
   of `I`, increment `I`, and recurse.
4. A symbolic duplicate of the base equation with the same RHS.
5. A symbolic fold that is exactly the reverse of the guarded step equation.
6. `stringSequenceCodes(Int) [function,total]`.
7. Its negative-input empty result under `N < 0`.
8. Its nonnegative initial/fold result under `N >= 0`.

The guard pairs are disjoint and exhaustive. Concrete accumulator recursion
decreases the natural measure `N-I+1` while it is positive. The duplicate base
agrees on overlap. The fold is a true equality on its complete guard; at the
`I=N` overlap with the base, both paths yield the same updated accumulator.
`[total]` supplies definedness, not an arbitrary value. These rules change no
operational cell and do not bypass execution.

The loop claim is a standard guarded circularity over the real recurring loop
head. At least one fixed semantic iteration occurs before it can recur. It
reads `n`, `i`, and `result`, writes only `i` and `result`, and has no exception,
heap, output, allocation, break, continue, return, or cleanup effect. Framing
its continuation and unrelated cells is therefore sound.

I found no materially unsound rule, so there is no unsoundness allegation
requiring a false-conclusion witness. In particular, there is no operational
bridge, unconstrained oracle, task-answer rewrite, fabricated result, false
totalization equation, or overlap with disagreeing right-hand sides.

Stage 5: **PASS**.

## 6. Fresh non-vacuity test

I did not reuse the candidate's `spec-vacuity.k`. The fresh mutation keeps the
actual entry program and satisfying input `N=5` unchanged, but changes the
destination literal from:

```text
0 1 2 3 4 5
```

to the demonstrably false:

```text
0 1 2 3 4 6
```

The generated mutation is preserved as
`evidence/stage6-false-result.k`. The exact proof command was:

```bash
kprove stage6-false-result.k \
  --definition reviewer-verification-kompiled \
  --spec-module STAGE6-FALSE \
  --claims STAGE6-FALSE.false-entry-result-n5
```

The spec parsed and executed normally, then exited 1 with
`WarnStuckClaimState`. Its residual final value is the actual sequence ending
in code 53 (`'5'`), which cannot unify with the false destination ending in
code 54 (`'6'`). This is the expected unmet result obligation, not a parser
error, timeout, missing import, unreachable mutation, or unrelated crash. Both
Python implementations also establish that `N=5` satisfies the original
precondition and returns the actual result.

Evidence:

- `evidence/stage6_make_false_result.py`
- `evidence/stage6-false-result.k`
- `evidence/stage6-false-result.log` (`kprove_exit=1`; probe driver exit 0)

Stage 6: **PASS**.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

For every mathematical K integer `N`, under the supplied MPY semantics, if the
freshly initialized execution that loads the constructor-identical submitted
module and calls `string_sequence(N)` terminates, then it returns:

- `""` when `N < 0`;
- otherwise the ASCII decimal renderings of `0,1,...,N`, in order, with exactly
  one space between adjacent numbers.

It also terminates that call normally with the environment, scope allocator,
heap, heap allocator, stack, return state, exception state, and exit code fixed
as stated in the entry claim. This is partial correctness; termination and
resource bounds are not proved.

### Trust ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| Supplied `reference-semantics/` | Both claims and all concrete/proof execution | Trusted input selected by the benchmark. Integrity is exact. The complete used path was statically checked; unused language features do not affect closure. |
| K standard integer, Boolean, string, map/list hooks, especially `Int2String`, `substrString`, and `ordChar` | Decimal conversion and string-code construction | Low-level fixed primitives outside the program theorem. They implement ordinary mathematical integer/string operations. The theorem is conditional on this standard K runtime behavior. |
| Trusted `py2mpy.py` | Source-to-constructor bridge | Byte regeneration and constructor-level KAST comparison establish that the immutable submitted translation is exactly the term executed by the claim. |
| `sequenceAcc` and `stringSequenceCodes` | Loop and entry postconditions | Not opaque or assumed: exhaustive truthful equations plus the machine-checked loop/entry reachability claims connect them to real execution. |
| The 25 supplied named opaque/symbolic primitives listed in Stage 5 | None for this task | Explicitly outside the reachable slice. They have no dependent branch, result, state, exception, or postcondition here. |
| K 7.1.293 compiler, Haskell prover/backend, LLVM concrete backend, SMT solver, and host runtime | Machine-checking result | Conventional trusted computing base. Fresh builds reduce cache/provenance risk but do not prove the toolchain itself. |
| English interpretation of the recursive code sequence as “0 through N separated by spaces” | Human-facing contract bridge | Ordinary mathematical reading of exhaustive equations: start with code 48, append code 32 and fixed decimal `I`, then increment through `N`. It is also supported, not replaced, by concrete and differential evidence. |
| Trusted canonical Python and CPython execution | Differential evidence only | 873 finite tests support implementation-to-contract fidelity. They are not used as a universal K proof. |
| Reviewer concrete K witnesses and negative mutations | Adequacy, body sensitivity, non-vacuity | Finite validation evidence only; it does not substitute for the successful symbolic reachability proof. |

Gate A (real-program soundness): **PASS**. The actual program executes under
fixed semantics, candidate equations are sound, the result is constrained, the
body is sensitive, and the fresh false result is rejected.

Gate B (intent adequacy): **PASS**. The theorem covers the full annotated
integer domain without finite-size restriction and states the material source
contract. Negative integers are an additional canonical-compatible behavior,
not a narrowing.

Gate C (trust and auditability): **PASS**. All proof-local and fixed primitive
boundaries are explicit, claimed evidence is independently reproduced, and
finite evidence is not presented as universal proof.

The candidate is therefore a sound, result-constraining proof of the real
generated program, with no material adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
