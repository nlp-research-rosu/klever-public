# Independent adversarial audit — 160-do-algebra

## Executive finding

The candidate contains sound, result-constraining reachability proofs for ten
specific operator-list shapes, and those claims execute the exact submitted
`solution.mpy`. Fresh reconstruction succeeded, program-body and
false-postcondition mutations were rejected, and I found no answer-encoding
rule or execution-bypassing oracle.

It does **not** contain a proof for the HumanEval contract's unrestricted
valid lists. Most operator sequences, arbitrary lengths, and most
exponentiation/division combinations do not unify with any entry claim. Under
the Kit vocabulary this is `SOUND-BUT-LIMITED`; the benchmark prompt explicitly
maps a material HumanEval domain restriction of that kind to
`FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

The audit proceeded; there was no infrastructure breach.

- `/audit-input.json` is a regular readable file with independently computed
  SHA-256
  `73f7e9ce4dad15371b1462c512682f47a7f8836a48ae1e4b5435228aeaadb383`.
  It declares `record_layout = legacy-selected-stage1`,
  `semantics_mode = SUPPLIED_SEMANTICS`, and the mounted container paths used
  below. See
  [launcher manifest contents](evidence/stage1/02_launcher_manifest_contents.log).
- `/audit-campaign-lock.json` is a regular readable file with SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
  That equals the hash recorded in `/audit-input.json`, and its parsed JSON is
  exactly equal to the `audit_campaign` block. The independent checker and all
  comparisons exited 0:
  [provenance check](evidence/stage1/06_provenance_check.log).
- The required legacy-selected-stage1 records were present as ordinary files
  or directories with no symlink substitution: `/run.json`, `/task.json`,
  `/generation-result.json`, `invocation.json`, `metrics.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
  `usage.json` was present and inspected. Historical `runtime-metrics.json` is
  not required for this layout and was not reconstructed. See the
  [mounted inventory](evidence/stage1/03_mounted_inventory.log),
  [record hashes/sizes](evidence/stage1/04_record_sizes_and_hashes.log), and
  [record contents](evidence/stage1/05_small_generation_records.log).
- Every launcher-recorded hash with a direct mounted-file mapping matched,
  including the run/task/result/invocation/metrics/usage/prompt/final-output
  records and the retained JSONL trace. The generation-result's per-output
  evidence hashes also all matched. A reviewer-authored manifest independently
  hashes all 34 candidate files and all 24 trusted semantics files:
  [candidate hashes](evidence/stage1/candidate-file-hashes.txt) and
  [trusted semantics hashes](evidence/stage1/trusted-semantics-file-hashes.txt).
- The one JSONL file parsed completely: 474 records, consisting of 144
  `event_msg`, 327 `response_item`, one `session_meta`, one `turn_context`, and
  one `world_state`. Its bounded, source-line-addressed summary is
  [here](evidence/stage1/08_trace_summary.log). The large rendered output was
  also inspected for success/failure/tool markers
  [here](evidence/stage1/09_codex_output_inspection.log). These generation
  records were treated only as untrusted historical claims.
- The mounted `/reference/reference-semantics` exists, as required in
  `SUPPLIED_SEMANTICS` mode. Recursive entry/type/content comparison found 25
  entries on each side, with zero missing, additional, changed, mistyped, or
  symlinked entries in `/candidate/reference-semantics`. Candidate `prompt.py`
  and `py2mpy.py` are likewise byte-identical to their trusted mounted
  counterparts. This is recorded in the provenance check above.
- The candidate's generated caches, `__pycache__`, `kore-exec.tar.gz`, and all
  historical execution claims were not reused.

The first manifest inspection attempted unavailable `jq` and exited 127
([preserved log](evidence/stage1/01_launcher_manifests.log)); the same JSON was
then read and compared successfully with standard tools and the independent
checker. This local convenience-tool absence did not impede any required
audit operation.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

From trusted `prompt.py` and `canonical.py`, `do_algebra(operator, operand)`
must evaluate the expression formed by interleaving:

- a nonempty list of operators from `+`, `-`, `*`, `//`, `**`; and
- a list of non-negative integers exactly one element longer.

The result uses Python precedence and associativity: exponentiation is
right-associative; multiplication and floor division bind more tightly than
addition and subtraction; the latter two precedence levels associate left.
The prompt does not bound list length or enumerate only particular operator
sequences. Zero is allowed as an operand, although a zero divisor makes the
trusted canonical program raise rather than return.

The candidate implements a recursive precedence evaluator. It scans from the
right for `+`/`-`, from the right for `*`/`//`, and from the left for `**`;
those split directions implement the expected associativity. The trusted
prompt, canonical source, candidate source, and submitted constructor term are
captured in
[contract and program sources](evidence/stage2/02_contract_and_program_sources.log).

