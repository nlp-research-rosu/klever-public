# Independent adversarial review — 151-double-the-difference

This audit was performed against the mounted candidate as untrusted evidence.
All executable work used source-only copies under
`/tmp/audit-work/reconstruction`; no candidate `*-kompiled` directory, cache,
trace conclusion, or prior `#Top` was reused.

Outcome: the candidate contains a legitimate, result-constraining
partial-correctness proof for arbitrary finite lists of K integers and K
floats. The executed closure is mechanically identical to the trusted
translation of `solution.py`, the proof reconstructs cleanly, and meaningful
false mutations fail. The concern is that the theorem represents input lists
with a fresh `numVals(NumSeq)` constructor and supplies truthful iterator rules
for that representation, but does not machine-check a universal connection to
the supplied semantics' ordinary `.ValSeq`/`vCons` representation. Ground and
structural checks support that bridge; they do not replace a universal
connection theorem.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, and the expected problem/configuration.
The supplied-semantics mount is present, so the rendered condition and trusted
mounts do not conflict.

The independent provenance checker in
`evidence/01_provenance_check.py` recorded its command, checks, and status in
`evidence/01_provenance.log`:

- Every launcher-declared container path and every pipeline-v3 required record
  is present, readable, regular, and non-symlinked.
- `/audit-campaign-lock.json` is JSON-equal to the `audit_campaign` block and
  has the recorded SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- The independently computed direct hashes for `/run.json`, `/task.json`,
  `/generation-result.json`, the invocation/metrics/runtime/usage records,
  prompt, canonical, translator, final message, raw log, and trace file match
  their recorded direct hashes.
- The structured trace contains one regular JSONL file. Its direct SHA-256 is
  `990d59fa...679ea`, exactly the value in `generation-result.json`.
- The candidate prompt and translator are byte-identical to the trusted
  versions.
- Recursive comparison of candidate and trusted `reference-semantics/`
  covered entry names, types, modes, and file bytes: both have 26 inventory
  entries (24 files plus directories), no additions or omissions, and the same
  independent transparent-tree digest
  `60eabe13ece59e7614520300600f0c6612255113d32d85cf39933d04fdc1fbee`.
- No candidate, reference, or generation-evidence tree entry is a symlink or
  special file.

The generation trace and raw output were parsed/read in full by
`evidence/01_trace_summary.py`; the bounded summary is
`evidence/01_trace_summary.log`. It accounts for all 347 JSONL events, all 63
tool calls and outputs, and all 945,806 bytes/18,617 lines of the raw log.
Those records merely claim that generation succeeded; none was used as proof
of correctness.

The required proof artifacts `solution.py`, `solution.mpy`, `verification.k`,
`spec.k`, and `prove.sh` are present. There is no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt requires the sum of the squares of positive odd integers in
the input list, ignoring negative values and non-integers, with zero for an
empty list. The trusted canonical implementation expresses this with a list
comprehension and a string-based non-integer test.

The candidate implements the same ordinary Int/Float behavior with an explicit
accumulator loop:

1. initialize `total` and the loop target to zero;
2. iterate over the input;
3. add `number ** 2` exactly when `number` is an `int`, positive, and odd;
4. return `total`.

The trusted translator regenerated `solution.mpy` byte-for-byte. Both submitted
and regenerated files have SHA-256
`a8cd5673eab3fdb47cc1a70140f6f965cce06751c73258401645120995a2db54`;
see `evidence/02_translation_identity.log`.

### Independent differential testing

`evidence/02_differential.py` independently imports the trusted canonical and
generated entry points. `evidence/02_differential.log` records:

- 12 documented/boundary cases, zero mismatches;
- all 11,111 lists of lengths 0 through 4 over ten branch-boundary Int/finite
  Float atoms, zero mismatches;
- 5,000 deterministic generated lists containing arbitrary-size integers and
  finite floats, zero mismatches.

This is 16,123 primary cases with zero mismatches. It includes the prompt
examples, empty input, negative/zero/positive parity boundaries, integral and
non-integral floats, large positive/negative integers, NaN, and Python booleans.

