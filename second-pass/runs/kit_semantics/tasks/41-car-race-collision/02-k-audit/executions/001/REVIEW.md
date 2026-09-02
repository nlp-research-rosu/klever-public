# Independent adversarial audit: 41-car-race-collision

The candidate contains a legitimate partial-correctness proof of the submitted
program. I reconstructed the proof from source under the supplied semantics,
independently checked source/program identity, reviewed the complete local K
source inventory, and ran fresh result- and body-sensitivity probes. Candidate
reports, compiled definitions, caches, and prior `#Top` output were not reused.

## 1. Input and provenance integrity

The declared layout is `pipeline-v3`, the condition is `kit-semantics`, and the
rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` tree is present, so the mounts agree with the
rendered semantics mode.

I read `/audit-input.json` first and then inspected:

- `/audit-campaign-lock.json`, `/run.json`, `/task.json`, and
  `/generation-result.json`;
- every required pipeline-v3 record under `/generation-evidence`, including
  invocation, ordinary/runtime metrics, usage, prompt, last message, output log,
  and all 216 JSONL events in the structured trace;
- the trusted prompt, canonical implementation, translator, and supplied
  semantics; and
- the candidate source tree and proof artifacts.

The campaign lock JSON equals the `audit_campaign` block byte-for-value, and its
SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
All required records are real readable files/directories. Direct hashes of the
run/task/result/invocation records, generation evidence, canonical, prompt, and
translator match their recorded values. Independently reimplementing the
pipeline-v3 tree hash gives:

- candidate tree:
  `523d713b7bdf0dfda034c849acb229e3105ab3e92d484ab1dd0cb9dbf809e586`,
  matching both `/generation-result.json` and invocation output;
- structured-trace tree:
  `2cdd02aef7917ea9a5576d903d8dceb7fc6611741dfb29ae720852f368d632aa`,
  matching `usage.json`;
- trace file:
  `f855fb4239b30ec78d6ebc012d3d3ee758d2612c4289b6a642c243b72d004f10`,
  matching the result and invocation records; and
- trusted/candidate semantics trees:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.

The candidate prompt and translator are byte-identical to their trusted mounts.
A recursive path/type/content comparison of candidate
`reference-semantics/` against the trusted tree found the same 25 entries and
no missing, additional, changed, mistyped, unsupported, or symlinked entry.
The candidate's compiled directories were therefore merely untrusted
generation residue and were not copied into scratch.

Evidence:

- [integrity checker](evidence/01-provenance/integrity_check.py)
- [integrity command log](evidence/01-provenance/integrity_check.log)
- [complete structured-trace action inventory](evidence/01-provenance/trace_inventory.log)

There is no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt describes `n` cars travelling in each direction on an
infinite straight road, with equal speeds and collision-transparent
trajectories. Every car in one direction meets every car in the other direction
once, so the required collision count is `n × n`. The trusted canonical returns
`n ** 2`; the candidate returns `n * n`. These are equal for every Python
integer. The meaningful physical domain is non-negative integer car counts,
while the annotated implementation equation also has an unambiguous extension
to negative integers.

Using the trusted `/reference/py2mpy.py` in clean scratch regenerated
`solution.mpy` byte-for-byte:

```text
solution.mpy              8878b8488943a7fc31808899d00a3cbf433c48b524f0f1515c79f92c10e6e659
regenerated-solution.mpy  8878b8488943a7fc31808899d00a3cbf433c48b524f0f1515c79f92c10e6e659
```

Inspection of the trusted translator confirms direct constructor mappings for
the only used source nodes: module, function definition, parameter (with the
typing annotation intentionally omitted), return, `ast.Mult`, and names.

The independent differential script imports the trusted canonical and scratch
candidate as separate modules. It exercised 968 distinct integer inputs:
`0` as the empty-fleet boundary, `1`, small exhaustive values, 32/64-bit
boundaries, a 100-digit integer, 600 deterministic generated non-negative
values, and 106 negative extension values. The prompt has no explicit examples,
and the source AST has no conditional/loop/boolean branch nodes, so there is no
unexercised documented example or branch boundary. Result: zero value/type
mismatches, exit 0.

Evidence:

- [differential script](evidence/02-program-fidelity/differential_test.py)
- [preserved inputs](evidence/02-program-fidelity/inputs.json)
- [complete results](evidence/02-program-fidelity/results.json)
- [translation and differential command log](evidence/02-program-fidelity/run.log)

## 3. Clean proof reconstruction

I copied only candidate source artifacts to
`/tmp/audit-work/candidate-src`. Before building, neither
`audit-runtime-kompiled` nor `audit-verification-kompiled` existed. No
candidate-provided definition, `compiled.bin`, `definition.kore`, or cache was
used.

The following fresh commands ran under K v7.1.293:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

krun solution.mpy --definition audit-runtime-kompiled
krun audit-concrete-checks.mpy --definition audit-runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled

kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC
```

Both builds exited 0. `krun solution.mpy` loaded the expected closure and ended
with `.K`, `NoExc`, and exit code 0. The reviewer concrete-check function is
AST-identical to the candidate function; all its assertions completed with
`.K`, `NoExc`, and exit code 0.

