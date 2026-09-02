# Independent adversarial audit: 81-numerical-letter-grade

The candidate is **not a legitimate proof of the submitted program**. The
submitted positive claims do reconstruct to `#Top`, and a fresh false-result
mutation is rejected, but the successful proof depends on two decisive defects:

1. `spec.k` never loads or executes `solution.mpy`. `runGrades` constructs a
   closure around a separately copied K macro body. A scratch mutation changed
   the submitted program's `A+` branch to `Z`; after regenerating the mutated
   `solution.mpy` and freshly rebuilding the unchanged verification source, all
   claims still printed `#Top`.
2. `verification.k:72-75` preempts the supplied Float-equality semantics with
   an unconstrained, total, opaque Boolean `gpaEqFour`. The same symbol is used
   by execution and by `gradeOf`, so the proof is circular in exactly the
   result-bearing fact it needs. There is no bridge-free connection theorem.
   The candidate theory admits the opposite interpretation at the real input
   `4.0`, allowing the copied program to take the `"A"` branch even though
   Python and the fixed concrete semantics return `"A+"`.

The universal claim has a third adequacy defect: it quantifies over a fresh
`numericValues(NumericGrades)` constructor and gives that constructor custom
iterator rules. No theorem connects those artificial terms to ordinary concrete
`vCons` lists.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` tree is present, so the mount agrees with the
rendered mode; this is not an infrastructure breach.

The reviewer inspected all candidate entries with `lstat`-style type checks.
The required proof/source artifacts that are present are ordinary files or
directories, not symlinks. The candidate prompt and translator are byte
identical to their trusted versions:

- `prompt.py`: SHA-256
  `489ff1f658e105a21a1e28c105082983a77af3a6b0576d9cdfb43745de1b507c`
- `py2mpy.py`: SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

The candidate `reference-semantics/` and trusted tree have exactly the same 25
recursive entries, types, and bytes. There are no missing, extra, changed,
mistyped, or symlinked semantics entries. This integrity match fixes the
selected baseline; it does not validate the proof-local rules in
`verification.k`.

Four requested provenance artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace is present. These are provenance deficiencies,
not a malformed trusted mount and not the basis of the candidate verdict.

Evidence:

- `evidence/check-integrity.py`
- `evidence/01-integrity.log` (exit 0, tree and trusted-file matches)
- `evidence/26-source-manifest.log` (complete source hashes)

All builds and experiments used source copied to
`/tmp/audit-work/audit-src` or a dedicated mutation directory. No
candidate-provided compiled definition or cache was reused.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a list of numeric GPAs, return one letter per input, preserving order. The
top grade is `A+` exactly at `4.0`. The remaining branches use strict
greater-than thresholds:

| Condition in order | Result |
|---|---|
| `gpa == 4.0` | `A+` |
| `gpa > 3.7` | `A` |
| `gpa > 3.3` | `A-` |
| `gpa > 3.0` | `B+` |
| `gpa > 2.7` | `B` |
| `gpa > 2.3` | `B-` |
| `gpa > 2.0` | `C+` |
| `gpa > 1.7` | `C` |
| `gpa > 1.3` | `C-` |
| `gpa > 1.0` | `D+` |
| `gpa > 0.7` | `D` |
| `gpa > 0.0` | `D-` |
| otherwise | `E` |

Thus equality at a non-4.0 threshold falls to the next lower band. The trusted
example `[4.0, 3, 1.7, 2, 3.5]` maps to
`["A+", "B", "C-", "C", "A-"]`.

### Source and translation

`solution.py` implements that branch order. It additionally coerces each input
with `float`. Over the intended ordinary Int/Float GPA domain this agrees with
the canonical implementation. The K theorem's own proposed domain is likewise
limited to Int and Float grade constructors; it does not cover arbitrary Python
numeric objects.

Regeneration used the trusted translator, not the candidate copy:

```text
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

The command exited 0. Both `.mpy` files have SHA-256
`2e6aceeafbf0e72ac3bfbee3a9799161afeab018bacc859f63f56b0f2c1fe7cd`.
See `evidence/02-translation-identity.log`.

### Independent differential test

`evidence/differential_test.py` separately imports
`/reference/canonical.py` and the scratch copy of `solution.py`. It tested:

- the documented example and the empty list;
- integer inputs `0` through `4`;
- immediately lower, exact, and immediately higher IEEE-754 values for all 12
  branch thresholds;
- range edges from `-1.0` through `5.0`;
- deterministic generated lists of lengths 1, 2, 5, 16, 64, and 257, with
  values uniformly sampled from `[0.0, 4.0]` using seed `810081`.

