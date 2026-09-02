# Independent adversarial audit: 81-numerical-letter-grade

## Outcome

The candidate's six submitted claims do reconstruct: every isolated positive
`kprove` invocation exits 0 and prints `#Top`. The proof term is also
mechanically pinned to the submitted `solution.mpy`, and a fresh false
postcondition is rejected. Those facts establish that this is not a fabricated
trace or a vacuous theorem.

It is nevertheless not a legitimate proof of the real generated program over
the HumanEval source-contract domain, for two independent material reasons:

1. The generated semantics assigns exact decimal meanings to CPython float
   literals. This is false for non-integer decimal literals and changes a
   reachable result. The exact binary value of Python input float `3.7` is
   `4165829655317709/1125899906842624`, with positive denominator. K compares
   that value against exact `37/10` and returns `"A"`; the trusted canonical and
   submitted Python compare it with the same CPython float literal and both
   return `"A-"`.
2. There is no whole-program entry claim for an arbitrary input list. The only
   entry claims cover an empty list, a singleton, and one fixed five-element
   example. The two symbolic loop claims prove one transition and leave the
   arbitrary tail unprocessed; they do not prove the returned list for that
   tail. Under the benchmark's explicit decision boundary, this material
   restriction of an unrestricted list contract is `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = bare`, and `semantics_mode = GENERATED_SEMANTICS` in
`/audit-input.json`.

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  `/generation-result.json`, every required generation record, the candidate
  tree, trusted prompt/canonical/translator, and structured trace are present,
  readable, regular files or real directories as appropriate. Recursive tree
  inspection rejected symlinks or unsupported entries; none were found.
- The decoded `/audit-campaign-lock.json` object exactly equals the
  `audit_campaign` block. Its independently computed SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  equal to the recorded value.
- Every recorded regular-file digest was reproduced, including the run/task
  manifests, stage result and invocation, metrics, prompt, usage, Codex
  last/output logs, canonical, prompt, and translator. The independently
  recomputed pipeline tree digest of `/candidate` is
  `32fbe42fbf402874bdb4e6f902a4d2d525576c3ab4a00b434c70b55e4b93cfaa`,
  equal to both the invocation and result's retained
  `workspace_sha256`. The independently recomputed trace-tree digest is
  `0023ff0ddc816e25cd471bbf0e3b0359a192a0bd5f71f8ec128c51f33ca314e1`,
  equal to `usage.json`'s `source_trace_sha256`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.
- `/reference/reference-semantics` is absent, as required in generated mode.
  No candidate `reference-semantics` tree is present or was sought.
- The required generation records were read only as untrusted claims. The one
  structured JSONL trace contains 237 valid records (46 tool calls and 46 tool
  outputs among them); the prior positive run and final `KPROVE_PASSED` marker
  were not reused.

The complete mechanical check, hashes, trace counts, and exit 0 are in
[stage1-provenance.log](evidence/stage1-provenance.log), driven by
[provenance_check.py](evidence/provenance_check.py). There is no infrastructure
breach and therefore no basis for `AUDIT_ERROR`.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

For each numeric GPA, in input order, return:

- `A+` exactly at `4.0`;
- otherwise `A`, `A-`, `B+`, `B`, `B-`, `C+`, `C`, `C-`, `D+`, `D`, or `D-`
  at the successive strict lower bounds `3.7`, `3.3`, `3.0`, `2.7`, `2.3`,
  `2.0`, `1.7`, `1.3`, `1.0`, `0.7`, and `0.0`;
- `E` otherwise.

The result is a list of the same length and order as `grades`. Neither
`/reference/prompt.py` nor the canonical implementation bounds the list
length. The canonical also makes values below zero `E` and values other than
exactly `4.0` but above `3.7` `A`.

### Implementation and translation

