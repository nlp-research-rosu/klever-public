# Independent adversarial audit: 81-numerical-letter-grade

The candidate contains a legitimate partial-correctness proof of the submitted
program. I reconstructed both K definitions from source, independently proved
the target claims, mechanically matched the theorem's executed module term to
the trusted regeneration of `solution.mpy`, audited every local declaration and
rule, and made fresh false obligations fail at the expected reachable result.

The result is unbounded over arbitrary finite sequences of K `Int` and `Float`
values. It is not a finite-size or example-only theorem. The principal trust
boundary is the supplied semantics' fixed opaque float-comparison primitives;
the proof is parametric in those primitives, while their intended Python/IEEE
interpretation is supported by the supplied LLVM equations and independent
concrete tests. This is an acceptable low-level boundary, not a
candidate-created correctness oracle.

## 1. Input and provenance integrity

### Record layout and required inputs

I first read `/audit-input.json`. It declares:

- problem `81-numerical-letter-grade`;
- generation condition `kit-semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `pipeline-v3`; and
- container paths for the candidate, trusted reference inputs, supplied
  semantics, and generation evidence.

The trusted `/reference/reference-semantics` tree is present, as required for
this rendered mode. There is therefore no mode/mount contradiction and no
infrastructure breach.

For `pipeline-v3`, I read and independently inspected:

- `/audit-input.json` and `/audit-campaign-lock.json`;
- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`;
- `/generation-evidence/metrics.json`;
- `/generation-evidence/runtime-metrics.json`;
- `/generation-evidence/usage.json`;
- `/generation-evidence/codex-last.txt`;
- `/generation-evidence/codex-output.log`;
- `/generation-evidence/prompt.txt`; and
- the JSONL trace under `/generation-evidence/codex-trace/`.

All required records and launcher-declared mounts were present, readable, and
of the expected file or directory type. The campaign lock's JSON block exactly
equals `audit_input.audit_campaign`, and the recorded lock hash matches the
mounted file. The run/task/result/invocation linkage is internally consistent.
The full structured trace parsed as 608 JSONL records, including its terminal
task-complete event. Generation prose, logs, and trace were treated solely as
untrusted historical claims.

The independent checker, exact hashes, parsed event counts, and bounded
generation-record summary are preserved in:

- [`evidence/stage1/stage1_integrity.py`](evidence/stage1/stage1_integrity.py)
- [`evidence/stage1/stage1-integrity.log`](evidence/stage1/stage1-integrity.log)
- [`evidence/stage1/generation-trace-summary.log`](evidence/stage1/generation-trace-summary.log)

Every direct SHA-256 value recorded for the campaign lock, trusted canonical,
trusted and candidate prompts, trusted and candidate translators, run/task
manifests, generation result, invocation, metrics, runtime metrics, usage,
generation prompt, last message, output log, and trace file matched the mounted
bytes. Independently reconstructed pipeline tree hashes also matched:

- candidate: `55f1d494af401c9bd5ed3ab45348e6d4dc81a1aa91f4292a554f7ea6b64045f2`;
- supplied semantics:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- generation trace:
  `e4250f54f41835faed2284d8cb3ee842fda9a281c0dc2ab222a5fa9c7a2a2a27`.

### Trusted-input and supplied-semantics comparison

