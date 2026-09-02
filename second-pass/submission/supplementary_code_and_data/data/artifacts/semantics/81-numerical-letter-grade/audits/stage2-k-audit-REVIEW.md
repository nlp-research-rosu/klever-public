# Independent adversarial review: 81-numerical-letter-grade

## Executive finding

The candidate can be rebuilt and all submitted claims print `#Top`, and the
claim harness contains the exact translated function body. Those facts do not
make the proof legitimate. The proof adds a fresh, total, opaque Boolean
`gpaEqFour` and:

1. uses it in a priority rule that replaces execution of the fixed-semantics
   Float comparison `grade == 4.0`; and
2. reuses the same unconstrained value in `eqFour`, `gradeOf`, and the final
   list summary.

There is no bridge-free theorem connecting `gpaEqFour(F)` to fixed-semantics
Float equality. This is the exact circular result-bearing-oracle pattern
forbidden by the validation contract. It enables a concrete false conclusion:
with the admitted ground interpretation `gpaEqFour(3.9) = true`, the extended
K semantics accepts that the real submitted function returns `["A+"]` on
`[3.9]`; the trusted semantics and both Python implementations return `["A"]`.

Independently, the arbitrary-length claims quantify over the candidate-only
input term `numericValues(GS)`, not the real fixed-semantics recursive
`vCons(...)` representation. No connection theorem relates those
representations. The only entry claims over real `ValSeq` inputs cover the
empty list and two singleton regions. Thus the general HumanEval list domain
is not established even apart from the oracle.

## 1. Input and provenance integrity

The declared layout is `legacy-selected-stage1`, the rendered mode is
`SUPPLIED_SEMANTICS`, and `/reference/reference-semantics` is present. There is
no rendered-mode/mount contradiction.