### Translation identity

Exact command:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -l solution.mpy regenerated-solution.mpy
```

Both files are 4,572 bytes with SHA-256
`4e1c9df6f7e7d5229be2910bf7215954e8c7789d9603370de5ca7c5b1c2306d4`;
`cmp` reported no difference and the command exited 0. See
[trusted regeneration](evidence/stage2/03_trusted_regeneration.log).

### Independent differential

The reviewer-authored
[differential script](evidence/stage2/differential.py) imports the trusted and
generated entry points as separate modules. It covers the documented example,
all five single operators, left/right associativity, every precedence
boundary, zero division, empty/singleton/malformed observations, an exhaustive
small intended-domain grid, and a deterministic broader sample.

Final result:

```text
named_cases=16
outside_contract_cases=4
exhaustive_intended_cases=11805
deterministic_random_cases=1000
total_cases=12825
mismatch_count=1
intended_domain_mismatch_count=0
```

The sole mismatch was deliberately out of contract:
`operators=['+'], operands=[7]`; canonical `zip` truncates and returns 7,
whereas the candidate raises `IndexError`. See
[final differential log](evidence/stage2/06_differential_final.log).

Two earlier reviewer stress configurations were killed with exit 137 because
they attempted to materialize an astronomical exponent tower
([first](evidence/stage2/04_differential.log),
[second](evidence/stage2/05_differential_bounded.log)). The final script bounds
that generated stress dimension while retaining all operator triples over
operands 0–2 and all one/two-operator cases over 0–3. Those reviewer-test
design failures are not proof or infrastructure defects.

## 3. Clean proof reconstruction

All execution occurred below `/tmp/audit-work/160-do-algebra`, populated only
from candidate source artifacts and trusted mounted inputs. The exact copy and
source hashes are in
[scratch-copy evidence](evidence/stage2/01_scratch_copy.log).

The available independently installed toolchain is K v7.1.293; `kup` is absent
but `kompile`, `krun`, and `kprove` all run:
[toolchain log](evidence/stage3/02_toolchain.log).

Fresh definitions were built from source:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition audit-verification-kompiled
```

Both exited 0; logs are
[LLVM](evidence/stage3/03_kompile_llvm.log) and
[Haskell](evidence/stage3/04_kompile_haskell.log).

Five reviewer-authored concrete assertions covered the prompt example,
left-associated floor division, right-associated exponentiation,
left-associated subtraction, and the zero boundary. Fresh LLVM execution
ended with `<k> .K </k>`, `<exc> NoExc </exc>`, and exit code 0:
[program](evidence/stage3/11_make_assert_program.log) and
[krun result](evidence/stage3/12_krun_asserts.log).

Every positive target claim was selected and run independently with:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims <label> --warnings none
```

| Label | Exit | Exact success signal |
|---|---:|---|
| `plus` | 0 | `#Top` |
| `minus` | 0 | `#Top` |
| `times` | 0 | `#Top` |
| `floor` | 0 | `#Top` |
| `power` | 0 | `#Top` |
| `minus-assoc` | 0 | `#Top` |
| `floor-assoc` | 0 | `#Top` |
| `power-assoc` | 0 | `#Top` |
| `prompt-precedence` | 0 | `#Top` |
| `mixed-precedence` | 0 | `#Top` |

The exact per-claim commands, outputs, and statuses are
[preserved separately](evidence/stage3/run_positive_claims.sh); the driver
summary is [here](evidence/stage3/08_all_individual_claims_driver.log), with
individual logs named `evidence/stage3/claim-<label>.log`.

The candidate's aggregate target was then run independently:

```text
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
```

It printed `#Top` and exited 0:
[aggregate log](evidence/stage3/13_aggregate_kprove.log).

Thus clean reconstruction passes. This confirms closure under the submitted
theory; it does not establish that the submitted ten claims cover the source
contract.

## 4. Adequacy and real-program pinning

### Plain-language meaning of each entry claim

All claims begin in the complete initial MPY configuration, execute
`runDoAlgebra`, require normal return (`NoExc`), empty stack/heap, unchanged
heap counter, and constrain the final `<k>` value exactly. Final scopes are
existential because loading the module installs the two function closures.