`/candidate/solution.py` implements the same ordered decision tree as
`/reference/canonical.py`; renamed locals and the docstring do not affect
behavior. Regeneration with the trusted translator produced SHA-256
`a2c515dd246ef12031f0d3a266f7331002216c533423df82fdb0cbb97b75f246`
for both the fresh and submitted MPy files, and `cmp` exited 0
([stage2-translation-success.log](evidence/stage2-translation-success.log)).

The independent test [differential_test.py](evidence/differential_test.py)
imports the trusted and candidate functions from separate paths. It covers the
documented example, empty input, all exact thresholds, both adjacent
IEEE-754 values around every threshold, out-of-range and special float values,
and deterministic generated lists of lengths 1, 2, 5, and 100. Across 21
cases and 170 scalar occurrences, there were zero mismatches
([stage2-differential.log](evidence/stage2-differential.log), exit 0). This
supports Python implementation fidelity; it does not prove the K semantics.

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/reconstruction`; no
candidate-built definition or cache was copied or used. The observed tools are
K `v7.1.293` and Python `3.10.12`
([toolchain.log](evidence/toolchain.log)).

Fresh builds:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition semantic-llvm-kompiled
# exit 0

kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition verification-kompiled
# exit 0
```

The bounded logs are
[stage3-kompile-semantic-llvm.log](evidence/stage3-kompile-semantic-llvm.log)
and
[stage3-kompile-verification-haskell.log](evidence/stage3-kompile-verification-haskell.log).

Fresh LLVM executions terminate with `.K` and the expected result for empty
input, the prompt example, and the full exact-decimal threshold vector:
[empty](evidence/stage3-krun-empty.log),
[example](evidence/stage3-krun-prompt.log), and
[thresholds](evidence/stage3-krun-thresholds.log).

Each positive claim was then selected and run independently:

| Claim | Exit | Output |
|---|---:|---|
| `SPEC.empty-input` | 0 | `#Top` |
| `SPEC.all-single-grades` | 0 | `#Top` |
| `SPEC.loop-step-new-variable` | 0 | `#Top` |
| `SPEC.loop-step-existing-variable` | 0 | `#Top` |
| `SPEC.loop-empty` | 0 | `#Top` |
| `SPEC.prompt-example` | 0 | `#Top` |

The exact command per row was
`kprove spec.k --definition verification-kompiled --spec-module SPEC --claims
SPEC.<label>`. Individual logs are indexed in
[COMMANDS.md](evidence/COMMANDS.md) and contain the command, exit status, and
`#Top`.

### Fresh generated-semantics counterexample

The translator emits `Float(repr(v))` for a CPython float AST constant
(`/reference/py2mpy.py:133-142`). The candidate semantics then asserts
`eval(Float(3.7)) => num(37,10)` (`/candidate/semantic.k:121`). But:

```text
3.7.as_integer_ratio()
= (4165829655317709, 1125899906842624)

4165829655317709/1125899906842624 - 37/10
= 1/5629499534213120
```

The denominator satisfies the claim's `Q > 0` precondition. Fresh K execution
of the actual `solution.mpy` on that exact ratio terminates with
`list(str("A") :: .Vals)`
([stage3-krun-ieee-3.7-witness.log](evidence/stage3-krun-ieee-3.7-witness.log)).
Both independently loaded Python implementations return `["A-"]` on input
float `3.7`
([ieee_bridge_witness.py](evidence/ieee_bridge_witness.py),
[successful output](evidence/stage3-ieee-bridge-python-success.log)).

This is the required concrete false-conclusion witness on the intended runtime
domain. It is not a timeout, rounding speculation, or untested theoretical
concern.

## 4. Adequacy and real-program pinning

### Plain-language claim meanings and satisfying states

- `empty-input`: from empty input and environment, execute the program and
  return/store an empty list. The literal empty initial configuration is a
  satisfying state, confirmed by concrete execution.
- `all-single-grades`: for arbitrary integers `P,Q` with `Q>0`, execute the
  program on the singleton `[P/Q]`, return
  `[expectedGrade(P,Q)]`, and constrain the complete final local environment.
  `P=4,Q=1` is a satisfying witness; K, canonical, and candidate Python all
  produce `A+` in that case. The positive-denominator binary ratio for `3.7`
  is another satisfying witness and exposes the K/Python disagreement above.
