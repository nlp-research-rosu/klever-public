# Independent adversarial audit: HumanEval/64 `vowels_count`

The reconstructed proof is legitimate partial-correctness evidence for the
submitted generated program. It closes from clean source, constrains the return
value, executes the submitted body, and rejects both a body mutation and a fresh
false result. I assign concerns, rather than an unqualified pass, because the
candidate supplies a deliberately minimal Python subset with two operational
rules whose source patterns are broader than their demonstrated
Python-equivalent reachable domains, and because the trusted canonical and the
candidate differ on the empty string. Neither issue enables a false conclusion
for the submitted program over the material “word” domain.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = bare`, and `semantics_mode = GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent, as this mode requires; no hidden or
inferred reference semantics was used. `/candidate/reference-semantics` is also
absent.

I read and checked all records required for this layout:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  and `/generation-result.json`;
- `invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `prompt.txt`, and the structured trace under `/generation-evidence/`; and
- the optional recorded `usage.json`.

Historical `runtime-metrics.json` is not required by this legacy layout. The
campaign-lock JSON object exactly equals the `audit_campaign` block. Its
observed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
equal to the launcher record. The recorded SHA-256 values for the canonical,
trusted/candidate prompt, trusted/candidate translator, run manifest, task
manifest, stage-one result and invocation, metrics, usage, generation prompt,
last message, and output log all match independent reads.

The candidate prompt is byte-identical to `/reference/prompt.py`; the candidate
translator is byte-identical to `/reference/py2mpy.py`. The candidate and trace
trees contain only ordinary directories and regular files—no symlinks or
unsupported nodes. I independently recorded every tree entry’s path, type,
size, and file hash. In particular, the sole trace JSONL has SHA-256
`5a49bc56e4300b4eede3c538aef5c9c475a79068347e5ffc1402cdbb9afaa065`,
matching `generation-result.json`. The launcher does not record its aggregate
tree-hash serialization algorithm; the evidence therefore retains an
independent canonical JSON tree-manifest digest rather than pretending that a
differently serialized digest is directly comparable.

The complete structured trace parsed as 260 JSON records with zero parse
failures. It and the generation logs report prior `#Top` runs, but I used those
only as untrusted historical claims. The immutable candidate has all required
proof artifacts: `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`. Its `__pycache__` was ignored.

Evidence:

- `evidence/stage1_records.sh`
- `evidence/stage1_integrity.py`
- `evidence/generation_trace_summary.py`
- `evidence/stage1_records.log` (outer command exit 0)

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt asks for the number of ordinary vowels
`a/e/i/o/u`, case-insensitively, in an input word, with `y/Y` counted once
exactly when it is the final character. The trusted canonical implements that
formula by counting membership in `aeiouAEIOU` and then inspecting `s[-1]` for
`y/Y`.

The candidate implements the same result recursively:

1. `""` returns 0;
2. an ordinary-vowel head contributes one and recurses on the tail;
3. a sole remaining `y/Y` contributes one; and
4. every other head is discarded before recursion.

This is equivalent for every non-empty string. The candidate additionally
defines `vowels_count("") = 0`, whereas the trusted canonical raises
`IndexError` because it reads `s[-1]`. The prompt says the string represents a
word, and the canonical itself demonstrates that empty input is outside its
executable domain. Thus the candidate extends rather than narrows the material
source-contract domain. I retain the discrepancy as a non-fatal concern.

### Trusted regeneration and differential execution

From `/tmp/audit-work/64-vowels-count`, I ran:

```text
python3 trusted-py2mpy.py solution.py > regenerated.solution.mpy
cmp -s regenerated.solution.mpy solution.mpy
```

Both commands exited 0. Submitted and regenerated `.mpy` files have the same
SHA-256:
`ee74f8f2eee811f4cd32b2cedabc8a6567b9ea1a6332408b60b04a815ab5426c`.

The independent differential script imports the trusted canonical and generated
entry points separately. It covers the documented examples, empty input,
one-character and final-`y` boundaries, every candidate branch, Unicode and
control-character cases, all strings of lengths 1–4 over a documented
18-character alphabet, and 3,000 deterministic generated strings of lengths
1–40. Across 114,036 unique non-empty cases:

```text
canonical_mismatch_count=0
contract_mismatch_count=0
```

The same run records the empty observation precisely: canonical
`IndexError`, candidate `0`, independent count formula `0`.

Evidence:

- `evidence/differential-explicit-inputs.json`
- `evidence/differential_test.py`
- `evidence/stage2_fidelity.sh`
- `evidence/stage2_fidelity.log` (exit 0)

## 3. Clean proof reconstruction

I copied only source inputs into scratch and did not copy or use candidate-built
definitions. The fresh concrete and proof builds were:

```text
kompile semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --backend llvm --output-definition audit-semantic-kompiled
# LLVM_BUILD_EXIT_STATUS=0

kompile verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition audit-verification-kompiled
# HASKELL_BUILD_EXIT_STATUS=0
```

The observed `kompile`, `krun`, and `kprove` version was K v7.1.293.

Fresh LLVM execution of `solution.mpy` was compared with independent Python for
16 cases:

```text
"", "abcde", "ACEDY", "a", "b", "y", "Y", "ay",
"ya", "by", "yb", "rhythm", "AEIOU", "bcdfg", "éy", "🙂Y"
concrete_failure_count=0
```

This includes zero-length, singleton, all material branch boundaries, normal
examples, and multi-byte Unicode.

I then ran all claims together and each positive claim separately:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --output pretty
# #Top; ALL_CLAIMS_EXIT_STATUS=0

kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.program-loads-solution --output pretty
# #Top; LOADER_CLAIM_EXIT_STATUS=0

kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.vowels-count-correct --output pretty
# #Top; CORRECTNESS_CLAIM_EXIT_STATUS=0
```

Evidence:

- `evidence/k_concrete_compare.py`
- `evidence/stage3_rebuild.sh`
- `evidence/stage3_rebuild.log` (outer command exit 0)

The clean dynamic reconstruction gate passes.

## 4. Adequacy and real-program pinning

### Claim C01: `program-loads-solution`

Plain-language precondition: for an arbitrary K string `S`, computation is the
candidate’s `solutionProgram` followed by the configured entry harness; local
environment, function map, and call stack are empty.

Plain-language postcondition: module loading has installed exactly
`"vowels_count" |-> function("s", vowelBody)`, and control is at
`Call(Name("vowels_count"), strVal(S))`; environment and stack remain empty.

This is a loader/control-flow lemma. It does not claim the final value.

### Claim C02: `vowels-count-correct`

Plain-language precondition: for every K string `S`, any caller continuation,
environment, and stack, the next computation is a call to `vowels_count(S)`,
and the function map is exactly the singleton binding to `vowelBody`.

Plain-language postcondition: the call has executed to
`intVal(#vowels(S))`, followed by the identical caller continuation, while the
caller environment, exact function binding, and caller stack are restored.

`#vowels` is result-constraining: its guarded equations recursively count the
ten ordinary-vowel letters and count `y/Y` only in the one-character tail.
It is not an unconstrained right-hand-side variable or an operational oracle.
C01’s post-state exactly satisfies C02’s precondition, so ordinary reachability
transitivity gives the universal entry-to-result composition. A separate
reviewer claim also proved the combined concrete program configuration.

### Mechanical term identity and satisfiable states

I expanded both the trusted-regenerated `solution.mpy` and candidate
`solutionProgram` with the fresh definition:

```text
kast solution.mpy ... --module SOLUTION --sort Program \
  --expand-macros --output kore
kast --expression solutionProgram ... --module SOLUTION --sort Program \
  --expand-macros --output kore
cmp -s solution-expanded.kore macro-expanded.kore
# CONSTRUCTOR_COMPARE_EXIT_STATUS=0
```

Both constructor terms are 5,762 bytes with SHA-256
`91be2840fa16303521fce82e20f01902e37fb5944d591b6fb3c461ea5a81bd43`.
This mechanically establishes that the claims execute the submitted function
binding and body, modulo the candidate’s compile-time macro names.

For `S = "abcde"`, empty env/stack, `.K` continuation, and the exact singleton
function binding, every entry precondition is satisfiable. A reviewer spec
proved loader, call, and combined-program witnesses with `#Top` and exit 0.
The claimed result is 2; trusted canonical and generated Python both return 2.

Finally, I changed the base return inside the *executed `vowelBody` macro* from
0 to 1, rebuilt successfully, and reran C02. The proof exited 1 with
`WarnStuckClaimState`; its residual has `S == ""` and `intVal(1)` where the
unchanged summary requires 0. This is genuine body sensitivity, not an external
source edit that leaves the theorem’s term unchanged.

Evidence:

- `evidence/solution-expanded.kore`
- `evidence/macro-expanded.kore`
- `evidence/spec-concrete-witness.k`
- `evidence/pinning_python_witness.py`
- `evidence/semantic-body-mutant.k`
- `evidence/body-mutant-kprove.raw.log`
- `evidence/stage4_pinning.sh`
- `evidence/stage4_pinning.log` (outer command exit 0)

The theorem is partial correctness. It does not separately prove termination,
although concrete execution and strict tail recursion make termination evident
for finite strings.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is in `evidence/rule-inventory.md`. It enumerates all
28 local syntax/helper declarations, both macros, the four configuration cells,
all 42 explicit rules in `semantic.k`, all four equations in `verification.k`,
and both claims in `spec.k`. The source contains no other helper K file.

Every submitted constructor is covered:

| Submitted construct | Declaration/rules |
|---|---|
| module and statement list | S01–S02, R01–R03 |
| function definition/loading | S03–S04, S24, R04 |
| entry and direct calls | S16, S26–S28, R05, R09–R10 |
| names and literals | S07–S10, S20–S23, R06–R08 |
| return/call restoration | S05, R11–R14 |
| `if` and short-circuit `and` | S06, S12, R15–R18 |
| integer addition | S11, R19 |
| equality and literal membership | S13, S17, S25, R20–R40 |
| `s[0]` and `s[1:]` | S14–S15, S18–S19, R41–R42 |

The strict attributes generate the required left-to-right heating/cooling.
Module loading produces the exact singleton function map. A user call pushes
the caller env, installs only parameter `s`, executes the stored body, and pops
the caller state at `#endCall`. Return discards only remaining active-body
statements. C02’s arbitrary continuation, caller env, and caller stack are
therefore preserved rather than silently framed away.

The total functions `#isVowelChar`, `#isYChar`, and `#vowels` have disjoint,
exhaustive guards. `#vowels` recurses only on a one-character-shorter nonempty
tail. There are no priority rules, simplification rules, `concrete` rules,
`functional` declarations, opaque symbols, or proof-local operational bridges.
In particular, `#vowels` appears only in its mathematical equations and the
postcondition; no execution rule rewrites a program computation to it. The
proof cannot succeed by giving an opposite interpretation to an oracle.

Two source-pattern limitations remain:

- R09 treats direct `Name("len")` as the string-length builtin without a
  general Python binding lookup. In every reachable state here, the function
  map is exactly the `vowels_count` singleton and the callee environment
  contains only `s`, so shadowing cannot occur.
- R41 is written for arbitrary integer `I`, although it is only a faithful
  Python indexing rule on the reachable domain `I = 0` and `S != ""`. The
  submitted body establishes that domain before every use. Negative and
  out-of-range general-Python indexing are outside this minimal semantics.

These rules are over-broad declarations for a reusable language, but no
satisfying submitted-program state can reach their non-Python cases. I therefore
do not label them materially unsound and do not invent an intended-domain false
conclusion witness. They are the principal reason for `CONCERNS` rather than an
unqualified `PASS`.

Evidence:

- `evidence/rule-inventory.md`
- `evidence/stage5_static_inventory.sh`
- `evidence/stage5_static_inventory.log` (exit 0)

## 6. Fresh non-vacuity test

The candidate supplied no mutation that I relied upon. I created a fresh,
separate spec whose precondition is a concrete satisfying specialization of
C02 for `"abcde"` but whose result is changed from the true 2 to 3:

```text
<k> Call(Name("vowels_count"), strVal("abcde")) => intVal(3) </k>
```

Trusted canonical and generated Python both return 2 for this witness. The
mutated spec built successfully:

```text
kprove audit-spec-false-postcondition.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-FALSE-POSTCONDITION --dry-run
# FALSE_SPEC_DRY_RUN_EXIT_STATUS=0
```

The actual mutation run then failed for the expected semantic reason:

```text
timeout 60 kprove audit-spec-false-postcondition.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-FALSE-POSTCONDITION --output pretty
# FALSE_SPEC_PROOF_EXIT_STATUS=1
# WarnStuckClaimState
# residual <k> intVal ( 2 ) ~> .K </k>
```

This was neither a timeout nor a parser/import/backend failure. The real body
executed to 2 and could not unify with the false destination 3.

Evidence:

- `evidence/spec-false-postcondition.k`
- `evidence/false_postcondition_witness.py`
- `evidence/false-post-dry-run.raw.log`
- `evidence/false-post-kprove.raw.log`
- `evidence/stage6_nonvacuity.sh`
- `evidence/stage6_nonvacuity.log` (outer command exit 0)

## 7. Proven-versus-assumed accounting

### Formally established

Under the freshly built candidate definition:

1. the exact submitted module term loads the exact submitted body binding and
   reaches the required public call for every K string;
2. that exact body call, from the loader-produced binding, has partial-correct
   result `intVal(#vowels(S))` for every K string and restores arbitrary caller
   env/stack/continuation; and
3. the recursive equations for `#vowels` characterize ordinary vowels plus a
   final `y/Y`.

C01 and C02 compose to the real submitted program. `#Top`, differential
testing, and prose are not substituted for one another: the K proof establishes
the reachability theorem, while testing supports only source/semantics bridges.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| K v7.1.293 compiler, LLVM/Haskell backends, and reachability prover | All rewriting and proof closure | Standard foundational toolchain trust. |
| Imported K `Bool`, `Int`, `String`, `Map`, and `List` domains | Guards, arithmetic, Unicode length/slicing/equality, bindings, and stack | Accepted low-level primitives; concrete Unicode boundaries were also tested. |
| Trusted `py2mpy.py` | Python-AST to submitted constructor tree | Launcher-trusted artifact; fresh output is byte-identical. |
| Candidate’s generated minimal semantics | Meaning of every submitted constructor | Audited rule-by-rule; exact reachable operations are sound. It is not claimed to model unused Python. |
| `#entry` harness | Selects `vowels_count` and supplies the configured string | Explicit external invocation convention, confirmed by exact loader claim. |
| Natural-language meaning of `#vowels` | Summary-to-contract bridge | Direct mathematical reading of exhaustive equations; independently compared with canonical on 114,036 nonempty cases. |
| Canonical empty behavior | Boundary-domain alignment | Canonical raises; candidate and count formula return 0. Recorded as a non-fatal extension/ambiguity, not hidden. |

There are no opaque symbols, fresh result variables, empirical operational
oracles, task-answer rules in the semantics, or unproved program-body summaries.

### Gates and excluded behavior

- Gate A, real-program soundness: **PASS**.
- Gate B, intent adequacy over strings representing non-empty words: **PASS**.
  The formal theorem additionally covers empty input with result 0.
- Gate C, trust/evidence auditability: **PASS with the named generated-semantics
  limitations**.

Not proved or claimed: termination as a separate theorem; behavior on non-string
Python values; general Python rebinding, arbitrary subscripts, exceptions,
multiple arguments, closures, heap objects, or any unused construct. These are
outside the submitted program and do not narrow the HumanEval word domain.

The proof is therefore result-constraining, body-sensitive, and pinned to the
real generated program, with no material adequacy gap. The minimal semantics’
over-broad rule surfaces and empty-string canonical discrepancy warrant a
legitimate-but-concerning classification, not failure.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