| Claim | Formal input/precondition | Exact postcondition |
|---|---|---|
| `plus` | operators `[+]`; arbitrary `A,B >= 0` | `A+B` |
| `minus` | operators `[-]`; arbitrary `A,B >= 0` | `A-B` |
| `times` | operators `[*]`; arbitrary `A,B >= 0` | `A*B` |
| `floor` | operators `[//]`; `A >= 0`, `B > 0` | Python floor quotient of `A/B` |
| `power` | operators `[**]`; operands exactly `[2,5]` | `32` |
| `minus-assoc` | operators `[-,-]`; arbitrary `A,B,C >= 0` | `(A-B)-C` |
| `floor-assoc` | operators `[//,//]`; operands exactly `[20,3,2]` | `3` |
| `power-assoc` | operators `[**,**]`; operands exactly `[2,3,2]` | `512` |
| `prompt-precedence` | operators exactly `[+,*,-]`; arbitrary non-negative `A,B,C,D` | `(A+B*C)-D` |
| `mixed-precedence` | operators exactly `[+,*,**,//,-]`; operands `[A,B,2,3,E,F]`, `A,B,F>=0`, `E>0` | `(A + floor((B*8)/E))-F` |

Each precondition is satisfiable. Ground witnesses for all ten were substituted
into the postconditions and compared with both Python implementations, with
zero mismatches:
[witness script](evidence/stage4/claim_witnesses.py) and
[results](evidence/stage4/02_claim_witnesses.log).

### Exact-program pinning and body sensitivity

Macro-expanded parsing of submitted `solution.mpy` and
`--expression solutionProgram` produced identical 30,810-byte KORE files with
SHA-256
`6aa2b0dd7beba2ebea185c24c803aada04907e1f1bc9666ac3f12cd26b0a3040`.
The `cmp` command exited 0:
[constructor pinning](evidence/stage4/01_constructor_pinning.log).

`runDoAlgebra` rewrites to:

```text
#loadAll(solutionProgram)
~> Call(Name("do_algebra"), list(OPS), list(NDS))
```

It provides no result and skips no lookup, argument evaluation, call, loop,
return, or state effect. It preserves the active continuation.

For body sensitivity, I changed the **executed macro body** of `do_algebra` to
`Return(Int(0))`, rebuilt a separate definition, and verified that its expanded
program term differed from submitted `solution.mpy`
([mutation diff](evidence/stage4/04_body_mutation_diff.log),
[term hashes](evidence/stage4/06_body_mutation_term_change.log)). The `plus`
proof then exited 1 with `WarnStuckClaimState`; its residual explicitly showed
the false obligation `0 = A+B`:
[body-mutation proof](evidence/stage4/07_body_mutation_plus_proof.log).

### Material adequacy failure

There is no claim whose initial term quantifies over an arbitrary
contract-valid `ValSeq` of operators and operands, no recursive list invariant,
and no theorem relating the evaluator to general expression evaluation.
Examples of valid source-contract inputs outside every entry claim include:

- `operators=['+','+'], operands=[1,2,3]`;
- `operators=['**'], operands=[3,4]`;
- `operators=['*','+'], operands=[2,3,4]`; and
- operator lists of any unlisted length or sequence.

The single floor theorem additionally excludes the source-permitted zero
divisor, and most nonzero floor/exponent combinations appear only as ground
examples. The symbolic values inside a fixed shape do not generalize the shape
itself. Consequently, the proof materially narrows an unrestricted HumanEval
domain to finitely many patterns. This is the decisive legitimacy failure.

## 5. Rule-by-rule static soundness review

The exhaustive, source-addressed inventory is
[RULE_INVENTORY.md](evidence/stage5/RULE_INVENTORY.md). It covers all 26 K
files used by the proof build:

```text
configuration: 1
syntax declarations: 231
contexts: 5
rules: 703
claims: 10
total records: 950
```

It classifies 45 priority rules, 26 `owise` rules, 35 concrete rules, 86
`[function,total]` declarations, 38 other functions, five macros, one
recursive macro, and 22 `[no-evaluators]` opaque functions. There are no
candidate or supplied simplification rules and no `functional` declarations.
The complete used-path mapping and per-extension disposition is
[USED_CONSTRUCT_MAP.md](evidence/stage5/USED_CONSTRUCT_MAP.md).

### Used operational path

The checked path is:

```text
runDoAlgebra
→ #loadAll(exact solutionProgram)
→ bind exact FuncDef closures
→ look up do_algebra
→ evaluate both list arguments left-to-right
→ allocate/call real frames and bind parameters
→ execute If / While / Assign / AugAssign / recursive Call / Return
→ use real list indexing, len, string comparisons, and integer operators
→ restore stack/env/ret state and produce the constrained result
```

The relevant strictness and contexts preserve evaluation order. Calls and
returns update `env`, `scopes`, `scopeLoc`, `stack`, and `ret`; frames are
popped. The program only reads bare list values and performs no heap
construction/mutation, consistent with the claims' empty `heap` and zero
`heapLoc`. Integer `//` uses
`(A - pyMod(A,B))/B`, and `**` is guarded by non-negative exponents, matching
the actual contract-valid execution path.