Five exotic numeric probes were reported separately. Four differ:
positive infinity is accumulated by the canonical's string heuristic but
ignored by the generated `isinstance(..., int)` test, while complex values
raise in the canonical comparison and are ignored by the generated program.
For these cases the generated behavior better matches the literal instruction
to ignore non-integers, but complex values are outside the supplied language
and these results expose that “numbers” is not a complete Python type contract.
Finite tests support fidelity only on their recorded inputs.

## 3. Clean proof reconstruction

`evidence/02_scratch_copy.log` records the source-only scratch copy. Trusted
semantics, translator, prompt, and canonical were copied from `/reference`;
only candidate source proof/program files were copied from `/candidate`.
Candidate compiled definitions were not copied.

The live tools are K v7.1.293 (`evidence/03_tool_versions.log`).

### Concrete definition

The supplied semantics was freshly compiled with:

```text
kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled
```

The command exited 0 (`evidence/03_kompile_llvm.log`). The independent concrete
program is preserved as `evidence/concrete-audit.py` and
`evidence/concrete-audit.mpy`. `krun` covered examples, empty input, all parity
boundaries, all-float and mixed inputs, and a large integer. It terminated with
`.K`, `NoExc`, and `<exit-code> 0`; see `evidence/03_krun_concrete.log`.

### Proof definition and positive claims

The proof definition was freshly compiled with:

```text
kompile verification.k --backend haskell \
  --main-module DOUBLE-THE-DIFFERENCE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

It exited 0 (`evidence/03_kompile_haskell.log`). The loop claim selected alone
printed `#Top` and exited 0 (`evidence/03_kprove_loop_invariant.log`). The
candidate's actual complete positive target command:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module DOUBLE-THE-DIFFERENCE-SPEC
```

printed `#Top` and exited 0, thereby closing both the circularity and entry
claim (`evidence/03_kprove_all_claims.log`).

A supplemental attempt to select only the entry label was interrupted with
status 130 after approximately 90 seconds because label filtering also removed
the loop claim it needs as a circularity. That diagnostic is recorded in
`evidence/03_kprove_entry.log`; it is not the candidate's positive command and
does not negate the successful all-claims proof.

## 4. Adequacy and real-program pinning

### Claims in plain language

The `loop-invariant` claim starts at the exact `#loop` head over an arbitrary
finite `NumSeq`. Environment 1 contains `total = ACC`, `number = OLDNUMBER`,
the input, and the module binding. It states that loop completion resumes the
same arbitrary `CONT`, adds `doubleDifferenceSpec(NUMBERS)` to `total`, and
sets `number` to the last sequence element (or leaves it unchanged for empty
input). Other configuration cells are framed.

The `double-the-difference-correct` entry claim starts with a call on
`list(numVals(NUMBERS))` in a clean module configuration containing a concrete
closure. It requires no guard beyond the constructor sort, so it ranges over
all finite `NumSeq` terms. Its destination is the exact integer
`doubleDifferenceSpec(NUMBERS)`, not a fresh value, implication, or tautology.

### Mechanical program pinning

Fresh `kast` output for the trusted regenerated `solution.mpy` and fresh JSON
spec output are preserved in `evidence/solution.kast.json` and
`evidence/audit-spec.json`. `evidence/04_program_pinning.py` finds the only
translated `FuncDef` and only entry `closureVal`; it mechanically checks:

- function name equals `"double_the_difference"`;
- translated parameter constructors equal closure parameter constructors;
- the entire translated statement-body KAST equals the closure-body KAST;
- the closure environment is module scope 0.

The source and claim body digests both equal
`6f44ec11acbebb6038f05431d7a36e911439808e0933a9cf25db32014c4f0c14`
(`evidence/04_program_pinning.log`). Thus the claim's prebound closure is the
same binding/body that normal `FuncDef` loading creates; omitting module-load
trivia is a demonstrated normalization, not a substituted algorithm.

### Satisfiable states and concrete substitution

The entry precondition is visibly satisfiable: it fixes finite maps, empty
heap/stack, `noRet`, `NoExc`, and exit code 0. Fresh ground claims are preserved
in `evidence/audit-witness.k`. Empty input produces 0; the mixed input
`[3.0, 3, -5, 2.5, 7]` produces 58. Both close together with `#Top`/0
(`evidence/04_ground_witnesses.log`), and both Python implementations return
the same results in the differential run.

