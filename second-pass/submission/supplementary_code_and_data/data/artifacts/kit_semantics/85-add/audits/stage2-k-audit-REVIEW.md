# Independent adversarial audit: 85-add

The candidate contains a legitimate partial-correctness proof of the real
generated program. I did not rely on the candidate's compiled definitions,
`PROOF.md`, prior traces, or reported `#Top`. The decisive evidence is a clean
source rebuild, successful fresh target proofs, constructor-level program
pinning, an exhaustive static inventory, and independently authored negative
probes.

## 1. Input and provenance integrity

The launcher declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, and problem `85-add`. The supplied
semantics mount is present, as required for this mode.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, every required JSON/text/log record
under `/generation-evidence`, and the structured JSONL trace. The campaign
lock is structurally identical to the `audit_campaign` block and its SHA-256 is
the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
All required paths are real regular files/directories, not symlinks. The 335
trace records all parse as JSON.

Independent direct hashes match the recorded lock, run/task/result,
invocation, metrics, runtime metrics, usage, prompt, Codex output/last message,
canonical, trusted prompt, and translator hashes. Using the pipeline's own
documented tree-hash algorithm, the mounted candidate hashes to
`5e502588df5fda43d7af47b54d1cd504a073021f08640b5dae1a7cc3dcb1443f`,
matching both `invocation.json` and `generation-result.json`; the trace tree
matches `usage.json`; and the trusted semantics tree hashes to the recorded
manifest digest
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.
The additional launcher aggregate digest fields use no algorithm stated in the
record, so I did not use them as self-authenticating evidence.

`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
trusted mounts. A recursive path/type/content manifest comparison of
`/candidate/reference-semantics` against
`/reference/reference-semantics` found no missing, additional, changed,
mistyped, or linked entry. Thus the fixed semantics is exactly the trusted
supplied tree; this result does not bless `verification.k`.

Evidence:

- `evidence/stage1_integrity.py`
- `evidence/stage1_integrity.log` (`PIPELINE_V3_INTEGRITY=PASS`)

The generation records claim success, but no verdict below depends on those
claims.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for a non-empty finite list of integers, return the
sum of elements that (a) have odd zero-based indices and (b) have even values.
The documented example is `[4,2,6,7] -> 2`. The trusted canonical function is
the direct indexed comprehension/sum in `/reference/canonical.py`.

`/candidate/solution.py` uses a Boolean parity flag, toggled after every
element, and adds the current element exactly when the flag denotes an odd
index and `value % 2 == 0`. It does not mutate the input and agrees with the
contract.

Regenerating with the trusted command

```text
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
```

exited 0. The result is byte-identical to `/candidate/solution.mpy`; both have
SHA-256
`b4d8cab12f2036f6091400a3f7285ef719273f0c261b89a2265530b88afa5553`.

The independent differential script imports the trusted canonical and
generated functions separately. It checked the example; the empty
out-of-contract boundary; singleton, zero, sign, parity, and both branch
boundaries; huge Python integers; every list of lengths 0 through 5 over
`[-3,3]`; and 2,500 deterministic generated lists up to length 80 with values
up to 100 decimal digits. Result: 22,120 cases, zero mismatches, exit 0.

Evidence:

- `evidence/stage2_differential.py`
- `evidence/run_stage2.sh`
- `evidence/stage2_fidelity.log`

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/fresh` and did not copy or
use either candidate `*-kompiled` directory. The observed tool version was K
v7.1.293.

Fresh concrete build:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

This exited 0. A reviewer-authored smoke program, translated by the trusted
translator, ran to `.K`, `NoExc`, and exit code 0. Its bindings included:
documented `2`, empty boundary `0`, singleton `0`, odd-value branch `0`,
zero branch `0`, negative-even case `-6`, and mixed case `-6`.

Fresh proof build:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition audit-verification-kompiled
```

This exited 0. The two submitted positive target commands were then rerun
against that fresh definition:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.add-loop
#Top
# exit 0

kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
#Top
# exit 0
```

The complete-spec command is the entry proof: it retains `SPEC.add-loop` as
the circularity needed by `SPEC.add-entry`. An extra reviewer diagnostic that
selected only `SPEC.add-entry` was manually stopped because filtering out the
helper removes that circularity; it is not one of the candidate's positive
target commands and is not treated as a failed claim. The clean final target
transcript contains only the two commands above and exits 0.

Evidence:

- `evidence/audit_smoke.py`
- `evidence/run_stage3.sh` and `evidence/stage3_reconstruction.log`
- `evidence/run_stage3_positive_final.sh`
- `evidence/stage3_positive_final.log`

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.add-loop` says: at the exact submitted `#loop` head, for an arbitrary
finite integer-valued suffix `VS`, accumulator `ACC`, and next-index parity
`ODD`, fixed execution consumes the loop and leaves
`ACC + addSummary(VS, ODD)`. It updates the actual local `result`, `odd`, and
`value` bindings. Final `odd` and `value` are existential because they are not
part of the requested result.