I read and parsed:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`,
  `legacy-metrics.json`, and `legacy-run-input.json`; and
- all 495 JSONL records in the structured trace.

All required records and launcher-declared container paths are real regular
files/directories rather than symlinks. The relevant mounts are read-only
([`stage1_mounts.log`](evidence/stage1_mounts.log)). The campaign-lock JSON
object exactly equals `audit_input.audit_campaign`, and the lock's file SHA-256
is the recorded `ad5dfc...d745`.

The independent integrity script checked every file hash exposed by the
manifest/result records. In particular, the run, task, result, invocation,
metrics, usage, prompt, output log, last message, and individual trace-file
hashes all match. The mounted candidate has the independently recomputed
length-delimited digest `beb977...600`, equal to the invocation's retained
workspace digest. The semantics digest `4e0639...789f` equals the separately
recorded manifest digest, and the trace-tree digest `33846c...1085` equals
`usage.json`'s source-trace digest. `/audit-input.json` also carries
launcher-current tree hashes under a different encoding (`f73630...`,
`1de6d5...`, and `a867da...`); those were not conflated with the
length-delimited digests.

Most importantly, recursive entry/type/content comparison found the candidate
and trusted semantics trees identical: 24 files, one subdirectory, no missing
or additional entry, no changed bytes, no mistyped entry, and no symlink.
Candidate `prompt.py` and `py2mpy.py` are also byte-identical to their trusted
mounts. Full evidence is in
[`stage1_integrity.py`](evidence/stage1_integrity.py) and
[`stage1_integrity.log`](evidence/stage1_integrity.log). The generation records
were treated only as claims; their bounded structural summary is
[`stage1_generation_summary.log`](evidence/stage1_generation_summary.log).

Stage 1 result: infrastructure/provenance gate passed.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract maps each GPA independently, preserving list order:
exactly `4.0` maps to `A+`; otherwise the first strict descending threshold
among `3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0` determines
`A, A-, B+, B, B-, C+, C, C-, D+, D, D-`; values not above zero map to `E`.
The result is the list of those letters.

The candidate implements the same decision tree, with an added `float(grade)`
normalization. Running the trusted translator in scratch produced
`solution.regenerated.mpy` byte-identical to submitted `solution.mpy`
([`stage2_translation.log`](evidence/stage2_translation.log)).

The independent differential oracle imports `/reference/canonical.py` and
`/candidate/solution.py`. It tested the documented example, empty input, every
threshold, both adjacent IEEE-754 neighbors of every threshold, small
integers, NaN/infinities, and 1,000 deterministic generated lists. There were
0 mismatches across 1,058 cases and 12,307 scalar GPA values
([`differential_test.py`](evidence/differential_test.py),
[`stage2_differential.log`](evidence/stage2_differential.log)).

An intentionally out-of-GPA diagnostic found that `10**1000` returns `A` in
the canonical implementation but raises `OverflowError` in the candidate
because of the added conversion. This does not affect the ordinary GPA domain,
but it means the candidate is not CPython-equivalent over arbitrary Python
integers; the K claim's unrestricted `iGrade(Int, ...)` wording is broader than
that executable behavior.

Stage 2 result: fidelity passed for the material GPA domain, with the noted
out-of-domain/over-broad-claim observation.

## 3. Clean proof reconstruction

I copied source artifacts to `/tmp/audit-work/candidate`, used the trusted
semantics tree, and did not copy or reuse candidate-built definitions/caches.
K version 7.1.293 was available.

Fresh builds:

- LLVM supplied semantics:
  `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled`
  exited 0
  ([`stage3_kompile_llvm.log`](evidence/stage3_kompile_llvm.log)).
- Haskell proof definition:
  `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled`
  exited 0
  ([`stage3_kompile_haskell.log`](evidence/stage3_kompile_haskell.log)).
- `krun smoke.mpy --definition runtime-kompiled --output pretty` exited 0
  with `NoExc` and K exit-code 0
  ([`stage3_krun_smoke.log`](evidence/stage3_krun_smoke.log)).

Fresh proof results:

| Selection | Result |
|---|---|
| `SPEC.empty` | `#Top`, exit 0 |
| `SPEC.a-plus` | `#Top`, exit 0 |
| `SPEC.a` | `#Top`, exit 0 |
| `SPEC.loop-maps-all-numeric-grades` | `#Top`, exit 0 |
| `SPEC.function-maps-all-numeric-grades,SPEC.loop-maps-all-numeric-grades` | `#Top`, exit 0 |
| all claims, as submitted | `#Top`, exit 0 |

The function theorem needs the loop claim as a circularity. A diagnostic
selecting the function alone excluded that dependency and unrolled until I
stopped it; that diagnostic is not a submitted positive command. The function
closes in its explicit dependency set and in the all-claims command. Exact
commands, statuses, and links to each bounded log are indexed in
[`COMMANDS.md`](evidence/COMMANDS.md).

Stage 3 result: verification reconstruction passed. This establishes closure
only under the candidate-extended theory, not soundness of that theory.

## 4. Adequacy and real-program pinning

### Constructor-level program identity

Using `kast --expand-macros`, I parsed the trusted-regenerated module and the
candidate's `numericalLetterGradeBody`. After extracting the sole function's
body, their canonical KAST SHA-256 values were both
`3c0beee8f266d581230a8265a475dafc409269ac3653e4b50ba5e913f4b88608`.
The KAST objects are equal, the entry is `numerical_letter_grade`, its sole
parameter is `grades`, and the module has no extra executable statements.
`runGrades` binds that expanded body into a closure and invokes it. See
[`pinning_compare.py`](evidence/pinning_compare.py) and
[`stage4_pinning_compare.log`](evidence/stage4_pinning_compare.log).

Thus the body itself is not substituted. The proof harness directly invokes
the exact closure body instead of replaying module loading and a source-level
name call; given the exact body/binding check and initial module environment,
that normalization is semantically inert for this function.

### Claim meanings

- `empty` executes the exact function on a real empty `ValSeq` and requires
  the returned heap object to contain `[]`.
- `a-plus` executes it on one real Float and, assuming `eqFour(F)`, requires
  `["A+"]`.
