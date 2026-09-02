# Independent adversarial audit: 132-is-nested

The candidate reconstructs successfully and its theorem has the right
unbounded bracket-string domain, but it is not a legitimate proof. The fatal
defect is the installed priority-40 `proved-scan-loop` operational rule in
`/candidate/verification.k:74`: the bridge-free helper theorem proves the loop
only with exact global and builtins scopes, whereas the installed rule changes
those cells to arbitrary `_REST:Map`. A ground state in that broader match
domain produces `false` under the supplied semantics and `true` under the
bridge. This is a concrete false-conclusion witness, not merely a missing test
or an informal concern.

All candidate and generation artifacts were treated as untrusted. Builds,
proofs, mutations, and tests used fresh definitions below
`/tmp/audit-work`. Reviewer artifacts and bounded logs are in
`/audit-output/evidence`; the exact command index is
[`evidence/COMMANDS.md`](evidence/COMMANDS.md).

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `132-is-nested`;
- condition `semantics`;
- record layout `legacy-selected-stage1`;
- semantics mode `SUPPLIED_SEMANTICS`;
- a mounted supplied semantics at
  `/reference/reference-semantics`.

This is internally consistent: the trusted supplied-semantics mount exists, so
there is no rendered-mode contradiction and no infrastructure stop condition.

The independent checker
[`evidence/provenance_check.py`](evidence/provenance_check.py) read the
launcher-owned container paths rather than the host-only provenance paths. Its
status-0 log is [`evidence/01-provenance.log`](evidence/01-provenance.log).
It established:

- `/audit-campaign-lock.json` is exactly equal as parsed JSON to the
  `audit_campaign` block in `/audit-input.json`; its direct SHA-256 is the
  recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- All records required for `legacy-selected-stage1` are readable regular
  mounts: `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `prompt.txt`, and the structured trace. `usage.json` is present and was also
  inspected. Historical runtime metrics are not required for this layout.
- Every recorded direct-file digest checked by the script matches, including
  the run/task/result/invocation records, prompt, usage, metrics, generation
  output, canonical source, translator, and campaign lock.
- The one structured trace file has the generation-result-recorded digest,
  contains 695 valid JSONL records, and its independently recomputed workspace
  tree digest matches `usage.json`.
- The candidate workspace independently hashes to
  `5f4b7b31bc51511eef0e9b7c51b5a5bdca3825ddaa8491fd6eaa9f90dc9f21a9`,
  matching the retained generation workspace digest.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
  `/candidate/py2mpy.py` is byte-identical to
  `/reference/py2mpy.py`.
- Recursive path, type, mode, size, digest, and byte comparison found no
  missing, additional, changed, mistyped, linked, or special entry between
  `/candidate/reference-semantics` and the trusted
  `/reference/reference-semantics`. The independently recomputed workspace
  digest of both trees is
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  matching the recorded manifest digest.
- The whole candidate and both semantics trees contain only regular files and
  directories; no symlink is present.

The generation evidence was read only as history. It reports a successful
candidate run and prior `#Top` outputs, but none of those claims was used as
proof evidence. There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

`/reference/prompt.py` requires `is_nested(string)` for a finite string
containing only square brackets. It returns `True` exactly when there are
indices `i < j < k < l` whose characters spell `[[]]`; equivalently, there is
a valid bracket subsequence containing nesting.

`/reference/canonical.py` records all opening and closing positions, reverses
the closing positions, greedily pairs an opening with a later closing, and
returns whether at least two such nested pairs exist.

`/candidate/solution.py` uses a state in `0..4`: the first two opening brackets
advance it to 2, and the first two later closing brackets advance it to 4.
It returns `state == 4`. This is a different but extensionally equivalent
subsequence scan on the stated domain.

### Trusted regeneration

The scratch command

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

used the trusted mounted translator and returned statuses 0 and 0. Both `.mpy`
files have SHA-256
`2ae25652f4b8334470ad0f669458c35757c408e5fd85fe6219197da365bf9c9c`.
See [`evidence/02-regeneration.log`](evidence/02-regeneration.log).

### Independent differential evidence

[`evidence/differential_test.py`](evidence/differential_test.py) imports the
trusted canonical and generated entry points independently. It also uses a
regex subsequence oracle, cross-checked against a literal four-index oracle on
all strings through length 8. The final status-0 run covered:

- all six documented examples;
- 19 explicit empty and state-transition boundary cases;
- all 32,767 bracket strings of lengths 0 through 14;
- 2,000 deterministic generated strings, seed 132, at lengths through 512;
- five structured strings through length 4,096.