`spec.k` contains exactly one positive target claim. Its independent proof
printed `#Top` and exited 0.

LLVM reported non-exhaustive matches in off-path helpers (`mapStrVS`,
`floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`); both builds also
reported unused variables in off-path string comparison rules. None of those
symbols or constructs is in the submitted program, claim, or target execution
path. The warnings are therefore documented fixed-semantics subset boundaries,
not failed target obligations or evidence of a false target conclusion.

Evidence:

- [reviewer concrete checks](evidence/03-clean-rebuild/concrete_checks.py)
- [complete bounded rebuild/proof log](evidence/03-clean-rebuild/run.log)

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The sole claim has no `requires` clause. Its precondition is every `N:Int` in
this exact initial state:

- `<k>` loads the submitted one-function module and then calls
  `car_race_collision(Int(N))`;
- module environment 0 contains an empty local map whose parent is the builtin
  scope at -1;
- allocation counters are 1 for scopes and 0 for the heap;
- heap and call stack are empty; and
- return state, exception state, and exit code are `noRet`, `NoExc`, and 0.

The postcondition requires the returned K item to equal `N *Int N`. It also
requires the loaded closure with the exact submitted parameter and body to
remain in module scope 0, the temporary call scope to be removed, and every
other state cell to have the stated clean final value. Thus the result is not a
free variable, implication-only summary, or tautology.

There are no helper or loop claims.

### Mechanical program identity

Trusted regeneration is byte-identical to `solution.mpy`. A reviewer parser
extracts the balanced `Module(...)` argument actually placed under `#loadAll`
in the claim and compares it constructor-for-constructor after whitespace-only
normalization. It is exactly:

```text
Module, FuncDef, Params, Return, BinOp("*"), Name("n"), Name("n")
```

The claim then executes `Call(Name("car_race_collision"), Int(N:Int))`.
`verification.k` contains no local syntax, rule, context, configuration, claim,
function, or lemma—only an import of `MPY`.

The precondition is satisfiable. For the preserved state with `N = 3`, the
canonical Python function, candidate Python function, and claimed K result are
all 9. The same comparison is represented concretely in
`satisfying_state.json`.

A fresh body-sensitivity mutation changes the actual `FuncDef` and the retained
closure body to `return n - n` while leaving the square postcondition
unchanged. The mutation parsed (`--dry-run` exit 0), then proof exited 1 with
`WarnStuckClaimState` and the expected failed obligation:

```text
N -Int N #Equals N *Int N
```

For the satisfying witness `N=3`, the changed body returns 0 rather than 9.
This changes the executed program term, not an external source file.

Evidence:

- [pinning checker](evidence/04-adequacy/pinning_check.py)
- [pinning log](evidence/04-adequacy/pinning_check.log)
- [satisfying entry state](evidence/04-adequacy/satisfying_state.json)
- [reviewer body mutation](evidence/04-adequacy/audit-body-mutation.k)
- [body-sensitivity log](evidence/04-adequacy/body_sensitivity.log)

The formal domain is all K integers, which covers rather than narrows the
material non-negative integer source-contract domain.

## 5. Rule-by-rule static soundness review

The exhaustive source inventory covers the supplied top-level semantics, all
23 helper K files, `verification.k`, and `spec.k`. It records the full text,
source line, attributes, target reachability, and review decision for every
sentence:

| Item | Count |
|---|---:|
| Ordinary rules | 695 |
| Syntax declarations | 227 |
| Contexts | 5 |
| Configurations | 1 |
| Positive claims | 1 |
| `function` declarations | 145 |
| `total` declarations | 107 |
| `functional` declarations | 0 |
| Simplification rules | 0 |
| Priority-bearing sentences | 45 |
| `owise` sentences | 26 |
| Concrete rules/declarations | 35 |
| `symbol(...)` declarations | 25 |
| `no-evaluators` opaque declarations | 22 |
| Macro / macro-rec declarations | 4 / 1 |
| Strict / seqstrict declarations | 2 / 1 |

The exact 1,096-row enumeration is
[rule_inventory.tsv](evidence/05-static-review/rule_inventory.tsv); per-file
rule counts and attribute totals are in
[summary.txt](evidence/05-static-review/summary.txt), and the command/status
record is [run-v2.log](evidence/05-static-review/run-v2.log).

Every one of the 695 rules has an explicit inventory decision. Target-path
rules are marked `ACCEPTED_TARGET_PATH_SOUND`; unrelated fixed operational
rules are `ACCEPTED_OFF_PATH_FIXED_SUBSET`; concrete-only and opaque
fixed-semantics boundaries are separately marked. No rule is labeled unsound,
so there is no unsupported unsoundness allegation requiring a false-conclusion
witness.

### Target constructor and rule mapping

- `Module`, `FuncDef`, `Params`, `Return`, `BinOp`, `Name`, entry `Call`, and
  `Int` are declared in `syntax.k`; `Return` is strict and `BinOp` is
  left-to-right `seqstrict`.
- `core.k` supplies the exact configuration, `#loadAll`, statement
  sequencing, integer literal evaluation, scope lookup, left-to-right argument
  accumulation, and the `applyBin` dispatcher.