There were 11 list cases containing 397 scalar inputs and zero mismatches.
Exact inputs are preserved in `evidence/differential-inputs.json` (SHA-256
`68440171d704fdd67d172fda3ffffca5c9c8513f20f23d34bd01d1686a24cdd7`);
the command and exit 0 are in `evidence/03-differential.log`.

This finite evidence supports the Python rewrite-to-canonical bridge on the
tested domain. It is not a K proof and does not connect `gpaEqFour` to Float
equality.

## 3. Clean proof reconstruction

K was independently available as version `v7.1.337`.

### Concrete definition

The supplied semantics was freshly compiled with LLVM:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit was 0 (`evidence/04-kompile-runtime.log`). The compiler reported several
fixed-semantics non-exhaustive-totality warnings (`mapStrVS`, `floorFI`, `toF`,
`ceilF`, `joinCodes`, and `valSeqAt`). None is on this program's executed path.
They belong to the selected supplied baseline.

Fresh execution of the submitted smoke harness ended with `.K`, `NoExc`, and
exit code 0. The assertions cover the empty list, the documented example, and
all grade branches (`evidence/05-krun-smoke.log`). A separate fixed-semantics
test concretely confirmed `[4.0] -> ["A+"]` and `[3.8] -> ["A"]`
(`evidence/oracle-fixed-semantics.py`,
`evidence/14-oracle-fixed-translate.log`, and
`evidence/15-oracle-fixed-krun.log`).

### Proof definition and claims

The Haskell proof definition was freshly built from `verification.k`:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Exit was 0 (`evidence/06-kompile-verification.log`).

Positive reconstruction results:

| Claim/run | Result | Evidence |
|---|---|---|
| `SPEC.empty` | exit 0, `#Top` | `07-kprove-empty.log` |
| `SPEC.a-plus` | exit 0, `#Top` | `08-kprove-a-plus.log` |
| `SPEC.a` | exit 0, `#Top` | `09-kprove-a.log` |
| `SPEC.loop-maps-all-numeric-grades` | exit 0, `#Top` | `11-kprove-loop-map.log` |
| universal function claim together with its loop circularity | exit 0, `#Top` | `12-kprove-function-with-loop.log` |
| all five submitted claims | exit 0, `#Top` | `13-kprove-all.log` |

The universal function claim was also tried after filtering out its loop
invariant. It produced no prover output for approximately 90 seconds and was
interrupted with status 130 (`10-kprove-function-map.log`). That diagnostic is
not treated as a failed submitted proof: the loop claim is its explicit
circularity, was independently shown to close, and the intended combined and
aggregate proof runs both closed.

Fresh reconstruction therefore verifies closure under the submitted extended
theory. It does not establish that the extension is sound.

## 4. Adequacy and real-program pinning

### Plain-language claims

| Claim | Precondition | Postcondition |
|---|---|---|
| `empty` | Initial module/builtins scopes, no heap objects, input sequence empty | Return `ref(0)` to a newly allocated empty list; heap location advances from 0 to 1 |
| `a-plus` | Same initial state, one Float `F`, and `eqFour(F)` | Return `ref(0)` to a one-element list containing `A+` |
| `a` | Same initial state, one Float `F`, `not eqFour(F)`, and `above(F,3.7)` | Return `ref(0)` to a one-element list containing `A` |
| `function-maps-all-numeric-grades` | Same initial state and an invented `numericValues(GS)` sequence; no explicit logical guard | Return `ref(0)` to a list equal to `mappedAppend(.ValSeq,GS)` |
| `loop-maps-all-numeric-grades` | Function frame 1; result list at heap 0; invented remaining iterator `numericValues(GS)`; heap fragment `HP` lacks key 0 | Consume the loop, append `mappedAppend(PREFIX,GS)`, update `grade` to the final converted grade (or preserve `OLD` if empty), then continue with the exact incoming `CONT` |

The destination values are syntactically constrained. They are not free RHS
variables or tautological implications. The loop continuation is an LHS
variable and is preserved. Omitted `<exc>` and `<exit-code>` cells are framed
and are not postconditioned.

The following satisfying ordinary input witnesses agree between both Python
implementations (`evidence/22-claim-witnesses.log`):

- `empty`: `[] -> []`
- intended witness for `a-plus`: `[4.0] -> ["A+"]`
- intended witness for `a`: `[3.8] -> ["A"]`
- universal empty case: `[] -> []`
- universal mixed case:
  `[4.0, 3, 1.7, 0] -> ["A+", "B", "C-", "E"]`