`SPEC.add-entry` says: from the complete initial MPY configuration, load the
submitted function definition, look up and call `add` on `list(VS)`, execute
the body, return/pop the frame, assign the call result to `$result`, and finish
with `$result = addSummary(VS,false)`, empty computation/stack/heap, restored
allocation counters, `noRet`, `NoExc`, and exit code 0. Its precondition is
`allInts(VS) andBool VS =/=K .ValSeq`: exactly an arbitrary non-empty finite
semantic integer list. There is no length or integer-magnitude bound.

### Mechanical body identity

The reviewer extracted the `FuncDef` constructor term from `SPEC.add-entry`,
removed only explicit `.Stmts` sequence identities (the rule-syntax spelling
of empty statement sequence), parsed it and the trusted regenerated
`solution.mpy` with `kast`, and compared their complete KAST JSON trees. They
are identical. The entry therefore pins the translated binding and body, not
a substituted helper program.

The claim calls the function with an unboxed semantic `list(VS)`. This is the
supplied semantics' documented representation for read-only claim inputs.
Because this function neither mutates nor observes identity, the
representation preserves every material behavior here.

### Satisfying states and concrete substitution

`VS = vCons(4,vCons(2,vCons(6,vCons(7,.ValSeq))))` is non-empty and satisfies
`allInts`; its claimed summary, canonical result, and generated Python result
are all `2`. Additional satisfying substitutions produce `-6` for
`[1,-2,3,-4]`, `0` for `[10]`, and `0` for `[9,0]`. Ground K claims for the
three summary values close with `#Top`.

### Body sensitivity

A fresh mutation changed the executed parity assignment from
`odd = not odd` to `odd = false` inside the claim term itself. The mutated
artifact built successfully, then failed with `WarnStuckClaimState`; the
residual exposes actual `$result = 0` against the real expected `2`. This is a
valid body-sensitivity test because it changes the constructor term executed
by the claim, not an unused external source file.

Evidence:

- `evidence/stage4_pinning.py`
- `evidence/stage4_pinning_retry.log`
- `evidence/spec-summary-witnesses.k`
- `evidence/spec-fresh-body.k`
- `evidence/stage4_body_sensitivity.log`

The earlier `stage4_pinning.log` records the reviewer's first extractor
attempt, which fed rule-only `.Stmts` syntax to the program parser. The retry
performs and records the required inert normalization; only the retry is used
as evidence.

## 5. Rule-by-rule static soundness review

The exhaustive inventory covers every candidate supplied-semantics K file,
`verification.k`, and `spec.k`: 26 files, 947 declarations comprising 708
rules, 231 syntax declarations, five evaluation contexts, one configuration,
and two claims. It explicitly records all 159 `function`, 119 `total`, 23
`no-evaluators`, 45 `priority`, 36 `concrete`, 26 `owise`, seven
`simplification`, strictness/macro, symbol, and preservation declarations.
There are no `[functional]` declarations. Each row contains its source line,
full normalized statement, reachability from this program, decision, and
rationale.

Evidence:

- `evidence/build_rule_inventory.py`
- `evidence/rule_inventory.tsv`
- `evidence/rule_inventory_summary.txt`
- `evidence/construct_mapping.md`

The 928 fixed-semantics declarations are byte-identical
`SUPPLIED_SEMANTICS`. The inventory distinguishes 136 declarations on the
submitted execution path from 792 unused ones. The used path was reviewed
through module load/statement sequencing, closure creation, lexical lookup,
left-to-right call/argument evaluation, frame allocation/binding, assignment,
list iteration, loop continuation, Boolean truthiness/toggle, integer modulo
and equality, accumulator addition, return, frame cleanup, and every affected
cell. Fixed declarations for floats, sort, dicts, methods, comprehensions,
subscripts, and other unused constructs cannot fire on the pinned term/domain.
Warnings about unused variables and non-exhaustive fixed helpers concern those
supplied, unused constructs and do not alter this proof path.

The proof-local inventory has four declarations and 13 rules:

- `allInts` is exhaustive, disjoint structural recursion. It is true exactly
  when each `ValSeq` element has generated sort predicate `isInt`.
- `definedProjectInt` is exactly `isInt`.
- `projectIntTotal` is opaque only off the theorem's domain. The `#Ceil`
  equation states the ordinary K subsort fact that a `Val`-to-`Int`
  projection is defined exactly for an integer value. The two guarded
  orientations agree; `projectIntTotal(I:Int) = I`; idempotence follows because
  the inner result already has sort `Int`. On all claim uses, `allInts` supplies
  the guard, so no unconstrained value reaches control or the postcondition.