All 34,797 comparisons agreed. The authoritative log is
[`evidence/03-differential-final.log`](evidence/03-differential-final.log).
Two earlier retained reviewer-development logs contain an incorrect expected
value for a long alternating string; the correction is documented in
`evidence/COMMANDS.md` and is not a candidate mismatch.

Program fidelity passes.

## 3. Clean proof reconstruction

No candidate definition or cache was copied. The scratch source tree contains
only the candidate source proof files, trusted source inputs, and a fresh copy
of the trusted supplied semantics. The available independent toolchain is K
v7.1.293; see [`evidence/04-toolchain.log`](evidence/04-toolchain.log).

### Concrete build and execution

The supplied semantics compiled afresh with LLVM:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

This exited 0
([`evidence/06-kompile-llvm.log`](evidence/06-kompile-llvm.log)).
The reviewer concrete harness contains an AST-identical copy of the submitted
function plus documented and boundary assertions; AST identity is recorded in
[`evidence/05-concrete-harness-fidelity.log`](evidence/05-concrete-harness-fidelity.log).
Trusted translation and `krun` exited 0 with `.K`, `NoExc`, and exit code 0
([`evidence/07-krun-concrete.log`](evidence/07-krun-concrete.log)).

### Positive proof claims

The base Haskell definition compiled afresh with status 0
([`evidence/08-kompile-proof-base.log`](evidence/08-kompile-proof-base.log)).
The helper loop claim independently exited 0 and printed `#Top`
([`evidence/09-kprove-loop.log`](evidence/09-kprove-loop.log)).

The definition containing the installed loop rule also compiled afresh with
status 0
([`evidence/10-kompile-proof-lemma.log`](evidence/10-kompile-proof-lemma.log)).
Each entry claim was then selected and run separately:

- `IS-NESTED-TOP-SPEC.empty-input`: exit 0, `#Top`
  ([`evidence/11-kprove-empty.log`](evidence/11-kprove-empty.log));
- `IS-NESTED-TOP-SPEC.all-bracket-strings`: exit 0, `#Top`
  ([`evidence/12-kprove-universal.log`](evidence/12-kprove-universal.log)).

Thus verification under the candidate-supplied theory reconstructs. These
successes do not establish that every added rule is sound; Stage 5 finds that
one is not.

## 4. Adequacy and real-program pinning

### Formal claims in plain language

1. `scan-loop` in `/candidate/spec.k:6`:
   for every `BSeq BS` and integer `I` with `0 <= I <= 4`, start at the exact
   function-loop configuration with state `I`, execute the remaining encoded
   bracket sequence, execute the real return statement, and pop the exact
   call frame. The resulting Boolean must equal
   `scanState(I, BS) == 4`. The local scope is deleted, the caller environment
   and allocation counter are restored, and the empty heap, return, exception,
   exit, and stack cells are pinned.
2. `empty-input` in `/candidate/spec.k:37`:
   from the exact initial entry environment, calling the submitted binding on
   the empty encoded string returns `false`, with every other observable cell
   unchanged.
3. `all-bracket-strings` in `/candidate/spec.k:52`:
   for every freely generated finite `BSeq`, calling the submitted binding on
   its code encoding returns `nested(BS)`, exactly
   `scanState(0,BS) == 4`. There is no finite-size restriction or hidden
   precondition.

The postconditions are direct equalities to concrete or recursively defined
Boolean results. They contain no free right-hand-side result, tautological
implication, or one-way property.

### Satisfying states and substitutions

The preconditions are satisfiable. Examples include:

- empty entry: the exact cells printed in the claim;
- universal entry: `BS = bNil`;
- helper loop: `I=0`, `BS=bNil`,
  `_CHAR=str(.IntSeq)`, and
  `_INPUT=str(bCodes(bNil))`, with the exact global/builtins maps.

[`evidence/claim_witnesses.py`](evidence/claim_witnesses.py) substitutes empty,
positive, negative, and state-boundary instances. Its status-0 output
([`evidence/14-claim-witnesses.log`](evidence/14-claim-witnesses.log)) agrees
with both Python implementations.

### Mechanical body pinning

The entry claims place `isNestedClosure` directly in scope rather than first
executing the whole `Module(FuncDef(...))`. This is permitted only if that
factoring is inert. The following chain establishes it:

1. trusted regeneration is byte-identical to submitted `solution.mpy`;
2. [`evidence/source-pinning-spec.k`](evidence/source-pinning-spec.k) equates
   `scanBody` and `isNestedClosure` to the exact function parameters, defining
   environment, statements, nested conditionals, calls, and return constructors
   in that regeneration;
3. both configuration-wrapped constructor claims exit 0 with `#Top`
   ([`evidence/13b-kprove-source-pinning.log`](evidence/13b-kprove-source-pinning.log)).

A reviewer body-sensitivity mutation changes the code point tested by the
executed `scanBody` from 91 to 93; it does not merely edit an external source
file. The mutant definition builds successfully
([`evidence/16-kompile-body-mutant.log`](evidence/16-kompile-body-mutant.log)).
The source-pinning proof then fails with a residual containing code point 93
([`evidence/17-kprove-body-mutant-pinning.log`](evidence/17-kprove-body-mutant-pinning.log)),
and the universal proof fails on the concrete symbolic input `[[]]`
([`evidence/18-kprove-body-mutant-universal.log`](evidence/18-kprove-body-mutant-universal.log)).

The claim scope, contract domain, result constraint, and immutable-program
pinning are adequate. The failure below is theory soundness, not theorem
vacuity or domain narrowing.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`evidence/inventory_k.py`](evidence/inventory_k.py) generated
[`evidence/rule-inventory.tsv`](evidence/rule-inventory.tsv), a 953-record
inventory containing:

- all 695 supplied semantic rules;
- all 227 supplied syntax declarations;
- the supplied configuration and five contexts;
- all 13 proof-local rules and all nine proof-local syntax declarations;
- all three reachability claims.

It records every function/total declaration, opaque or no-evaluator symbol,
priority attribute, ordinary operational rule, equational or macro rule,
context, and claim. Direct counts match the source. There are no
`[functional]` declarations and no simplification rules. The full
declaration-by-declaration decisions, state footprints, and used-constructor
mapping are in
[`evidence/proof-extension-review.md`](evidence/proof-extension-review.md).

The candidate's three body/closure definitions are exact definitional
summaries. `BSeq` is a free unbounded datatype. The three `bCodes` iterator
rules are disjoint and exhaustive on that datatype, yield exactly ASCII codes
91 and 93, preserve the continuation and cells, and do not displace any fixed
rule because `bCodes` is a fresh constructor. `openStep`, `closeStep`,
`scanState`, and `nested` are truthful, structurally terminating, exhaustive,
and non-overlapping.

All 25 supplied opaque/symbol declarations are in unused MD5, float, and sort
paths. No candidate opaque symbol influences control or result. The material
program path uses the supplied configuration, lookup, call, binding,
assignment, `For`, iterator, `If`, integer comparison/addition, `ord`, return,
and pop rules. Those operations and every affected cell are mapped in the
static-review artifact.

### Unsound installed operational bridge

The helper theorem and installed rule are not the same theorem:

- `/candidate/spec.k:6-31` proves the loop under the exact scope map containing
  local scope 1, global scope 0 with the real `is_nested` closure, and scope -1
  equal to `builtinsScope`.
- `/candidate/verification.k:74-115` installs a priority-40 rewrite with the
  local scope plus arbitrary `_REST:Map`.

No bridge-free universal connection theorem covers the installed rule's
complete domain. In particular, `_REST` may change name binding for `ord`,
remove parents, or supply other scopes. Priority makes the bridge preempt the
real lookup, calls, loop control, return, and frame pop; priority does not
justify their replacement.

### Required false-conclusion witness

[`evidence/bridge-witness-spec.k`](evidence/bridge-witness-spec.k) uses a
ground state satisfying the installed rule:

- `I = 2`, satisfying `0 <= I <= 4`;
- `BS = bClose(bClose(bNil))`, an intended-domain suffix of two closing
  brackets;
- the exact loop body, return continuation, frame, empty heap, and no
  exception;
- `_REST` contains global scope 0 where `ord` is a normal source-language
  closure that returns integer 91, plus the standard builtins scope.

Under fixed semantics, normal lexical lookup calls that global closure for
each `]`. Both characters therefore take the opening branch. From state 2 the
state remains 2, so the real return is `false`. The bridge-free ground claim
proving this exits 0 with `#Top`
([`evidence/20-kprove-bridge-witness-fixed.log`](evidence/20-kprove-bridge-witness-fixed.log)).