- `a` executes it on one real Float and, assuming `not eqFour(F)` and
  `above(F,3.7)`, requires `["A"]`.
- `function-maps-all-numeric-grades` executes the exact function on
  `list(numericValues(GS))` and requires the returned heap list to equal
  `mappedAppend(.ValSeq,GS)`.
- `loop-maps-all-numeric-grades` is the circular loop-head summary. It
  preserves the arbitrary continuation and framed cells, extends the heap
  accumulator with `mappedAppend(PREFIX,GS)`, and records the last converted
  grade.

Every claim precondition is satisfiable. Concrete/model witnesses and
substitutions are listed in
[`stage4_claim_witnesses.md`](evidence/stage4_claim_witnesses.md). Empty,
4.0, and 3.9 witnesses agree with both Python implementations under the
intended primitive interpretation.

### Adequacy failure

The arbitrary theorem's nonempty input is not a fixed-semantics Python list.
`numericValues` is a newly added `ValSeq` constructor. For example:

- real input `[3.9,3]` is represented by
  `vCons(3.9,vCons(3,.ValSeq))`;
- the theorem uses
  `numericValues(fGrade(3.9,iGrade(3,.NumericGrades)))`.

These are distinct constructors, and the candidate supplies direct iterator
rules for the latter. It supplies no bridge-free reachability theorem or
equation connecting the proof-only term to the real list term. Consequently,
the general claim cannot be instantiated on an actual nonempty `vCons` input.
The real-input entry claims cover only empty and two singleton branch regions,
not arbitrary lengths or all grading branches. This is a material source-domain
gap, not merely missing source-to-proof automation.

Stage 4 result: syntactic/body pinning passed; real-input domain adequacy failed.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`static_inventory.json`](evidence/static_inventory.json) contains the source,
line span, full text, attributes, flags, digest, disposition, and rationale for
all 973 outer K sentences:

- supplied semantics: 1 configuration, 5 contexts, 227 syntax declarations,
  and 695 rules;
- candidate `verification.k`: 11 syntax declarations and 29 rules; and
- `spec.k`: 5 claims.

The summary is in
[`stage5_static_inventory.log`](evidence/stage5_static_inventory.log). There
are no candidate simplification rules. Candidate priority rules are the
equality bridge and the three proof-only iterator cases.

The 928 supplied-semantics sentences are the selected, byte-verified trusted
baseline, not candidate proof extensions. For the submitted program's used
path I additionally checked:

- syntax/evaluation order for `Module`, `FuncDef`, `Assign`, `Name`,
  `ListExpr`, `For`, `Call`, `Attribute`, `If`, `Compare`, `Expr`, `Return`,
  Float and String literals (`semantics/syntax.k`);
- configuration, allocation, scopes, lookup/builtins, argument evaluation,
  and sequencing (`core.k`);
- closure calls, parameter binding, frame push/pop, and return control
  (`call.k`, `functions.k`);
- assignment, branching, loop control, target binding, and continuation
  handling (`controls.k`, `tuple.k`);
- list construction, real-list iteration, left-to-right concatenation, and
  in-place append (`list.k`);
- string representation (`str.k`); and
- Float conversion and comparison dispatch (`float.k`, `operators.k`).

The exact program executes material allocation, lookup, calls, iteration,
append heap writes, branching, return, and frame restoration. The candidate
does not bypass those operations except at the equality comparison described
below and at iteration of its proof-only input representation.

### Candidate-local rules

1. **Program macros, `runGrades`, and `letter` (lines 7–66): accepted.**
   The two macros expand to the exact regenerated body. `runGrades` is a fresh
   harness constructor, not a rewrite of a source operation, and invokes the
   exact closure. `letter(S) = str(strToCodes(S))` matches fixed string
   representation.

2. **`gpaEqFour` declaration (lines 70–71): rejected result-bearing oracle.**
   It is `[function,total,symbol(gpaEqFour),no-evaluators]`, has no defining
   equations, and affects the first branch, returned string, heap result, and
   final postcondition.

