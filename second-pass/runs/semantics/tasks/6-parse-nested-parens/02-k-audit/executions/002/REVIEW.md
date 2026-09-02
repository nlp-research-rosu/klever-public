# Independent adversarial audit: 6-parse-nested-parens

The reconstructed K proof is sound, non-vacuous, and mechanically pinned to the
submitted generated function. It is nevertheless not a legitimate proof of the
full HumanEval contract. The proved postcondition follows the submitted
character-by-character implementation, which invents zero-depth groups for an
empty string and for empty fields created by repeated, leading, or trailing
spaces. The trusted canonical omits empty fields. These inputs satisfy the K
entry precondition, and the prompt does not restrict separators to exactly one
space or require a nonempty input. This is a material result mismatch, not a
mere test-coverage limitation.

## 1. Input and provenance integrity

The launcher record declares:

- `record_layout`: `legacy-selected-stage1`
- `semantics_mode`: `SUPPLIED_SEMANTICS`
- problem/config: `6-parse-nested-parens`,
  `codex-gpt-5.6-sol-xhigh-semantics`

All records required for that legacy-selected layout were present, regular,
readable files: `/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the structured JSONL trace. The optional
`usage.json` was also present and checked. The absent modern
`runtime-metrics.json` is not required for this declared historical layout.

I read the manifests, result, prompt, generation log/last message, and
structured trace. They claim a successful generation and `#Top`, but I used
none as proof evidence. The trace shows that the generator manually introduced
the proof terms and eventually ran both claims together; that history was
treated only as an untrusted claim to reconstruct.

The complete `audit_campaign` object equals `/audit-campaign-lock.json`, whose
independent SHA-256 is the declared
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every launcher-declared regular-file hash and every evidence hash in both
`generation-result.json` and `invocation.json` matched the mounted bytes.

The supplied-semantics boundary is intact:

- `/reference/reference-semantics` is present as required.
- `diff -qr --no-dereference` reports exact recursive equality with
  `/candidate/reference-semantics`.
- A separately sorted entry-type manifest is identical.
- No symlink exists under the candidate, trusted semantics, or structured
  trace.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts.

Evidence: `evidence/01_provenance.py`, `01_provenance.sh`, and
`01_provenance.log`. The script exits 0 and records every candidate regular-file
SHA-256. There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks for the maximum nesting depth of each parenthesis group
in a string of groups separated by spaces. The trusted canonical implements
that contract by:

1. splitting on the literal space;
2. discarding empty fields;
3. scanning each remaining group and returning its maximum depth.

Consequently, the canonical returns no result for no group (`"" -> []`) and
does not treat additional separator spaces as zero-depth groups.

The candidate uses a one-pass scan. It appends the current maximum at every
space, resets, and unconditionally appends once more at end-of-input. This is
correct for nonempty balanced groups separated by exactly one space. It is not
equivalent at empty/irregular-space boundaries.

### Translator fidelity

From the scratch copy I ran:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both commands exited 0. Both translated files have SHA-256
`afa6188c96fbcb733382af9864858d7c1c591c354d8f577c2acaa1aa148b246f`.
Thus `solution.mpy` is the exact trusted translation of `solution.py`.

### Independent differential test

`evidence/02_differential.py` independently imports
`/reference/canonical.py` and the scratch `solution.py`. It exercises the
documented example, all branch boundaries, all balanced groups through six
pairs, exhaustive pairs of groups through four pairs, and 500 deterministic
multi-group generated inputs. The generation procedure and fixed seed are in
the preserved script.

Command and result are in `evidence/02_fidelity.log`:

```text
python3 /audit-output/evidence/02_differential.py
documented: cases=1 mismatches=0
intended_valid: cases=1130 mismatches=0
boundary_or_ambiguous: cases=13 mismatches=7
EXIT_STATUS: 0
```

The seven retained mismatches are:

| Input | Trusted canonical | Candidate |
|---|---:|---:|
| `""` | `[]` | `[0]` |
| `" "` | `[]` | `[0, 0]` |
| `"  "` | `[]` | `[0, 0, 0]` |
| `"() "` | `[1]` | `[1, 0]` |
| `" ()"` | `[1]` | `[0, 1]` |
| `"()  ()"` | `[1, 1]` | `[1, 0, 1]` |
| `"()   (())"` | `[1, 2]` | `[1, 0, 0, 2]` |

This is material. In particular, `"()  ()"` still consists of two valid
parenthesis groups separated by spaces, and the trusted implementation
deliberately filters the empty split field. The prompt supplies no
exactly-one-space precondition. Empty input likewise has zero groups and should
produce zero outputs.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work`, used the trusted
`/reference/reference-semantics` and translator, and did not copy or reuse any
candidate kompiled definition or cache. K reports version 7.1.293.

The reviewer-authored `evidence/03_reconstruct.sh` records exact commands and
statuses. The important results are:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
EXIT_STATUS: 0

krun audit_concrete.mpy --definition audit-runtime-kompiled --output none
EXIT_STATUS: 0

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
EXIT_STATUS: 0

kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.parse-loop --output pretty
#Top
EXIT_STATUS: 0

kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --output pretty
#Top
EXIT_STATUS: 0
```

The first proof independently closes the loop claim. The complete-spec run
closes the conjunction of the loop claim and target theorem; the target uses
the loop circularity. Compiler warnings concern unused variables and unrelated
non-exhaustive fixed-semantic functions. No warning is a failed claim.

Before concrete execution, the harness function AST was independently compared
with `solution.py` and found identical. The LLVM run covers the documented
case, branch boundaries, empty input, and repeated-space candidate behavior.
The complete bounded build/proof output is in
`evidence/03_reconstruct.log`.

## 4. Adequacy and real-program pinning

### Claims in plain language

`parse-loop` says: starting at the actual fixed-semantics string-loop head with
suffix `S`, accumulator depth `D`, group maximum `M`, result list `VS`, and old
loop variable `OLD`, executing the remaining loop:

- consumes all of `S`;
- updates depth and maximum to the projections of `scanParens(S,D,M,VS)`;
- updates the result heap list to its completed maxima;
- leaves `char` equal to the last consumed character, or `OLD` when `S` is
  empty;
- preserves the continuation, stack, allocation counters, return, exception,
  and exit state.

Its precondition is only `parenInput(S)`: every code is `(`, `)`, or space.
It does not require balance, nonempty groups, normalized separators, or a
nonempty input.

`parse-nested-parens` says: from the explicit initial semantic state, calling a
closure with parameter `paren_string`, the submitted body, and definition
environment 0 returns heap reference 0. The entire final heap is exactly
`0 |-> list(parsedParens(S))`; the allocation counters, scopes, stack, return,
exception, and exit cells are all fixed. This is result-constraining, not a
free result or a one-way implication.

### Constructor-level program identity

The entry claim names the body through `parseLoopBody`,
`parseFunctionBody`, and `parseNestedParensClosure` rather than loading the
whole module text. `evidence/04_pinning.py` freshly parses the regenerated MPY
module and the candidate rule right-hand sides with `kast`, expands the two
aliases, and compares KAST trees structurally.

It found:

```text
actual_loop_body_sha256=39fdf2207115f6d3fe97dead9adbddc193469faa6696cf0783c5e9fb6c0acc1d
proof_loop_body_sha256=39fdf2207115f6d3fe97dead9adbddc193469faa6696cf0783c5e9fb6c0acc1d
actual_function_body_sha256=3c0e0bc0d0ac38492a9b5c38a042b7a86ac89db94ca0d338d2e6115fb4f23b91
proof_function_body_sha256=3c0e0bc0d0ac38492a9b5c38a042b7a86ac89db94ca0d338d2e6115fb4f23b91
closure_definition_environment=0
LOOP_CONSTRUCTOR_IDENTITY=PASS
FUNCTION_CONSTRUCTOR_IDENTITY=PASS
CLOSURE_BINDING_BODY_IDENTITY=PASS
```

The omitted typing import is a fixed-semantics no-op. Loading the actual
`FuncDef` would bind exactly this one-parameter closure and body at module
environment 0. Directly constructing that identical closure is therefore a
demonstrated semantically inert normalization, not a substituted program.