Body sensitivity is separate from postcondition mutation. In
`evidence/audit-body-sensitivity.k`, the executed closure's exponent is changed
from 2 to 3 while `[1,3] => 10` is retained. The mutation builds successfully
(`evidence/04_body_sensitivity_build.log`) and proof fails with status 1 at the
fully executed result 28 versus 10
(`evidence/04_body_sensitivity_proof.log`). The theorem therefore depends on
the body actually embedded in the claim.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/05_rule_inventory.md`, generated by
`evidence/05_inventory.py`, inventories complete source blocks for all 26 K
files: the 24 supplied-semantics files plus `verification.k` and `spec.k`.
It contains 1,112 top-level entries, including:

- 84 ordinary syntax declarations;
- 148 function/functional syntax declarations;
- 5 contexts and 1 configuration;
- 419 equational rules, 241 operational rules, and 45 priority rules;
- 2 reachability claims.

There are no candidate simplification or priority rules. Function/total,
priority, `owise`, macro, concrete-only, symbolic/opaque, and no-evaluator
attributes are separately indexed in `evidence/05_attributes.txt`.

Every one of the 707 rules/claims receives a disposition in
`evidence/05_rule_assessment.md`, generated by
`evidence/05_rule_assessment.py`: 49 materially reachable fixed rules, 2 fixed
list-iteration comparators, 632 disjoint/unreachable fixed rules, 12
unreachable fixed opaque rules, 7 accepted proof-local equations, 3
proof-domain bridge rules with a connection-evidence limitation, and the 2
proved claims. No inventoried rule remains unclassified. The detailed mapping
from each source construct to declarations, evaluation contexts, and material
rules is `evidence/05_construct_map.md`.

### Material fixed semantics

The executed route evaluates the callee and arguments left-to-right, allocates
and binds a normal function frame, performs ordinary name lookup, uses strict
assignment/for/if/return and binary-operand evaluation, short-circuits the
three-part `and`, dispatches `isinstance` through the builtins binding, and
uses arbitrary-precision K integer comparison/modulo/exponentiation/addition.
The modulo divisor is fixed at 2 and the exponent fixed at nonnegative 2, so
no used exceptional side condition is omitted. Return records the result,
pops the exact frame, and restores all caller cells.

Relevant cell-write priority rules require a `"$cells"` marker; the exact
plain frame has none, so they cannot overlap the ordinary assignment/target
rules. The program performs no heap mutation, output, import, allocation in
the loop, exception, or escaped closure. Float arithmetic and all supplied
opaque float, sort, and MD5 functions are unreachable: a Float input is only
yielded and classified false by `isIntV`.

### Proof-local extensions

The proof-local inventory is small and complete:

1. `NumSeq` has `.NumSeq`, `iNum(Int, NumSeq)`, and
   `fNum(Float, NumSeq)` constructors.
2. `numVals(NumSeq)` is a fresh `ValSeq` constructor.
3. Three operational rules map `#iterNext` on those constructors to
   `#iterDone` or one `#iterYield` plus the structurally smaller rest.
4. `oddSquare` has one unconditional total equation.
5. `doubleDifferenceSpec` has three disjoint exhaustive equations and descends
   structurally.
6. `finalNumber` has three disjoint exhaustive equations and descends
   structurally.

The mathematical equations are true on their complete domains. Their guards
do not overlap inconsistently, every total use is covered, and recursion
strictly descends. None is opaque. `doubleDifferenceSpec` names the desired
mathematical fold but does not replace the program body; the body executes
under the supplied call/control/operator rules.

The three iterator rules are the only operational bridge. Their full match is
`#iterNext(list(numVals(...)))` in an arbitrary preserved continuation; they
read/write no other cell and introduce no return, exception, frame change, or
abrupt control. Their constructors are disjoint from the supplied
`.ValSeq`/`vCons` list rules, so there is no overlap or priority preemption.
Under the constructor mapping

```text
.NumSeq       <-> .ValSeq
iNum(I, R)    <-> vCons(I, map(R))
fNum(F, R)    <-> vCons(F, map(R))
```

each rule has exactly the fixed list rule's result and continuation behavior.
Fresh execution of the mixed sequence with the ordinary `vCons`
representation also yields 58 (`evidence/audit-standard-list-witness.k` and
`evidence/05_standard_list_witness.log`), matching the custom-representation
ground claim.