- `loop-step-new-variable`: with `grades` and `result` bound and no `grade`
  binding, process one numeric head, insert `grade`, append one expected value,
  and leave `loop(...,REST)`. A witness is `P=4,Q=1`, empty `REST`/`OUT`, and
  `ALL = num(4,1) :: .Vals`.
- `loop-step-existing-variable`: the same single step when `grade` already
  exists. The preceding witness plus old `grade = num(0,1)` satisfies it.
- `loop-empty`: reduce an empty internal loop to `.K`, framing every omitted
  cell. Any well-formed framed cells satisfy it.
- `prompt-example`: execute the program on the exact five given rational
  values and return the hard-coded five grades. Its literal start state is
  satisfying, and both Python implementations agree with the claimed result.

All entry results are constrained by exact cell rewrites; none is a free
right-hand variable, tautology, or one-way implication.

### Program identity

`solutionProgram` is a constructor macro, and `gradingBody` is its one nested
constructor macro. The reviewer expanded both, normalized only K's internal
`.Exprs` empty-list spelling to the concrete external empty spelling, parsed
the expanded term and submitted `solution.mpy` with the rebuilt definition,
and obtained identical KORE SHA-256
`89113720d47ee7302b3496ca13226fb03b2de567550601211336c066efb8cb92`
for both. See [program_term_compare.py](evidence/program_term_compare.py) and
[stage4-program-term-compare-success.log](evidence/stage4-program-term-compare-success.log).

A separate body-sensitivity mutation changed the A+ branch inside the
`gradingBody` actually referenced by `solutionProgram` to append `"WRONG"`.
The mutated definition compiled, while isolated proof of
`all-single-grades` exited 1 with `WarnStuckClaimState` and a final `"WRONG"`
result ([mutated source](evidence/verification-body-mutated.k),
[build](evidence/stage4-body-mutation-kompile.log),
[failed proof](evidence/stage4-body-mutation-kprove.log)). Thus source-to-claim
maintenance is manual, but the immutable submitted theorem is mechanically
pinned and body-sensitive.

### Fatal formal scope gap

No claim starts the actual program on an arbitrary finite `Vals` list and
constrains the final result to a mapped list. `expectedGrades` is defined but
unused. The two loop-step claims end at `loop(...,REST)`, not at `.K` with a
result for `REST`; `loop-empty` only covers the empty internal tail. Proving
those three claims separately establishes a base transition and one-step
transition relation, not a reachability theorem that iterates it for arbitrary
length. The only whole-program lengths proved are 0, 1, and the single fixed
example of length 5.

This materially narrows the HumanEval list domain. Even if the semantics were
repaired, the benchmark explicitly maps such a `SOUND-BUT-LIMITED` theorem to
`FAIL / NOT_LEGIT`.

## 5. Rule-by-rule static soundness review

There are no additional candidate K helper files. The exhaustive inventory,
including every local syntax production, attribute, configuration cell, all
41 rules in `semantic.k`, all 17 rules in `verification.k`, all six claims,
construct coverage, and a decision for each rule is in
[stage5-rule-inventory.md](evidence/stage5-rule-inventory.md). The mechanical
declaration/rule extraction and counts are in
[stage5-static-extraction.log](evidence/stage5-static-extraction.log).
There are no local priority, simplification, concrete, opaque, or functional
declarations.

### Syntax and configuration

The MPy syntax covers every constructor used by the submitted program:
`Module`, `FuncDef`, `Params`, statement sequences, `Expr`, `Assign`, `For`,
the nested `If`s, `Return`, `Name`, `Str`, `Float`, `ListExpr`, `Compare`,
`CmpOp`, `Attribute`, and `Call`. The four cells—computation, input,
environment, and result—are all used. Missing semantics for unused Python
constructs is not charged as a defect in generated mode.