3. **Float equality bridge (lines 72–75): rejected operational bridge.**
   At priority 40 it rewrites
   `Compare(F, CmpOp("==", 4.0))` to `gpaEqFour(F)` before fixed
   `Compare -> applyCmp -> ==Float` execution. Its matched continuation and
   framed cells are broad (`...`). Although it leaves those cells unchanged
   and runs after operand evaluation, there is no bridge-free universal
   connection theorem fixing its value. Priority supplies preemption, not
   equivalence.

4. **`eqFour` (line 76): rejected as circular justification.**
   It aliases the result summary to the same unconstrained atom introduced by
   the operational bridge. Its appearance on both execution and specification
   sides does not prove actual equality.

5. **`above` (line 77): accepted conditionally.**
   It is a direct alias to supplied `gtF`. `gtF` is a supplied trusted
   no-evaluator primitive for symbolic proofs with a concrete `>Float` rule
   for LLVM.

6. **`NumericGrades`, `numericValues`, and iterator rules (lines 82–97):
   internally coherent but inadequate/unconnected.** The three rules describe
   empty, Float-head, and Int-head iteration in left-to-right order and
   preserve the continuation/cells. They are exhaustive and nonoverlapping
   over `NumericGrades`. However, they operate on a fresh list-representation
   constructor and have no bridge-free theorem relating it to real `vCons`
   lists. LLVM compilation of the extended module also warns that adding this
   new `ValSeq` constructor makes numerous supplied `[total]` functions
   non-exhaustive on it (`vsLen`, `valSeqConcat`, `valSeqAt`, and others).
   I treat those warnings as a representation/totality evidence gap, not as a
   separately claimed false rule: no additional false final conclusion from
   those unused cases was required or demonstrated.

7. **`gradeOf` and its 13 guarded equations (lines 99–202): structurally
   correct but oracle-dependent.** The guards mirror the exact ordered
   decision tree. They are mutually exclusive and exhaustive over Boolean
   outcomes; overlap cannot yield disagreeing results. But the A+ distinction
   remains unfixed because the equations use `eqFour/gpaEqFour`.

8. **`mappedAppend` (lines 204–213): internally valid structural fold.**
   All `NumericGrades` constructors are covered, recursion descends on `GS`,
   and Int heads use supplied `intToF`. It inherits both the opaque-equality
   defect and the synthetic-domain gap.

9. **`afterGradeValue` (lines 215–220): internally valid structural fold.**
   Its three rules are exhaustive, nonoverlapping, and descending. It likewise
   summarizes only the proof-local representation.

### Required false-conclusion witness

[`oracle-witness.k`](evidence/oracle-witness.k) adds the opposite ground
interpretation `gpaEqFour(3.9) => true`, which the candidate's opaque
declaration does not rule out. The witness programs contain the exact submitted
function:

| Semantics/program assertion | Observable result |
|---|---|
| trusted fixed semantics, assert `[3.9] -> ["A"]` | `NoExc`, exit 0 |
| trusted fixed semantics, assert `[3.9] -> ["A+"]` | `AssertionError`, exit 1 |
| candidate extension plus admitted ground interpretation, assert `["A"]` | `AssertionError`, exit 1 |
| same extension/interpretation, assert `["A+"]` | `NoExc`, exit 0 |

See
[`stage5_oracle_fixed_real.log`](evidence/stage5_oracle_fixed_real.log),
[`stage5_oracle_fixed_false.log`](evidence/stage5_oracle_fixed_false.log),
[`stage5_oracle_extended_real.log`](evidence/stage5_oracle_extended_real.log),
and
[`stage5_oracle_extended_false.log`](evidence/stage5_oracle_extended_false.log).
This witnesses the false conclusion enabled on the intended GPA domain.
Finite differential tests cannot repair the missing universal connection
theorem.