### Satisfiability and concrete substitution

`spec-ground.k` uses the satisfying input `"(()()) ()"` and fixes the claimed
result to `[2,1]`. It proves `#Top`, exit 0. The same input returns `[2,1]` in
both trusted canonical Python and generated Python. See
`evidence/04_adequacy.log`.

A separate body-sensitivity mutation changed the actually executed
`parseLoopBody` assignment from `maximum = depth` to `maximum = 0`. The mutated
definition compiled, but the unchanged proof produced
`WarnStuckClaimState` and exited 1. This changed the claim's executed term, not
merely an external source file. See `evidence/04_body_sensitivity.sh` and
`.log`.

### Adequacy failure

Mechanical pinning does not rescue the source contract. For `S = .IntSeq`,
`parenInput(S)` is true and `parsedParens(S)` is `[0]`; the trusted canonical
returns `[]`. For the code sequence of `"()  ()"`, the same precondition is
true and the claimed/candidate result is `[1,0,1]`; the intended canonical
result is `[1,1]`. The entry claim therefore constrains the result precisely,
but not to the intended result on a material part of its own formal domain.

## 5. Rule-by-rule static soundness review

`evidence/05_rule_inventory.tsv` is the exhaustive source inventory generated
by `evidence/05_inventory.py`. It contains:

```text
inventory_entries=958
kind_counts=claim:2,configuration:1,context:5,rule:713,syntax:237
flag_counts=concrete:35,function:156,macro:4,no-evaluators:22,
            owise:27,priority:45,strict:2,symbol:25,total:112
```

All 928 fixed-semantics entries are individually recorded as the exact trusted
supplied baseline. The remaining 30 entries are the 10 proof-local syntax
declarations, all 18 proof-local rules, and 2 claims. The full used-path
mapping, configuration/cell analysis, opaque-symbol list, and per-group
proof-local decisions are preserved in `evidence/05_static_review.md`.

### Proof-local rule decisions

- `parseLoopBody`, `parseFunctionBody`, and
  `parseNestedParensClosure` (three declarations and three rules) are exact
  constructor aliases. They do not match or preempt a fixed operational redex.
- `parenMax` has two disjoint, exhaustive equations (`A > B` and `A <= B`)
  with mathematically correct right-hand sides.
- `scanParens` has five disjoint structural cases: empty; code 40; code 41;
  code 32; and `owise`. Each recursive equation consumes one code. The
  fall-through also matches the submitted code's ignored-character behavior.
- `scanDepth`, `scanMaximum`, and `scanValues` project the three fields of
  `scanDone`; ground `scanParens` structurally normalizes to that constructor.
- `finalChar` has complete empty/cons cases and consumes one code recursively.
- `parsedParens` names completed group maxima followed by the final current
  maximum. It is spec-side only and does not replace execution.
- `parenInput` has complete empty/cons cases and accepts exactly codes 40, 41,
  and 32.

All proof-local `[total]` declarations have the stated exhaustive or
normalizing coverage. There is one proof-local `owise` and no proof-local
priority, simplification, `functional`, opaque, or `no-evaluators`
declaration. Guards are disjoint or agreeing; recursive calls descend. There
is no program-result oracle and no operational bridge requiring a
bridge-equivalence theorem. Instead, `parse-loop` is the machine-checked
connection theorem from fixed loop execution to the mathematical scan.

The used fixed path includes real closure application, argument binding,
left-to-right condition evaluation, string iteration, local writes, integer
arithmetic, in-place list append, return, frame pop, and allocation. Every
material state/control effect is represented. The 22 fixed opaque symbols are
confined to unused float, MD5, and sorting paths and cannot affect this proof.

I found no unsound proof-local rule and therefore make no rule-unsoundness
allegation requiring a false-conclusion witness. The rejection is an intent
adequacy failure, for which the concrete inputs above are direct witnesses.

## 6. Fresh non-vacuity test