For the formal `a-plus` and `a` claims, however, satisfiability is relative to
the arbitrary interpretation of `gpaEqFour`. That predicate is not equality.
The loop claim has a simple formal witness with `GS=.NumericGrades`,
`HP=.Map`, `PREFIX=.ValSeq`, `OLD=0.0`, and an otherwise well-formed frame; its
side condition holds because key 0 is absent from `HP`.

### Failure to pin `solution.mpy`

The entry `<k>` term is `runGrades(...)`, not the submitted `Module(...)`.
`verification.k:59-63` rewrites it to a call of
`closureVal("grades", numericalLetterGradeBody, 0)`.
`numericalLetterGradeBody` and `numericalLetterGradeStep` are separate
proof-local macros. They structurally match the current submitted function
body, but the proof has no import, parse, hash guard, or connection claim for
`solution.mpy`. Module loading and `FuncDef` execution are bypassed.

The body-sensitivity experiment is decisive:

1. In `/tmp/audit-work/pinning-mutant`, the submitted branch
   `result.append("A+")` was changed to `result.append("Z")`.
2. The trusted translator regenerated an `.mpy` containing `Str("Z")`; the
   mutant `.mpy` hash is
   `fe0f1b56af5f2a2355fbeece14d3243e640afdec5035b2eea4e862b086281e9c`.
3. The unchanged `verification.k` and supplied semantics were freshly
   compiled.
4. All five claims still exited 0 and printed `#Top`.

See `evidence/pinning-mutation.diff`,
`19-pinning-mutant-translation.log`,
`20-pinning-mutant-kompile.log`, and
`21-pinning-mutant-kprove-all.log`. The successful proof is therefore
insensitive to the submitted program artifact.

### Universal-domain failure

Concrete list contents in this semantics are `.ValSeq` and
`vCons(Val,ValSeq)`. The universal entry claim instead supplies the fresh term
`numericValues(GS)` as a `ValSeq`, and proof-local priority rules fabricate its
iterator behavior. There is no bridge-free claim proving that execution over
an arbitrary concrete numeric `vCons` list corresponds to a
`numericValues(GS)` term. The only claims over ordinary list syntax are empty
and two one-element conditional cases. Consequently, even apart from the
equality oracle, the universal theorem is about an artificial input
representation rather than all actual numeric input lists.