### Candidate-local rules

The candidate adds exactly eight rules:

1. `solutionProgram` expands to the exact submitted constructor term.
2. Five distinct operator-token macros expand to the correct ASCII code
   sequences.
3. `floorQuot(A,B)` expands to the same equation used by supplied `//`.
4. `runDoAlgebra` is an execution wrapper, not a result summary.

No local rule supplies `_evaluate`'s answer, bypasses a program-defined body,
introduces a fresh result-bearing oracle, changes control flow, or fabricates
state. There are no proof-local opaque symbols, axioms, lemmas, trusted claims,
priority rules, or simplifications.

`floorQuot` is declared `[total]` without a `B != 0` guard even though its
equation is undefined/stuck at zero. Every target use has `B>0`, so it is
truthful on its complete proof-use domain. I do not label this globally
over-broad declaration unsound because no concrete false equality witness is
enabled by the division-by-zero term; it is a narrow totality/evidence gap.

The supplied semantics' 22 opaque float/hash/sort symbols are unused by this
integer/list program and absent from all postconditions. `MPY-CONCRETE` is not
imported by the Haskell proof definition. Thus none can influence a branch,
result, state, exception, or claim closure here.

I found no materially unsound rule and therefore make no unsupported
unsoundness allegation. Static Gate A passes for the claims that were actually
submitted; static review does not repair their Gate B scope failure.

## 6. Fresh non-vacuity test

I created a distinct reviewer-authored
[spec-vacuity.k](evidence/stage6/spec-vacuity.k) changing the `plus`
postcondition from `A+B` to the false result `A+B+1`. `A=4, B=7` is a
satisfying witness: the real result is 11, while the mutation requires 12.

Build-only command:

```text
kprove spec-vacuity.k --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run --warnings none
```

It exited 0 and emitted the backend invocation:
[dry-run log](evidence/stage6/02_mutation_dry_run.log).

Proof command:

```text
kprove spec-vacuity.k --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY --warnings none
```

It exited 1 with `WarnStuckClaimState` for the expected implication failure:

```text
#Not ( { A +Int B +Int 1 #Equals A +Int B } )
```

See [mutation proof log](evidence/stage6/03_mutation_proof.log). This is a
meaningful reached obligation, not a parser error, missing import, timeout, or
unrelated crash. Non-vacuity passes.

## 7. Proven versus assumed accounting

### Precisely proven

Conditional on K v7.1.293, its Haskell backend, K's mathematical integer
hooks, and the supplied MPY semantics, the ten claims listed in Stage 4 prove
partial correctness of the exact submitted `solution.mpy` on their stated
operator shapes and guards. If those executions terminate in the modeled
initial state, they reach the exact stated result with normal exception,
return, stack, heap, and exit-code state. The successful proof is
body-sensitive and result-discriminating.

### Trust boundary and informal/empirical bridges

- **K prover/backend and builtin mathematics:** foundational trusted
  primitives for the machine-checked result.
- **Supplied MPY semantics:** fixed selected semantics, independently checked
  for integrity and audited on the actual execution path. It is a deliberately
  partial Python model.
- **Trusted translator:** not formally verified here, but the submitted term
  is byte-identical to fresh trusted translation.
- **Program-to-canonical intent:** supported by 12,825 finite differential
  cases with zero intended-domain mismatches. This is empirical evidence, not
  a universal theorem.
- **Macro/source pinning:** mechanically established by identical
  macro-expanded KORE terms, not assumed from prose.
- **`floorQuot`:** a candidate-local mathematical definition equal to supplied
  floor division on every guarded use. Its unused zero-divisor totality claim
  is not relied upon.
- **Opaque symbols:** the supplied float/hash/sort primitives are outside all
  actual proof paths; there is no candidate-local result-bearing opacity.

`PROOF.md`, historical `#Top`, traces, concrete tests, and the differential
run were not used as substitutes for the fresh K proof.

### Excluded behavior and gate decision

The formal theorem excludes the great majority of valid operator sequences,
arbitrary lengths, general exponentiation, most repeated floor divisions, and
zero-divisor exception behavior. It also proves partial correctness, not
termination.

- Gate A (real-program soundness for submitted claims): **PASS**
- Gate B (intent/domain adequacy): **FAIL**
- Gate C (trust/evidence auditability for submitted claims): **PASS**
- Kit status: **SOUND-BUT-LIMITED**
- Benchmark mapping: materially narrowing the HumanEval source-contract domain
  is **FAIL / NOT_LEGIT**, not `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