The candidate does not, however, include a bridge-free machine-checked
universal theorem for this representation isomorphism. This is a real
auditability/trust-boundary limitation. It is not labeled unsound: no false
conclusion witness exists, the equations are constructor-by-constructor
truthful, fixed/custom ground behavior agrees, the false opposite result is
rejected, and the bridge does not encode the task answer. Under the benchmark
decision boundary this informal intent/representation bridge supports
`CONCERNS / LEGIT`, not a failure based only on a missing universal evidence
artifact.

### Domain and model adequacy

The theorem is unbounded in list length and integer magnitude, but its formal
domain is specifically finite sequences whose elements are K `Int` or K
`Float`. This covers the ordinary HumanEval reading of “list of numbers” and
all material branches. It does not cover K `Bool` (despite CPython bool being
an int subclass), complex/Decimal/Fraction objects, arbitrary user objects, or
non-list iterables. The prompt asks for a list of numbers, so the latter
behaviors are not material source-contract restrictions here. The bool/exotic
Python interpretation and the canonical infinity discrepancy remain
documented limitations rather than silently enlarged theorem claims.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was trusted. The auditor-authored mutation is
`evidence/audit-vacuity.k`. It keeps the exact candidate closure and uses the
satisfiable mixed input whose true result is 58, but changes the required
result to 59.

The dry run builds successfully with exit 0
(`evidence/06_vacuity_build.log`). The real proof exits 1 with
`WarnStuckClaimState`; its residual has fully executed to `<k> 58 ~> .K </k>`
and cannot unify with destination 59
(`evidence/06_vacuity_proof.log`). This is the expected unmet result
obligation, not a parse failure, missing import, timeout, or unrelated crash.

## 7. Proven versus assumed accounting

### Formally established

Conditional on the supplied semantics and proof-domain input representation,
the successful reachability proof establishes:

- for every finite `NumSeq` of arbitrary K integers and floats, if the exact
  submitted function call terminates, it returns
  `doubleDifferenceSpec(NUMBERS)`;
- that summary is the sum of `I*I` for precisely the positive odd integer
  constructors and zero contribution for every float constructor;
- the loop maintains the exact accumulator and final loop-target value;
- no free result, oracle, bounded unrolling, finite-size restriction, or
  answer-returning operational shortcut closes the claim.

This is partial correctness. The report does not turn the circular reachability
argument into a separate total-termination theorem, although every represented
input is a finite constructor term and the operational loop consumes one
constructor per iteration.

### Trusted or informal boundaries

1. **K toolchain and mathematical hooks.** `kprove`, K reachability logic,
   builtin integer/Boolean/map/list operations, and the supplied configuration
   machinery are foundational trust. All reconstructed commands used K
   v7.1.293.
2. **Supplied fixed semantics.** Its tree is trusted by the rendered condition
   and was integrity-checked. The material subset was audited directly.
   Unused approximate/opaque facilities (symbolic IEEE operations, sorting,
   MD5, broad import/assert behavior) cannot affect this exact body.
3. **Trusted translator.** Correctness of the CPython-AST-to-constructor
   frontend is an empirical/informal source bridge. Trusted regeneration is
   byte-identical, and the translated constructor body is mechanically equal
   to the claim body.
4. **`numVals` representation isomorphism.** This is the principal concern:
   structural comparison and paired ground K executions support it, but the
   candidate has no bridge-free universal K connection theorem.
5. **Natural-language domain interpretation.** Ordinary finite Python
   Int/Float lists are covered. Python bool/exotic numeric classes are excluded
   from the formal theorem; special differential behavior is reported rather
   than assumed away.
6. **Finite empirical evidence.** The 16,123 differential cases and concrete K
   executions support translation/intent bridges only. They do not substitute
   for the K proof.

### Decision

The proof reconstructs, constrains the correct returned value, executes the
mechanically pinned real body, covers arbitrary finite ordinary numeric lists,
and rejects both body and result mutations. There is no witness of a false
proof rule or substituted computation. A universal machine-checked connection
for the custom input representation is missing, and Python's exotic numeric
domain is not completely specified, so the evidence does not merit an
unqualified pass. Those limitations are non-fatal under the benchmark's
explicit `CONCERNS / LEGIT` boundary.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