Adequacy/real-program pinning fails.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/rule_inventory.py` inventories every K declaration block and records
its complete text, source hash, lines, kind, attributes, decision, and
rationale. The generated artifacts are:

- `evidence/rule-inventory.csv` — compact one-row-per-declaration review
- `evidence/rule-inventory.json` — full declaration blocks
- `evidence/23-rule-inventory.log` — counts and zero unmapped candidate entries

The inventory covers 26 K files and 1,140 declaration records:

- 724 rules: 695 in the fixed supplied semantics and all 29 in
  `verification.k`;
- 238 syntax declarations: 227 fixed and all 11 proof-local declarations;
- five submitted claims;
- the fixed configuration, five contexts, all modules/imports/requires, and
  module endings.

It flags all 157 `[function]`, 116 `[total]`, 26 `[symbol]`, 23 opaque
`[symbol,no-evaluators]`, 53 priority, 58 concrete, 30 `owise`, and seven macro
declaration blocks. There are no `[functional]` declarations and no
`[simplification]` rules.

Every fixed-semantics record is adjudicated as the byte-identical selected
supplied baseline. This is the semantics level against which proof-local
extensions must be checked. The mapping from every syntax construct actually
used by `solution.mpy` to declaration and execution rules is in
`evidence/used-construct-map.md`.

### Configuration, evaluation, control, and state

The fixed configuration has `<k>`, environment/scopes, heap/allocation
location, call stack, return state, exception, and exit-code cells. On the
duplicated body:

- expressions and call arguments evaluate left-to-right;
- name lookup and assignment use the active function frame;
- `float` conversion dispatches through the builtins scope;
- ordinary concrete lists use the fixed iterator protocol;
- `If` consumes a Boolean truth value and selects one branch;
- `append` mutates the heap list in place;
- `Return` stores the value, pops the frame, restores the caller, and leaves
  the returned reference in `<k>`.

The local equality and synthetic-iterator bridges rewrite only the front of
`<k>` and frame the rest of the configuration. They do not directly corrupt
heap or stack state. Their problem is value/domain fidelity, not an observed
cell-write mismatch.

### Candidate-local declarations and rules

All 29 rules have individual decisions in the inventory. Grouped findings are:

1. **Copied-body macros (`verification.k:8-56`) and `runGrades`
   (`:59-63`).** The macro expansions match the current function body, and
   subsequent execution uses fixed call/control/state rules. Nevertheless,
   this is a substituted program entry with no machine-checked source
   connection. The mutation witness in Stage 4 proves body insensitivity.
   This is a pinning failure, not a claim that the macro equation itself is
   mathematically false for its current expansion.

2. **`letter` (`:65-66`).** Truthful and total: it names the fixed
   string-code representation.

3. **Equality oracle and bridge (`:68-76`).**
   `gpaEqFour(Val)` is declared `[function,total,symbol(gpaEqFour),
   no-evaluators]` and has no defining or concrete rule.
   The priority-40 bridge
   `Compare(F, CmpOp("==",4.0)) => gpaEqFour(F)` preempts the fixed path
   `Compare -> applyCmp -> F ==Float 4.0`. `eqFour(F)` is merely an alias back
   to the same oracle. There is no bridge-free universal connection theorem,
   no exhaustive truthful equation, and no external primitive contract.

   **False-conclusion witness:** choose the intended input `F=4.0` and the
   admitted interpretation `gpaEqFour(4.0)=false`. Ordinary Float comparison
   and the supplied concrete semantics give `4.0 == 4.0 = true`, while the
   bridge yields false. Since `4.0 > 3.7`, the copied program then takes the
   `"A"` branch rather than `"A+"`.

   Machine evidence preserves both sides:

   - fixed LLVM execution gives `[4.0] -> ["A+"]`
     (`15-oracle-fixed-krun.log`);
   - under symbolic conditions
     `gpaEqFour(F)=false` and `gtF(F,3.7)=true`, the candidate theory proves
     output `"A"` (`spec-oracle-opposite.k`,
     `17-oracle-symbolic-wrong-result-provable.log`, exit 0 and `#Top`);
   - under the same condition, requiring `"A+"` is stuck, and its residual
     explicitly retains both satisfiable predicate constraints
     (`spec-oracle-opposite-check.k`,
     `18-oracle-symbolic-real-result-rejected.log`, exit 1).

   A direct ground Haskell attempt reached an unsupported `FLOAT.gt` hook and
   exited 113 (`16-oracle-wrong-result-provable.log`). That backend limitation
   is not used as verdict evidence; the fixed LLVM run and symbolic opposite
   interpretation supply the required witness.

4. **`above` (`:68-77`).** This is an exact alias to the fixed supplied
   primitive `gtF`. It is acceptable only as the selected semantics'
   conditional primitive boundary. Unlike `gpaEqFour`, program execution
   reaches `gtF` through the fixed comparison dispatch.

5. **Synthetic numeric sequence and iterator rules (`:82-97`).** The three
   cases are constructor-disjoint, priority does not overlap the fixed
   `.ValSeq`/`vCons` cases, and their head/tail behavior is internally
   list-like. However, fixed semantics has no meaning for the new
   `numericValues` constructor, and no connection theorem relates it to real
   lists. The narrower conclusion is an unconnected abstraction/adequacy gap;
   these equations are not labeled globally false on their fresh synthetic
   datatype.

6. **`gradeOf` (`:99-203`).** The 13 rules mirror the nested threshold order.
   Their guards are pairwise exclusive by construction, and later guards add
   every earlier negation. The function is not declared total. Relative to
   arbitrary `gpaEqFour` and fixed opaque threshold predicates, these rules
   consistently summarize the copied branches. They do not establish the real
   task mapping: the same `F=4.0`, oracle-false witness derives
   `gradeOf(4.0)="A"` instead of `"A+"`.

7. **`mappedAppend` (`:204-213`).** The three constructor cases are exhaustive
   over `NumericGrades`, disjoint, and structurally descending. The recurrence
   is mathematically sound as a map of `gradeOf`, but its values inherit the
   equality oracle and the datatype lacks a real-list connection.

8. **`afterGradeValue` (`:215-220`).** The cases are exhaustive, disjoint, and
   structurally descending. They truthfully preserve the old loop variable for
   empty input and otherwise compute the final converted grade.

### Overlaps, priorities, and totality

- The harmful overlap is deliberate: local priority 40 makes the
  `gpaEqFour` rule win over fixed generic comparison dispatch. Priority changes
  which rule executes; it supplies no equivalence proof.
- The three local iterator priority rules match only the fresh
  `numericValues` form, not fixed concrete list constructors.
- `letter`, `eqFour`, `above`, `mappedAppend`, and `afterGradeValue` cover their
  declared argument sorts syntactically. Totality of opaque `gpaEqFour` merely
  gives it an arbitrary Boolean interpretation and does not prove equality.