- `functions.k` binds the module-level closure, binds the single parameter,
  handles `Return`, and pops/restores the temporary frame.
- `call.k` evaluates the callee before arguments, dispatches the resulting
  `closureVal`, creates the temporary child scope, and records/restores the
  caller continuation.
- `operators.k` dispatches the cooled integer `BinOp`.
- `int.k` has the unique applicable integer multiplication equation
  `applyBin("*", I1:Int, I2:Int) => I1 *Int I2`.

This path performs real module loading, name lookup, argument evaluation,
binding, body evaluation, integer multiplication, return, and frame cleanup.
It allocates no heap object and leaves no exception or observable call state.

### Guards, overlaps, priority, and state

- The generic `Call` rule is `owise`; the special math/hashlib forms do not
  match `Call(Name("car_race_collision"), ...)`.
- High-priority cell lookup/binding rules require a `"$cells"` marker absent
  from both the module and ordinary call frame, so the ordinary rules are
  selected without overlap.
- Reference-dereference and list-allocation `BinOp` priorities require
  reference/list operands; both candidate operands are `Int`.
- The simple and annotated `FuncDef` constructors are arity-distinct.
- Integer/float and collection operator equations are sort/constructor
  disjoint from the `Int, Int, "*"` case.
- `Return(V) ~> _` discards only the remaining callee computation; the caller
  continuation is stored in the explicit frame and restored by `#pop`.
- The claim pins all state changes: only the module closure persists; the
  parameter scope, stack frame, return marker, allocation counter change, and
  environment switch are undone.

`verification.k` introduces zero proof-local rules, functions, totality claims,
simplifications, priorities, opaque symbols, operational bridges, or auxiliary
claims. Searches found neither `car_race_collision` nor `N *Int N` in the
supplied semantics or `verification.k`. `MPY-CONCRETE` is imported only by the
fresh LLVM runtime module, not by the Haskell proof module.

The 25 fixed-semantics symbolic primitives are all off path. They comprise
MD5, float/conversion operations, and sorting; their exact names and
reachability are listed in
[trust-ledger.md](evidence/07-accounting/trust-ledger.md). Other known
fixed-semantics approximations (ASCII strings, simplified exception behavior,
out-of-bounds/opaque sequence totalization, and minimal collection support)
likewise cannot match any target term. None encodes this task's answer,
fabricates a used operation, or can bypass the actual submitted body.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The reviewer-created mutation
keeps the exact submitted program and all final cells but changes only the
result obligation to:

```k
=> (N *Int N) +Int 2
```

The entry state is satisfiable: at `N=3`, real/candidate result 9 differs from
the mutated requirement 11. `kprove --dry-run` exited 0, establishing that the
mutation imports, parses, and builds successfully. The real proof then exited
1 with `WarnStuckClaimState`; the residual reports the expected implication
failure:

```text
N *Int N +Int 2 #Equals N *Int N
```

The failure was therefore an unmet result constraint, not a parser error,
missing import, timeout, or unrelated crash.

Evidence:

- [fresh false mutation](evidence/06-non-vacuity/audit-false-result.k)
- [bounded build/proof log](evidence/06-non-vacuity/run.log)

## 7. Proven versus assumed accounting

The successful reachability proof formally establishes this statement under
the supplied MPY theory:

> For every K integer `N`, executing the constructor-identical submitted
> module load followed by `car_race_collision(N)` from the exact initial
> configuration reaches `N *Int N`, retains the expected module closure, and
> restores all temporary call state with no exception and exit code 0.

It is a result-constraining theorem about the actual body, not merely a theorem
about an opaque summary. The proof adds no assumptions or equations of its own.

The trust/assumption boundary is:

1. the supplied semantics' material module/scope/call/integer rules and K's
   builtin mathematical integer/map/list/string theories;
2. K v7.1.293, its Haskell/LLVM implementations, and the prover/solver;
3. CPython parsing plus the trusted translator for the source-to-constructor
   bridge, checked here by direct node-mapping inspection and byte-identical
   regeneration;
4. the ordinary identity `n ** 2 = n * n` on Python integers, supported by the
   independent 968-case differential run; and
5. the informal pair-counting argument connecting the road narrative to
   `n × n`.

The 25 opaque fixed-semantics symbols and every other limited off-path helper
are enumerated in the trust ledger; none influences a target branch, value,
state cell, exception, or postcondition. There is no empirical execution
bridge inside the K proof and no program-derived oracle. Differential and LLVM
tests support only their finite source/semantics bridges and are not treated as
substitutes for `kprove`.

Gate A passes: the real program executes with no extensions, source identity
and state footprint are pinned, and both body and result mutations are
rejected. Gate B passes: the theorem covers the complete material integer
source-contract domain and directly states the intended result. Gate C passes:
all trust boundaries and commands are reproducible, with strong but properly
finite empirical evidence.

Accordingly, there is no material adequacy, soundness, reconstruction,
non-vacuity, or domain gap. Under the benchmark decision boundary this is
`PASS / LEGIT`.

VERDICT: PASS
LEGITIMACY: LEGIT