The installed rule ignores the admitted binding and rewrites the same state to
`scanState(2,bClose(bClose(bNil))) == 4`, which is `true`. The
bridge-enabled ground claim proving that opposite result also exits 0 with
`#Top`
([`evidence/21-kprove-bridge-witness-extended.log`](evidence/21-kprove-bridge-witness-extended.log)).

This witnesses a false partial-correctness conclusion enabled by the rule over
an intended-domain bracket input. The target entry path happens to carry the
narrow exact scopes, but that does not validate a globally false rule:
`validating-proof` Gate A explicitly requires every bridge match to fall within
its justification and rejects off-path false equations/rules. The candidate
would need to narrow `_REST` to the exact proved scopes or provide a genuinely
universal, binding-sensitive connection proof.

Static soundness therefore fails.

## 6. Fresh non-vacuity test

The candidate supplied no trusted vacuity result. The reviewer created
[`evidence/spec-vacuity.k`](evidence/spec-vacuity.k), changing the realizable
empty-input result from `false` to `true`.

The mutation is syntactically and definition-compatible: `kprove --dry-run`
exited 0 and emitted the backend proof command
([`evidence/22-vacuity-dry-run.log`](evidence/22-vacuity-dry-run.log)).
The actual proof exited 1 with `WarnStuckClaimState`; the residual computation
is `false` while the destination requires `true`
([`evidence/23-kprove-vacuity.log`](evidence/23-kprove-vacuity.log)).

This is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash. Non-vacuity passes. It shows that the
claims discriminate results; it does not make the over-broad bridge sound.

## 7. Proven versus assumed accounting

### What the successful reachability runs establish

Under the candidate's compiled theory:

- the bridge-free helper claim characterizes the exact loop/return execution
  as `scanState(I,BS)==4` for all `BSeq` and all `I` in `0..4`;
- the empty entry returns `false`;
- the universal entry returns `nested(BS)` for all finite bracket encodings.

The statement is materially adequate to the HumanEval contract, and the
constructor/source bridge is pinned. However, the universal entry proof uses
the installed loop rule. Because that theory can prove the false ground
conclusion in Stage 5, `#Top` in that theory is not a sound proof of the real
program.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, compiler, Haskell/LLVM backends, and builtin integer/Boolean/string hooks | All builds, executions, and proofs | Ordinary toolchain trust; acceptable and version-recorded. |
| Supplied MPY semantics | Defines the selected execution model for every claim | Condition-authorized baseline; candidate copy is exact. Its ASCII string model fully covers `[` and `]`. Deliberately partial/opaque unused modules do not affect this program. |
| Trusted `py2mpy.py` | Connects `solution.py` to `solution.mpy` | Acceptable: trusted mount, byte-identical candidate copy, and exact regeneration. |
| Direct closure factoring | Entry claims omit module loading and install the function closure | Acceptable in isolation: machine-checked constructor pinning and body-sensitivity evidence cover binding, body, parameters, and defining environment. |
| `BSeq`/`bCodes` representation | Quantifies over all finite bracket strings and supplies iterator observations | Acceptable proof-domain encoding: free constructors are unbounded, equations are exhaustive/disjoint, and codes are exactly 91/93. Differential tests are finite support, not the universal proof. |
| Trusted canonical and natural-language equivalence | Connects `nested(BS)` to the human-facing subsequence contract | Ordinary mathematical argument plus broad independent finite evidence; no observed mismatch. |
| Supplied opaque symbols (`md5hexCodes`, float primitives, `sortVS`, `sortKeyVS`, etc.) | None: unreachable from the submitted body and claims | Inert for this theorem; explicitly inventoried. |
| Candidate `proved-scan-loop` bridge with arbitrary `_REST` | Closes the universal entry proof by replacing loop, return, and frame-pop execution | Illegitimate. It exceeds its connection theorem and has a machine-checked fixed-versus-extended opposite-result witness. |
| Candidate generation report, prior logs, tests, and `#Top` | Historical claims only | Not trusted and not used in place of reconstruction or validation. |

### Gate and benchmark decision

- Real-program/extension soundness (Gate A): **fail**, due to the falsified
  operational bridge.
- Intent adequacy (Gate B considered independently): pass; the claim is
  unbounded and matches the bracket-only source contract.
- Evidence/non-vacuity: the audit evidence is reproducible and the false
  postcondition is rejected, but these later facts cannot cure Gate A.

The decision boundary requires `FAIL / NOT_LEGIT` for a proof relying on a
materially unsound proof rule. This is not an infrastructure uncertainty, a
timeout, or merely a thin evidence limitation.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