- Local recursion descends on `NumericGrades`; there is no local
  simplification interaction.
- The loop body contains no abrupt return, break, exception, allocation other
  than initial list creation, or cleanup effect that the loop circularity
  silently drops. `CONT` is preserved. The decisive local bridge is still
  unsound because it changes a branch-controlling value.

Gate A real-program soundness fails on the equality bridge and source pinning.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`. The reviewer created
`evidence/spec-vacuity.k`, changing the empty-input result obligation from the
true empty list to the demonstrably false one-element list `["E"]`.

The witness input is `[]`; both Python implementations return `[]`
(`22-claim-witnesses.log`). The mutation was copied to scratch.

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

This exited 0 and emitted a valid backend command
(`24-vacuity-dry-run.log`), establishing that the mutation parsed and built.
The actual proof command exited 1 with `WarnStuckClaimState`
(`25-vacuity-proof.log`). The residual final heap contains
`0 |-> list(.ValSeq)`, directly showing the unmet result obligation rather than
a parser error, missing import, timeout, or unrelated crash.

The proof is therefore non-vacuous and result-discriminating for this claim.
This positive fact does not repair the unsound theory or substituted program.

## 7. Proven versus assumed accounting

### What `#Top` actually establishes

Under the supplied semantics plus all proof-local rules, and conditional on
arbitrary interpretations of imported opaque primitives and the local
`gpaEqFour` symbol:

- the separately copied body returns an empty list for empty input;
- it returns `A+` or `A` for the respective one-element abstract-predicate
  preconditions;
- over the invented `numericValues(NumericGrades)` iterator, it returns a list
  described by `mappedAppend`;
- the submitted loop invariant summarizes heap append and the final loop
  variable for that invented iterator.

This is a partial-correctness result: it constrains terminating executions. It
does not prove that the candidate's equality oracle means equality, that the
synthetic iterator represents every concrete list, or that the theorem's body
is loaded from the submitted `solution.mpy`.

### Trust ledger

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| Byte-identical supplied semantics and K built-in Int/Bool/String/Float/Map/List hooks | All concrete and symbolic execution | Accepted as the rendered fixed semantics level; freshly rebuilt rather than trusting caches |
| Fixed opaque `gtF` with a `[concrete]` twin | Every strict threshold in execution and `gradeOf`; branch control and final result | Acceptable selected-semantics primitive boundary, but the human-intent bridge remains conditional and finitely tested |
| Fixed opaque `intToF` with a `[concrete]` twin | Conversion of Int grades; `mappedAppend` and `afterGradeValue` | Same conditional boundary; concrete K/Python tests support tested values |
| Local opaque `gpaEqFour` with no equations or concrete twin | First branch in execution, `eqFour`, all `gradeOf` rules, every nonempty universal result | Illegitimate program-derived oracle; circular and refuted by the opposite-interpretation witness |
| Proof-local `numericValues` iterator rules | Universal entry theorem and loop invariant | Illegitimate as a theorem about real lists without a bridge-free concrete-list connection |
| Copied macros and `runGrades` | Every claim | Illegitimate source-artifact pinning; proof remains `#Top` after a material `solution.mpy` mutation |
| Manual statement that current macros structurally match the current function body | Only an informal current-version bridge | Verified by static comparison, but not machine-pinned and disproved as a dependency by mutation |
| Python differential testing (397 scalar inputs) | Candidate Python to trusted canonical intent bridge | Useful finite evidence only; no support for the K equality oracle |
| Fixed-semantics smoke and isolated K tests | Concrete behavior of supplied semantics on recorded examples | Useful finite evidence only; runtime definition does not import the proof-local oracle |

The remaining imported opaque symbols are not reachable from this submitted
program/proof path: `sortVS`, `sortKeyVS`, `intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `eqF`,
`decStrToF`, `divFloatIntV`, `truncF`, `roundF`, `roundFN`, `sqrtF`, and
`md5hexCodes`. They remain part of the selected semantics' broad trust boundary
but have no dependent candidate claim here.

The formal domain also excludes non-Int/non-Float elements, Python object
coercion behavior, and related exceptions. Differential evidence does not turn
those exclusions or any opaque symbol into a universal theorem.

### Decision

Fresh `#Top` and non-vacuity are real, but they prove a copied program under an
extended theory that can change `4.0 == 4.0` into an arbitrary Boolean, and the
universal claim ranges over an unconnected synthetic list representation. The
required real-program soundness and pinning gates fail. These are candidate
defects with explicit witnesses, not audit infrastructure uncertainty.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