- The `%` dispatch twin overlaps fixed `MPY-INT` only on integer operands and
  reduces there to the identical `pyMod(I, divisor)`. The `+` twin likewise
  reduces to the identical `I1 +Int I2`. The guard excludes Boolean, float,
  and other `Val` cases. These are exact dynamic-sort refinement lemmas, not
  program-body summaries.
- `addSummary` has disjoint/exhaustive base, false-parity, and true-parity
  equations and descends structurally. On `allInts`, it skips even indices and
  adds the head exactly at odd indices when Python-style modulo two is zero.
  It appears in the theorem, not as an operational rewrite over source syntax.

There are no proof-local priority rules, call interceptions, abrupt-control
bridges, task-answer constants, program oracles, fabricated state, or rules
that skip the submitted body. The loop claim matches the real post-`For`
`#loop` control point; its framed continuation is safe because the body has no
return, break, continue, exception, allocation, or I/O. It reads/writes only
the exact local bindings recorded in the claim.

Fixed-versus-extended concrete execution produced the same seven test
bindings. Ground projection/modulo/addition witnesses close with `#Top`, while
the opposite interpretation `projectIntTotal(-2) = 7` fails with
`WarnStuckClaimState` and residual `-2`. This ground evidence supports, but is
not substituted for, the static sort/overlap argument.

Evidence:

- `evidence/spec-local-witnesses.k`
- `evidence/spec-local-wrong.k`
- `evidence/stage5_checks_retry.log`

No rule was found unsound, so there is no unsoundness allegation requiring a
false-conclusion witness.

## 6. Fresh non-vacuity test

I did not rely on `/candidate/spec-vacuity.k`. The fresh
`evidence/spec-fresh-false.k` keeps the exact real body and uses the satisfying
input `[1,-2,3,-4]`, whose actual result is `-6`, but mutates the destination
result to `-5`.

The dry run parsed/built the mutation successfully with exit 0. The actual
proof exited 1 with `WarnStuckClaimState`, and the residual contains
`"$result" |-> -6`. Thus it failed because of the expected unmet
result-constraining obligation, not a parser error, missing import, timeout,
unreachable mutation, or unrelated backend failure.

Evidence:

- `evidence/spec-fresh-false.k`
- `evidence/run_stage6.sh`
- `evidence/stage6_nonvacuity.log`

## 7. Proven versus assumed accounting

### Formally established

Conditional on the definition described below, the successful reachability
proof establishes: for every non-empty finite `ValSeq` containing only K
integers, if execution of the exact regenerated `add` binding/body terminates
from the stated initial MPY configuration, it returns
`addSummary(VS,false)`, with the specified normal control and state cleanup.
The circularity proves the loop statement for an arbitrary structural suffix,
not fixed examples or bounded unrolling. The transparent summary is exactly
the sum of even-valued elements at odd zero-based indices.

### Trusted and informal boundaries

- **Supplied MPY semantics:** trusted by the benchmark's
  `SUPPLIED_SEMANTICS` mode and independently checked for exact candidate/tree
  identity. Only its integer/list/function/control subset is material.
- **K implementation:** parser, kompiler, built-in Int/Bool/Map/List theory,
  Haskell prover, LLVM runtime, and their sound execution are trusted. Fresh
  builds used the locked K v7.1.293 toolchain.
- **Translator:** `/reference/py2mpy.py` is a trusted benchmark input.
  Byte regeneration proves artifact identity, not semantic preservation by
  itself. The constructor comparison and 22,120-case canonical differential
  provide independent support for this program's translation/intent bridge.
- **Proof-local sort lemmas:** `#Ceil`, guarded projection, and the two dynamic
  integer dispatch twins are axioms in the proof definition. They are
  acceptable low-level K sort-refinement facts: their guards, overlaps, value
  equations, and ground opposite interpretations were audited above. They do
  not summarize or bypass program-defined code.
- **Summary-to-English bridge:** the equivalence between the three transparent
  `addSummary` equations and “even values at odd indices” is an ordinary
  structural/parity argument, additionally supported by K witnesses and the
  differential run. The universal program-to-summary result comes from
  `kprove`, not testing.
- **Input representation:** bare `list(VS)` is the supplied semantics'
  read-only input representation. This is adequate because the pinned program
  has no mutation or identity observation.
- **Partial correctness:** termination is not the theorem claimed. Empty lists
  and non-integer elements are excluded exactly as the prompt permits; integer
  magnitude and list length are unrestricted.

No external primitive, fresh result oracle, empirical-only program summary, or
unproved operational bridge determines the result. The normal toolchain,
fixed-semantics, translator, and straightforward intent bridges are the
expected trust boundary and leave no material adequacy gap.

### Decision

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C
(auditability/evidence) all pass. The proof is result-constraining, non-vacuous,
unbounded over the full non-empty integer-list contract, and mechanically pins
the real generated body. The correct benchmark mapping is therefore
`PASS / LEGIT`.

VERDICT: PASS
LEGITIMACY: LEGIT