### Exhaustive semantic-rule decisions

- `semantic.k:74-75`: the two `append` equations are truthful, disjoint,
  structurally descending, and total over the free `Vals` datatype.
- `:78-81`: the exact-module entry rule is a direct entry harness, not a task
  oracle. It matches the exact function name/formal, binds the supplied input,
  preserves the continuation, and runs the exact body. It does not model
  general Python function creation/calls, but no material target behavior is
  skipped for this single-function direct entry.
- `:84-88`: empty/nonempty statement sequencing and expression discard
  preserve left-to-right execution and are sound for the used constructs.
- `:90-97`: RHS-before-store assignment plus disjoint map update/insert rules
  preserve binding and state.
- `:99-101`: test evaluation followed by true/false branch selection is sound.
- `:103-107`: iterable evaluation, list-loop setup, empty termination, and
  variable-bind/body/tail order match the real loop.
- `:109-111`: the return expression is evaluated and its value is put in
  `<result>`. This encoding would fail to discard a following continuation,
  but the submitted `Return` is last, so the exact used context is faithful.
- `:114-117`: name lookup, string literal, and fresh empty-list rules are
  sound.
- `:120,123,126,129,131`: `4.0`, `3.0`, `2.0`, `1.0`, and `0.0` are exactly
  representable and the integer-rational equations are faithful.
- `:121,122,124,125,127,128,130`: the `3.7`, `3.3`, `2.7`, `2.3`, `1.7`,
  `1.3`, and `0.7` equations falsely replace CPython binary values with exact
  decimals. Exact `as_integer_ratio` witnesses for every rule are listed in
  the inventory. Line 121 has the concrete result-changing witness in stage 3;
  lines 124 and 128 have the same above-decimal threshold issue.
- `:133-136`: comparisons evaluate the left then right operand, as Python does.
- `:137-140`: equality and greater-than cross multiplication are correct when
  denominators are positive. The symbolic claims require the current
  denominator positive, and literal denominators are positive. The rules are
  over-broad for syntactically admitted negative/zero denominators because
  their own guards do not state that condition.
- `:144-147`: the one used `Name(...).append(ARG)` form evaluates the argument,
  appends in order, mutates the environment, and yields `none`; it is sound.

### Exhaustive verification-rule decisions

The 13 equations at `verification.k:10-35` are a definitional table summary,
not an operational bridge: program execution still traverses every source
comparison and append. For `Q>0`, their guards are mutually exclusive,
exhaustive, and mathematically agree with the exact-rational table. The
`expectedGrades` empty/cons equations at `:38-40` are true where they match but
unused.

Two proof-local declaration limitations remain:

- `expectedGrade [total]` is globally over-broad. At
  `expectedGrade(0,0)`, the A+ rule (`P=4Q`) and E rule (`P<=0`) both apply
  with distinct results. `Q=0` is outside every dependent claim's
  positive-denominator domain, so this is a global consistency/reuse defect,
  not the intended-domain result witness used for the verdict.
- `expectedGrades [total]` has no equation for a `Vals` list headed by `str`,
  `bool`, `list`, or `none`. It is not total over its declared sort and is
  unused.

The nullary constructor equations for `gradingBody` and `solutionProgram`
(`:45-82`) are truthful and mechanically checked. There is no fresh opaque
result, oracle, operational proof bridge, priority rule, or simplification
lemma. The task result is not encoded into a rule that bypasses the real body.

Thus the decisive static soundness failure is in the generated float-literal
semantics, with a concrete false result on the intended runtime domain. The
separate whole-program claim-set gap is an adequacy failure, not a rule
unsoundness allegation.

## 6. Fresh non-vacuity test

The reviewer-authored mutation
[spec-vacuity.k](evidence/spec-vacuity.k) executes `solutionProgram` on the
satisfiable concrete input `[4.0]`. It preserves the correct final environment
but changes the result obligation from `["A+"]` to `["WRONG"]`.

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
# exit 0: spec parsed and built

kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
# exit 1: WarnStuckClaimState
```

The residual is a fully terminated `.K` configuration whose environment and
result contain `str("A+")`; it fails to unify with the mutated destination.
See [build log](evidence/stage6-vacuity-dry-run.log) and
[proof log](evidence/stage6-vacuity-kprove.log). This is a meaningful rejected
false obligation, not a parser error, timeout, unrelated crash, or unreachable
mutation. Non-vacuity passes.

## 7. Proven versus assumed accounting

### What the successful K proof actually establishes

Under the candidate's generated exact-rational semantics and imported K
builtins:

1. the submitted program returns the empty list on empty input;
2. it returns the proof-local exact-rational table value on every
   positive-denominator singleton;
3. one loop iteration on a positive-denominator numeric head appends the
   proof-local table value and leaves the tail loop, both before and after the
   loop variable exists;
4. an empty internal loop reduces to `.K`; and
5. the one five-element prompt example returns the specified five strings.

It does not establish a final result for arbitrary input-list length. It also
does not establish those singleton results for the real CPython float
semantics, as the `3.7` counterexample demonstrates. As a reachability proof,
it is a partial-correctness result; termination outside the concrete proved
finite instances is not a separate conclusion.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K parser, Haskell/LLVM backends, and imported `INT`, `BOOL`, `MAP`, cell/K-sequence infrastructure | All executions and proofs | Ordinary accepted low-level trust boundary; version and fresh builds recorded. |
| Trusted `py2mpy.py` transliteration | Program-term identity | Trusted launcher input; byte identity and constructor-level KORE equality independently checked. |
| Direct module-to-body entry harness | All whole-program executions | Limited but acceptable for the exact single function: exact name/formal/body and state effects are visible, with body-sensitivity evidence. It is not a general Python call semantics. |
| Candidate `num(P,Q)` representation of runtime floats and exact-decimal literal rules | Every comparison-dependent claim | **Illegitimate bridge.** No sound connection theorem relates it to CPython floats, and the concrete 3.7 witness disproves the connection and changes the result. |
| Builtin unbounded integer arithmetic and positive-denominator rational cross multiplication | Table comparisons | Acceptable mathematics only under positive denominators; symbolic claims state that guard for current grades. |
| `expectedGrade` equations | Singleton and loop-step postconditions | Truthful table specification for `Q>0`; globally over-broad `[total]`/overlap at `(0,0)` is an additional limitation. |
| `expectedGrades` equations | None | Unused and falsely declared total over all `Vals`; no claim relies on it. |
| `gradingBody` and `solutionProgram` constructor macros | Every claim except the bare loop base | Acceptable definitional naming, mechanically equal to the submitted constructor tree; no execution is replaced. |
| Python canonical-vs-candidate differential tests | Implementation-to-canonical bridge on tested cases | Finite empirical evidence only. It strongly supports Python implementation fidelity but neither proves universal equivalence nor repairs K semantics. |
| Concrete `krun` tests | Generated-semantics behavior on recorded inputs | Finite evidence only; one test is a decisive counterexample to the claimed Python bridge. |

There are no opaque proof symbols, trusted auxiliary claims, candidate-supplied
compiled artifacts, or empirical tests being substituted for `kprove`.

### Gate and decision accounting

- Real-program soundness: **FAIL** because the float-literal rules enable a
  false final grade on a satisfying real Python input. Program identity and
  non-vacuity subchecks themselves pass.
- Intent/domain adequacy: **FAIL** because the formal whole-program claims are
  limited to lengths 0, 1, and one fixed length-5 example; one-step loop claims
  do not prove the unrestricted list contract.
- Evidence auditability: **PASS for the evidence actually claimed**. Commands,
  sources, statuses, and bounded outputs are preserved under
  `/audit-output/evidence/`. Finite evidence is labeled as finite.

The reconstructed `#Top` therefore proves only a limited theorem in a
materially inaccurate generated semantics. It is not a legitimate
partial-correctness proof of the real generated program required by the task.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