I ignored any candidate validation material and created
`/tmp/audit-work/reconstruction/spec-vacuity-audit.k`. It changes the target
heap obligation from `parsedParens(S)` to that list with an extra trailing
zero. For satisfying input `"()"`, the true result is `[1]` and the mutation
requires `[1,0]`.

Exact results in `evidence/06_nonvacuity.log`:

```text
kprove spec-vacuity-audit.k --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run --output none
MUTATION_BUILD_EXIT_STATUS: 0

kprove spec-vacuity-audit.k --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --output pretty
Warning (WarnStuckClaimState)
MUTATION_PROOF_EXIT_STATUS: 1
NONVACUITY=EXPECTED_FALSE_CLAIM_FAILURE
```

The backend selected the even simpler satisfying branch `S = .IntSeq`: actual
heap `list(vCons(0,.ValSeq))` cannot unify with the mutated two-element result.
The failure is the intended unmet result obligation, not parsing, import,
timeout, or backend failure. The proof is non-vacuous.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the supplied MPY semantics, for every finite semantic `IntSeq S` whose
codes are all 40, 41, or 32, the mechanically pinned submitted function has
the following partial-correctness property: if it terminates from the explicit
entry configuration, it returns reference 0 to the unique heap list computed
by `parsedParens(S)`, with all named control/state cells as stated. The loop
claim establishes the corresponding exact scan invariant.

That is a strong and honest execution-characterization theorem for the real
generated program. It is not a theorem that `parsedParens(S)` equals the
trusted HumanEval result for all source-contract inputs.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, compiler, Haskell backend, solver, and builtin hooks | Both reachability claims and ground/mutation runs | Normal unavoidable checker trust; exact versions and commands recorded. |
| Launcher-supplied MPY semantics (928 inventoried declarations/rules/contexts/configuration entries) | All operational execution | Required benchmark trust boundary; candidate tree is byte/type identical. Relevant path was statically reviewed and concretely executed. |
| Trusted `py2mpy.py` transliteration | Source-to-MPY identity | Acceptable; submitted MPY is byte-identical to fresh output, then KAST body identity independently pins the claim. |
| K mathematical primitives for unbounded Int, Bool, String, Map, and List | Arithmetic, guards, cells, structural sequences | Standard fixed low-level boundary. Input codes are restricted to the three ASCII characters, avoiding Unicode-model ambiguity. |
| Fixed opaque float/MD5/sort symbols | None | Unreachable and non-influential for branches, result, state, or control in this program. |
| Interpretation of the English task through trusted canonical Python | Intent adequacy | The canonical is a trusted input. It explicitly filters empty split fields; concrete mismatches expose the candidate/spec disagreement. |
| CPython execution and the 1,130-case differential run | Finite implementation-to-canonical evidence | Empirical only, reproducible, and not substituted for K proof. It supports the normalized-input bridge but cannot erase the boundary counterexamples. |
| Informal statement that a valid balanced single-space group scan computes maximum nesting | Human-facing meaning of `parsedParens` on the normalized subset | Mathematically straightforward and heavily differentially checked, but not itself a separate universal K theorem. |
| Termination | Total-correctness interpretation | Excluded: the requested proof is partial correctness. The theorem does not claim a separate termination proof. |

### Gate/status accounting

- Gate A, real-program soundness: **PASS**. Fresh `#Top`, exact program
  identity, valid proof-local equations, satisfying witness, body sensitivity,
  and false-result rejection all pass.
- Gate B, intent adequacy: **FAIL**. The entry precondition includes empty and
  repeated-space inputs, but the proved/candidate result differs materially
  from the trusted source contract on them.
- Gate C, trust/evidence auditability: **PASS** for the theorem actually
  reconstructed. Every command, input scope, trust boundary, and finite
  empirical bridge is preserved and honestly bounded.

The generic Kit description would call a sound theorem with a failed adequacy
gate `SOUND-BUT-LIMITED`. This benchmark requires a candidate verdict about
the full HumanEval contract. Here the limitation is material: the theorem
fixes the wrong result on satisfying source-boundary inputs. Therefore it is
not a legitimate partial-correctness proof of the requested task.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