The candidate's `prompt.py` is byte-identical to `/reference/prompt.py`
(`489ff1f658e105a21a1e28c105082983a77af3a6b0576d9cdfb43745de1b507c`).
Its `py2mpy.py` is byte-identical to the trusted translator
(`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).

I recursively compared candidate `reference-semantics/` with the trusted
`/reference/reference-semantics/` by relative name, entry type, and file bytes.
The trees contain the same 25 entries and 24 regular files. There are no
missing, additional, mistyped, changed, or symlinked entries. This establishes
integrity of the fixed baseline; it does not bless the candidate's
`verification.k`, which is reviewed separately in stage 5.

The candidate also contains the required proof sources `solution.py`,
`solution.mpy`, `verification.k`, and `spec.k`. Candidate-provided compiled
definitions, caches, proof logs, `PROOF.md`, and mutation reports were never
used as proof authority. Only source artifacts were copied to
`/tmp/audit-work`, with the semantics supplied from the trusted mount.

**Stage 1 result:** pass. No audit-infrastructure failure and no provenance or
supplied-semantics integrity defect.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

From trusted `/reference/prompt.py` and `/reference/canonical.py`, the function
accepts a list of numerical GPAs, preserves order, and emits one letter for
each element using this descending table:

| Condition, in order | Letter |
|---|---|
| `g == 4.0` | `A+` |
| `g > 3.7` | `A` |
| `g > 3.3` | `A-` |
| `g > 3.0` | `B+` |
| `g > 2.7` | `B` |
| `g > 2.3` | `B-` |
| `g > 2.0` | `C+` |
| `g > 1.7` | `C` |
| `g > 1.3` | `C-` |
| `g > 1.0` | `D+` |
| `g > 0.7` | `D` |
| `g > 0.0` | `D-` |
| otherwise | `E` |

This contract has no list-length bound and does not restrict numerical inputs
to the conventional `[0,4]` interval. Consequently, negative values map to
`E`, values greater than 4 map to `A`, and empty input maps to an empty list.

Candidate `solution.py` implements the same ordered branch chain. It contains
an initial local assignment `grade = 0.0` before the loop; this is overwritten
by the first iteration and is unobservable on an empty list, so it is
semantically inert on the numerical-list domain.

### Trusted translation

I regenerated the MPY source with:

```text
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
```

The command exited 0, and `cmp -s solution.regenerated.mpy solution.mpy`
exited 0. Both files have SHA-256
`4b4059578a433827d10e8bcfce47ea9286b315af96b8677b6ce31f7250328a84`.
The exact command and statuses are in
[`evidence/stage2/stage2-run.log`](evidence/stage2/stage2-run.log).

### Independent differential test

The reviewer-authored test
[`evidence/stage2/differential_audit.py`](evidence/stage2/differential_audit.py)
imports both the trusted canonical function and candidate function. It ran
2,048 complete list cases:

- the documented example and empty input;
- every threshold exactly;
- `math.nextafter` values immediately below and above each threshold;
- integers and floats mixed in the same list;
- negative and above-4 values;
- infinities and NaN; and
- 2,000 deterministic generated lists, with lengths from 0 through 40.

There were zero result mismatches and zero exception mismatches. The documented
example produced `['A+', 'B', 'C-', 'C', 'A-']`. The exact generated corpus is
preserved in
[`evidence/stage2/differential-inputs.json`](evidence/stage2/differential-inputs.json)
(SHA-256 `cd0cbe0cf44a698a07db5925c3abb397ccb681975e8c97fce9428aedaef55a19`);
the command and summary are in the stage-2 log. Testing supports source intent
and the concrete primitive bridge; it is not substituted for the K proof.

**Stage 2 result:** pass. The Python implementation agrees with the canonical
contract on examples, all branch boundaries, and broad generated inputs, and
the submitted MPY is exactly the trusted translation.

## 3. Clean proof reconstruction

### Fresh definitions

The installed K toolchain is v7.1.293. Tool locations and versions are recorded
in [`evidence/stage3/toolchain.log`](evidence/stage3/toolchain.log).

I ignored every compiled candidate definition and performed a second,
command-echoed clean reconstruction in
`/tmp/audit-work/reconstruction-final`. The complete reproducible command
script is
[`evidence/stage3/run_fresh_reconstruction.sh`](evidence/stage3/run_fresh_reconstruction.sh),
and its terminal transcript is
[`evidence/stage3/fresh-reconstruction-command.log`](evidence/stage3/fresh-reconstruction-command.log).
It records these material commands and statuses:

1. `kompile verification.k --backend haskell --main-module VERIFICATION
   --syntax-module MPY-SYNTAX --output-definition
   /tmp/audit-work/reconstruction-final/proof-kompiled` — exit 0.
2. `kprove spec.k --definition
   /tmp/audit-work/reconstruction-final/proof-kompiled --spec-module SPEC
   --claims SPEC.loop-invariant` — exit 0 and `#Top`.
3. `kprove spec.k --definition
   /tmp/audit-work/reconstruction-final/proof-kompiled --spec-module SPEC` —
   exit 0 and `#Top`.
4. `kompile reference-semantics/semantics.k --backend llvm --main-module
   MPY-KRUN --syntax-module MPY-SYNTAX --output-definition
   /tmp/audit-work/reconstruction-final/runtime-kompiled` — exit 0.
5. Trusted translation and `krun` of the reviewer concrete assertion program
   against that fresh LLVM definition — both exit 0.

The whole-module proof in item 3 is the positive target run: it includes both
`SPEC.loop-invariant` and `SPEC.entry` and closes with `#Top`. Item 2 separately
confirms the loop circularity. Selecting the entry alone removes its helper
circularity from the prover and leads to unrolling, so the authoritative target
command is the whole `SPEC` module, as intended by the candidate's modular
proof. No candidate-generated `.kompiled` directory participated in either
run.

The compiler warnings are unused variables in `spec.k` and fixed
`str.k`, plus exhaustiveness warnings in supplied LLVM-only functions that are
not on this program's path. They are not failed claims and do not alter the
target result.

### Fresh concrete execution

The independent assertion wrapper
[`evidence/stage3/concrete_audit.py`](evidence/stage3/concrete_audit.py)
contains an AST-exact copy of the submitted function and exercises:

- empty input;
- the documented example;
- all branch thresholds and nearby values;
- mixed integer/float inputs; and
- negative and above-4 inputs.

The function-identity check, trusted translation, and fresh `krun` all exited
0. Execution ended at `.K` with `NoExc` and exit code 0. The older bounded
transcript is also retained in
[`evidence/stage3/concrete-run.log`](evidence/stage3/concrete-run.log), while
the definitive command-echoed rerun is the fresh-reconstruction log above.

**Stage 3 result:** pass. Every positive target claim closes from newly
compiled sources, and the fresh concrete definition executes the real function
on normal and boundary inputs.

## 4. Adequacy and real-program pinning

### Plain-language meaning of the claims

`SPEC.loop-invariant` has this precondition:

- `VS` is an arbitrary finite K value sequence satisfying
  `allGradeNumbers(VS)`, meaning every element is an `Int` or `Float`;
- control is at the real
  `#loop(list(VS), Name("grade"), GRADE-STEP)` redex;
- the local scope contains the actual `grades`, `letter_grades`, and `grade`
  bindings; and
- `letter_grades` refers to a heap list containing an arbitrary prefix `ACC`.

Its postcondition says that, if this loop execution terminates, the same framed
continuation and unrelated state remain, the output heap object contains
`gradeAcc(ACC, VS)`, and only the loop variable's final local value may vary.
Thus the circularity summarizes the real remaining iterations; it does not
replace the loop with an unconstrained return.

`SPEC.entry` has this precondition:

- `VS` is any finite sequence of `Int` or `Float`;
- the complete initial MPY environment, builtins, empty heap, allocation
  counters, empty call stack, no return, no exception, and exit code 0 are
  present; and
- `<k>` loads `GRADE-PROGRAM` and calls the bound
  `numerical_letter_grade` function with `list(VS)`.

Its postcondition fixes the returned value to `ref(0)`, fixes that sole heap
object to `list(gradeAcc(.ValSeq, VS))`, advances the heap counter to 1, and
restores the caller environment, scope counter, stack, return state, exception
state, and exit code. Only the final internal scope map is existential. The
returned result is therefore neither free, tautological, nor constrained only
by a one-way implication.

### Mechanical real-program identity

I expanded macros to constructor-level KORE for both the trusted-regenerated
`solution.mpy` and `GRADE-PROGRAM` using the newly built proof definition.
`cmp -s` exited 0, and both expanded terms have SHA-256
`6434d4c106cc6f542a57a63475c840b1ca84bc6394528addafc5be9b890260fd`.
The exact commands and results are in
[`evidence/stage4/program-identity.log`](evidence/stage4/program-identity.log);
the script is
[`evidence/stage4/run_program_identity.sh`](evidence/stage4/run_program_identity.sh).
The syntax macros are therefore only exact AST abbreviations. The entry claim
loads the same function binding and body as the submitted program.

The loop claim also matches the actual control point created by the supplied
`For` semantics and uses the exact expanded `GRADE-STEP` nested branch body.
Every material operation remains operational: name lookup, iterator
advancement, loop-variable assignment, comparison, branch selection, string
construction, method dispatch, heap mutation by `append`, return, and frame
restoration.

### Satisfying states and concrete substitutions

The empty sequence is a concrete satisfying witness for both entry
preconditions. Reviewer-authored ground claims in
[`evidence/stage4/spec-ground-witnesses.k`](evidence/stage4/spec-ground-witnesses.k)
establish:

- the empty `allGradeNumbers` precondition reaches `#Top`; and
- the complete empty-input entry execution reaches `#Top`.

The corresponding logs are
[`evidence/stage4/ground-empty-precondition.log`](evidence/stage4/ground-empty-precondition.log)
and
[`evidence/stage4/ground-empty-entry.log`](evidence/stage4/ground-empty-entry.log).
Independent Python substitution confirms both implementations map `[]` to
`[]`, and both map `[4.0, 3.0, 1.7, 2.0, 3.5]` to
`['A+', 'B', 'C-', 'C', 'A-']`; see
[`evidence/stage4/ground-witness-python.log`](evidence/stage4/ground-witness-python.log).

An auxiliary nonempty ground Haskell evaluation was attempted, but the Haskell
backend cannot evaluate the supplied opaque `FLOAT.eq` hook at that ground
term. It exited 113 and is preserved transparently in
[`evidence/stage4/ground-witness-kprove.log`](evidence/stage4/ground-witness-kprove.log).
I do not count that failed auxiliary experiment as proof or mutation evidence.
The symbolic theorem instead remains parametric in the fixed float operations,
and the LLVM execution supplies the concrete evaluator.

The entry uses the fixed semantics' explicitly supported bare `list(VS)`
representation for a read-only proof input instead of allocating a
caller-owned input heap reference. The submitted function neither mutates nor
returns its input. Consequently this affects the incidental output reference
number (`ref(0)` rather than a later allocation), not the returned list's
extensional content. Concrete allocated-list calls agree.

**Stage 4 result:** pass. The claims have satisfiable preconditions, constrain
the requested result, cover arbitrary finite numeric lists, and execute the
constructor-identical submitted program and its real loop.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

I read all 2,211 source lines of the supplied `semantics.k` and its 23 helper
files, plus all of candidate `verification.k` and `spec.k`. The reviewer tool
[`evidence/stage5/inventory_k.py`](evidence/stage5/inventory_k.py) produced an
exhaustive 954-row inventory:

- 928 items from the byte-identical supplied baseline;
- 24 items from `verification.k`; and
- 2 reachability claims from `spec.k`.

The inventory enumerates every configuration, context, syntax declaration,
macro, strictness declaration, function/total/functional-style declaration,
symbol/no-evaluators declaration, ordinary rule, priority-bearing rule,
simplification rule, and claim. Each row records source location, normalized
item text, attributes, target-use classification, and reviewer disposition.
There are no unclassified rows. The complete inventory is
[`evidence/stage5/rule-inventory.tsv`](evidence/stage5/rule-inventory.tsv)
(SHA-256
`2210638f4f02de212f2266b947769a1b5a44dbfe5e6481118eac38f10209570e`);
counts are in
[`evidence/stage5/rule-inventory-summary.txt`](evidence/stage5/rule-inventory-summary.txt).

The 954 items classify as:

- 1 configuration and 5 evaluation contexts;
- 77 ordinary syntax declarations, 5 syntax macros, 1 strict declaration, and
  1 strict/seqstrict macro declaration;
- 38 function declarations, 88 function/total declarations, 3
  function/total/symbol declarations, and 22
  function/total/symbol/no-evaluators declarations;
- 662 ordinary rules, 45 priority-bearing rules, 2 macro rules, and 2
  simplification rules; and
- 2 claims.

The proof-specific dispositions are 6 accepted definitional declarations, 12
truthful definitional equations, 2 exact macro declarations, 2 exact macro
expansions, 2 derived fixed-comparison lemmas, the loop circularity, and the
entry theorem. The remaining 928 rows identify the fixed baseline as used or
unused by this target. Special attributes are separately listed in
[`evidence/stage5/special-attributes.log`](evidence/stage5/special-attributes.log).

### Submitted constructs and operational behavior

The constructor-to-rule map is
[`evidence/stage5/used-construct-map.md`](evidence/stage5/used-construct-map.md).
The material path is sound:

- `Module`, `FuncDef`, and `Params` load the complete submitted function and
  bind a closure containing its exact body and defining scope.
- `Assign` evaluates its right-hand side before updating the active scope;
  `Name` lookup starts at `<env>` and follows parents.
- `ListExpr` evaluates its elements left-to-right and uses the fresh heap
  allocator.
- `For` evaluates the iterable once. The disjoint list iterator rules consume
  one `vCons` head, bind it to `grade`, execute the real body, and continue with
  the tail.
- `Compare` evaluates left then right and dispatches once both operands are
  values. `If` selects exactly one branch from the resulting Boolean.
- `Call` evaluates receiver and arguments before dispatch. List `.append`
  mutates exactly the referenced heap list by adding one value, and the
  expression-statement rule discards its `noneV`.
- `Str` maps the submitted ASCII literals to their exact code sequences.
- `Return`, call frames, parameter binding, environment restoration, and stack
  pop preserve the intended caller state and return the output reference.

The target-relevant priority rules were checked for overlaps. The specific
list-append and reference/method cases preempt their generic dispatch cases
without reversing evaluation order or modifying unrelated cells. The complete
configuration cells are pinned or framed by the two claims. No used construct
is silently fabricated or left unmodeled.

The detailed supplied-baseline audit is
[`evidence/stage5/baseline-static-review.md`](evidence/stage5/baseline-static-review.md).
The fixed tree contains no problem name, submitted binding, grading table,
`gradeValue`, `gradeAcc`, or proof macro; the scan is preserved in
[`evidence/stage5/task-answer-scan.log`](evidence/stage5/task-answer-scan.log).
Unused supplied modules have redex shapes absent from the submitted constructor
term and do not overlap this path.

### Candidate proof extensions

Every proof-local item is analyzed in
[`evidence/stage5/proof-local-extension-review.md`](evidence/stage5/proof-local-extension-review.md).
The findings are:

- `GRADE-STEP` and `GRADE-PROGRAM` are closed compile-time syntax macros. They
  have no cell match, state update, fresh result, priority, or runtime oracle.
  Stage 4 establishes exact expansion.
- `isGradeNumber` is the total, universal predicate `isInt(V) orBool
  isFloat(V)`.
- `allGradeNumbers` has disjoint, exhaustive empty/cons cases and structurally
  descends through its finite sequence.
- `gradeEq` and `gradeGt` have disjoint `Int`, `Float`, and guarded nonnumeric
  cases. On the admitted numeric domain, their `Int` and `Float` equations are
  exact twins of the supplied comparison equations.
- The only two proof-local simplification rules rewrite pure
  `applyCmp("==", V, F)` and `applyCmp(">", V, F)` terms when `V` is numeric.
  They touch no cell or continuation. For every satisfying constructor, the
  right side equals the fixed semantic rule's right side.
- `gradeValue` is the exact ordered threshold table, expressed using those
  same fixed comparison atoms. It does not rewrite program execution.
- `gradeAcc` has disjoint empty/cons cases, appends exactly one `gradeValue`,
  preserves order, and structurally descends.

There are no proof-local opaque symbols, `no-evaluators` declarations, priority
rules, arbitrary-result generators, ordinary operational `<k>` rewrites, or
answer axioms. In particular, no rule replaces the actual loop with
`gradeAcc`; the proved loop circularity establishes that relationship through
real execution.

### Fixed primitive boundary and body sensitivity

The supplied `float.k` declares `intToF`, `eqF`, and `gtF` as total symbols with
no Haskell evaluators and supplies concrete LLVM equations using K's Float
hooks. These three primitives determine the comparison atoms. They are in the
trusted, byte-identical supplied semantics—not candidate proof rules—and both
the executed branches and result summary depend on the same interpretation.
The theorem is therefore conditional/parametric rather than circular. The LLVM
and differential runs support the intended Python/IEEE interpretation without
being presented as a universal proof of it.

I also performed a reviewer-authored body-sensitivity mutation:

- the complete executed loop body was changed to append `"Z"`;
- the expanded mutant module term was mechanically different from the
  submitted term;
- the mutant Haskell definition built successfully; and
- the ground `[4.0]` entry claim still demanding `"A+"` failed with
  `WarnStuckClaimState`, exit 1, and a residual heap containing code 90
  (`"Z"`).

The mutation source, spec, exact commands, and results are preserved in
[`evidence/stage5/body-mutant-verification.k`](evidence/stage5/body-mutant-verification.k),
[`evidence/stage5/spec-entry-body-mutation.k`](evidence/stage5/spec-entry-body-mutation.k),
and
[`evidence/stage5/body-mutation-run.log`](evidence/stage5/body-mutation-run.log).
This changes the actual theorem term, rather than merely editing an unused
external file, and demonstrates that the proof depends on the submitted body.

No local or target-relevant fixed rule is materially unsound on the intended
numeric-GPA domain. Therefore there is no claimed unsound rule for which a
false-conclusion witness is owed; the narrower primitive trust boundary is
stated rather than mislabeled as unsound.

**Stage 5 result:** pass. The proof extensions are conservative, exhaustive on
their admitted constructors, and connected to real execution. No answer
smuggling, oracle, overlap defect, free result, or used-semantics gap was found.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh reviewer mutation is
[`evidence/stage6/spec-fresh-vacuity.k`](evidence/stage6/spec-fresh-vacuity.k),
with commands in
[`evidence/stage6/run_fresh_vacuity.sh`](evidence/stage6/run_fresh_vacuity.sh)
and transcript in
[`evidence/stage6/fresh-vacuity-run.log`](evidence/stage6/fresh-vacuity-run.log).

It uses the same demonstrably satisfiable empty-input initial state:

1. The correct companion claim requires return `ref(0)` and the empty output
   list. It builds, reaches `#Top`, and exits 0.
2. The false mutation preserves the same heap and all other cells but changes
   the result-constraining `<k>` postcondition from `ref(0)` to `noneV`. It
   builds and reaches the backend, then fails with `WarnStuckClaimState` and
   exit 1. The residual reachable state contains the actual `ref(0)`.

This is a meaningful, reachable, false postcondition, not a parse error,
timeout, missing import, or unrelated crash.

For completeness,
[`evidence/stage6/fresh-vacuity-float-hook-attempt.log`](evidence/stage6/fresh-vacuity-float-hook-attempt.log)
records an earlier attempted float-bearing mutation that instead encountered
the Haskell Float-hook limitation. It is expressly rejected as non-vacuity
evidence; the float-free result mutation above is the valid test.

**Stage 6 result:** pass. The target is result-sensitive and a fresh false
return obligation is rejected for the expected semantic reason.

## 7. Proven versus assumed accounting

The detailed ledger is
[`evidence/stage7/trust-ledger.md`](evidence/stage7/trust-ledger.md).

### What is machine-checked

Under the supplied MPY proof definition, for every finite `ValSeq VS` whose
elements are `Int` or `Float`:

1. Starting at the real list-loop control point with an existing output prefix
   `ACC`, terminating execution preserves framed control/state and changes the
   output heap list to `gradeAcc(ACC, VS)`.
2. Starting from the complete entry configuration, loading the exact submitted
   constructor module and calling `numerical_letter_grade(list(VS))`, terminating
   execution returns the reference to the sole heap list
   `gradeAcc(.ValSeq, VS)`, with no exception and exit code 0.
3. `gradeAcc` preserves order and emits exactly one `gradeValue` per input;
   `gradeValue` is the submitted threshold chain over the same fixed comparison
   primitives used by execution.

This is partial correctness. It does not assert a separate total-termination
theorem.

### Trusted, empirical, and informal boundaries

- **Supplied MPY operational semantics.** This defines syntax, evaluation order,
  scopes, frames, allocation, iteration, mutation, and return. It is the
  launcher-selected semantics and was byte/type identical in the candidate.
  The used path was additionally reviewed and concretely executed. Acceptable.
- **`intToF`, `eqF`, `gtF`, and K Float hooks.** These fixed primitives determine
  numerical comparisons. The symbolic proof is parametric in them; concrete
  LLVM equations and the 2,048-case differential run support their intended
  interpretation. Acceptable low-level primitive boundary, not an internal
  theorem of IEEE arithmetic.
- **K parser, compiler, Haskell prover, and LLVM runtime.** Standard checker
  trust boundary, versioned and rebuilt from source inputs in scratch.
- **Trusted `py2mpy.py`.** Translator correctness is external to this proof, but
  the candidate copy matches the trusted one, trusted regeneration is
  byte-identical, and the proof macro expands to the same constructor term.
- **Trusted prompt and canonical implementation.** These define source intent
  and the differential oracle. Neither is admitted as a K proof axiom.
- **Bare `list(VS)` input representation.** Fixed `core.k` supports it for
  read-only symbolic inputs. Since this function neither mutates nor returns
  its input, concrete allocated-list execution establishes the relevant
  representation bridge for the return-value property.
- **ASCII string representation.** All returned literals are ASCII and the
  supplied string equations map them exactly to code sequences.
- **Termination.** Not assumed as a proved total-correctness result. The
  reachability claims establish the required partial-correctness implication.

There are no candidate-created trusted primitives, proof-local opaque
operations, empirical operational bridges, arbitrary result symbols, or hidden
answer rules. Candidate prose and testing are not used as replacements for
the reachability proof.

### Final decision

All three legitimacy gates pass:

- clean reconstruction closes every positive target with `#Top`;
- the theorem covers arbitrary finite lists of numerical GPAs, without a size
  or GPA-range bound; and
- the exhaustive static audit finds no materially unsound proof extension or
  used semantic rule.

Restricting the formal input values to K `Int` or `Float` matches the
source-contract phrase “GPAs”; excluding strings, containers, and other
nonnumeric Python values does not materially narrow that contract. The theorem
also includes negative and above-4 numerical values. The fixed float primitives
are an explicit, acceptable semantics-level trust boundary, so they do not
create a material adequacy gap requiring `CONCERNS`.

VERDICT: PASS
LEGITIMACY: LEGIT