An independent body-sensitivity mutation changed the executed A+ branch from
`"A+"` to `"X"` while leaving summaries/postconditions unchanged. The mutant
definition built, and `SPEC-BODY-MUTANT.a-plus` failed with a reachable heap
containing `"X"` (`WarnStuckClaimState`, exit 1). See
[`verification-body-mutant.k`](evidence/verification-body-mutant.k),
[`stage5_body_sensitivity_build.log`](evidence/stage5_body_sensitivity_build.log),
and
[`stage5_body_sensitivity_proof.log`](evidence/stage5_body_sensitivity_proof.log).
Thus the proof is body-sensitive; its fatal defect is value connection, not
failure to execute the body.

Stage 5 result: Gate A real-program soundness failed because of the
result-bearing oracle and unjustified operational bridge. The separate
real-input representation gap also remains material.

## 6. Fresh non-vacuity test

I created a fresh claim over the satisfiable empty-input state and changed the
result-constraining heap obligation from `[]` to `["E"]`
([`spec-vacuity.k`](evidence/spec-vacuity.k)). Both trusted and candidate
Python return `[]` on that witness.

`kprove ... --dry-run` exited 0, establishing that the mutation parses and
builds. The actual proof exited 1 with `WarnStuckClaimState`; the residual
shows the reachable heap `0 |-> list(.ValSeq)`, which cannot unify with the
false destination list. This is the expected unmet result obligation, not a
parser error, timeout, or unrelated crash. See
[`stage6_vacuity_build.log`](evidence/stage6_vacuity_build.log) and
[`stage6_vacuity_proof.log`](evidence/stage6_vacuity_proof.log).

Stage 6 result: non-vacuity/discrimination test passed. It does not validate
the oracle used by other claims.

## 7. Proven versus assumed accounting

### What `#Top` actually establishes

Under the supplied semantics plus all candidate extensions and claims, the
exact submitted function body:

- returns the empty list for the real empty input;
- returns `A+` or `A` for the two real singleton regions stated in the first
  two branch claims;
- iterates the proof-only `numericValues(GS)` domain and constructs the
  proof-only mathematical summary `mappedAppend`; and
- satisfies the loop invariant over that same representation.

The result is syntactically constrained, but its A+ value is conditional on an
arbitrary interpretation of `gpaEqFour`, and the arbitrary-length input is not
the fixed-semantics real list representation. Therefore this is not a theorem
of the requested GPA mapping on arbitrary real input lists.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Entire byte-verified supplied semantics | Language execution, state, control, values | Accepted selected baseline for `SUPPLIED_SEMANTICS`; rebuilt from trusted source. |
| K primitive Int/Bool/String/Map/List operations and Float hooks | Low-level values and guards | Accepted toolchain/semantic trust boundary. |
| Supplied `gtF` and `intToF`, opaque to Haskell with concrete LLVM twins | Threshold branches and Int normalization | Acceptable named supplied primitive boundary, supported by concrete execution and differential tests; those tests remain finite evidence. |
| Candidate `gpaEqFour` | First branch, returned grade, heap, postcondition | Illegitimate. Program-derived, unconstrained, circularly reused, and falsified by the opposite-interpretation witness. |
| Candidate `numericValues` iterator extension | Domain and loop control for arbitrary-length theorem | Illegitimate as a proof of real inputs without a connection theorem; at best a theorem about a separate representation. |
| Python-to-K intent bridge | Human-facing table meaning | Empirically supported on 12,307 values, not universally proved; oracle defect shows why testing cannot substitute for the missing theorem. |
| Partial-correctness interpretation | Termination | The claims prove only partial correctness; termination is not established by reachability closure. |

Gate accounting:

- Gate A (real-program soundness): **failed**. The equality bridge admits a
  demonstrably wrong branch/result.
- Gate B (intent adequacy): **failed**. The only arbitrary-length theorem uses
  a candidate-only input representation, while real-input claims are finitely
  restricted.
- Gate C (auditability): evidence is reproducible and well preserved, but it
  cannot cure Gates A/B.

The successful reconstruction and fresh non-vacuity result are genuine but
insufficient. A proof that permits `3.9 -> A+` and does not quantify over real
arbitrary nonempty lists is not a legitimate partial-correctness proof of the
HumanEval program contract.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
