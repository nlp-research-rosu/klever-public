# Independent adversarial audit: 4-mean-absolute-deviation

The candidate is **not a legitimate proof**, despite a reproducible `#Top` and
a successful non-vacuity mutation.  The decisive defect is the priority-40
loop rewrite in `verification.k:70-86`: it replaces the real loop while
omitting the real loop's write to the loop variable `number`.  Its match admits
arbitrary continuations and pre-existing `number` bindings.  A fresh symbolic
witness is rejected by the fixed supplied semantics but proves `#Top` under
the candidate extension.  Thus the extension can prove a concretely false
state transition, and the target proof closes in a theory containing a
materially unsound operational rule.

All commands below were run against copies in
`/tmp/audit-work/4mad-review`.  Candidate files and candidate caches were not
used in place.  Exact commands, statuses, and bounded outputs are under
`/audit-output/evidence/`.

## 1. Input and provenance integrity

The rendered mode and mounts are consistent:

- Rendered mode: `SUPPLIED_SEMANTICS`.
- `/reference/reference-semantics` exists, as required.
- `diff -ru --no-dereference` between the trusted and candidate
  `reference-semantics/` trees exits 0.
- `find /candidate -type l` reports no symlinks.  Therefore there are no
  missing, additional, mistyped, changed, or symlinked entries inside the
  candidate semantics tree.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.

Evidence: `03_provenance_integrity.log` and `28_source_hashes.log`.

The required generation/provenance files are missing from `/candidate`:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`

No structured generation trace is present under either
`generation-trace.json` or `trace.json`.  There was therefore no such
untrusted generation narrative to corroborate.  This is a provenance and
auditability gap, not the basis for the candidate verdict.  The executable
source proof was independently reconstructed.  Evidence:
`02_required_untrusted_artifacts.log`.

The candidate also contains non-required `smoke.py`, `smoke.mpy`,
`prove.sh`, and `__pycache__/` files.  They were not treated as proof evidence
or reused as compiled artifacts.  The source artifacts needed for execution
were copied explicitly; see `04_scratch_copy.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From trusted `prompt.py` and `canonical.py`: for a non-empty list of Python
floats, compute the arithmetic mean, then return the arithmetic mean of the
absolute differences between each element and that mean:

`sum(abs(x - (sum(numbers) / len(numbers))) for x in numbers) / len(numbers)`.

The prompt does not expressly say “non-empty”, but the mathematical
denominators and the canonical implementation make the empty case undefined;
both Python implementations raise `ZeroDivisionError` on `[]`.  The K entry
claim explicitly excludes empty input.

### Source and translation fidelity

`solution.py` implements the same algorithm using an explicit accumulator and
`for` loop.  Its ordering of floating-point additions matches the canonical
`sum(generator)` computation.  Running the trusted translator on the scratch
copy of `solution.py` produced a file byte-identical to the submitted
`solution.mpy` (`cmp` exit 0).  Evidence:
`05_trusted_translation.log`.

### Independent differential execution

`differential_test.py` independently imports the trusted canonical entry point
and the submitted generated entry point.  It compares return values bit-for-bit
(with an explicit NaN class) and exception classes.  Its scope is:

- the documented `[1.0, 2.0, 3.0, 4.0]` example;
- empty, singleton, equal, opposite-sign, zero-deviation, positive/negative
  `abs` branch, duplicate, fractional, large, normal-minimum, and subnormal
  cases;
- infinity and NaN behavior;
- 256 deterministic uniform generated lists and 128 deterministic
  wide-exponent generated lists.

The script records seed `5062980`, 401 total inputs, and input-stream SHA-256
`074b94fde16776a223892d2920f3cb255ebce45d5c580b47cd683f6f623778de`.
There were zero mismatches.  The complete reproducible input recipe is in the
script, and all named inputs/results are in `06_differential_test.log`.

This supports program-to-canonical fidelity for the tested cases.  It is
finite evidence, not a proof.

## 3. Clean proof reconstruction

K reports version `v7.1.337`; see `00_tool_versions.log`.

Fresh source-only builds were made under
`/tmp/audit-work/4mad-review/candidate-source`:

1. Concrete definition:
   `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition concrete-kompiled`
   exited 0 (`07_concrete_build.log`).
2. `krun solution.mpy --definition concrete-kompiled` exited 0 with `.K` and
   the expected installed closure (`08_concrete_load_solution.log`).
3. Proof definition:
   `kompile verification.k --backend haskell --main-module MAD-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled`
   exited 0 (`09_proof_build.log`).

There is one positive target claim, in module `MAD-SPEC`.  The independently
run command

`kprove spec.k --definition verification-kompiled --spec-module MAD-SPEC`

exited 0 and printed `#Top`; see `10_positive_proof.log`.

The compiler's non-exhaustiveness warnings concern broad supplied-semantics
`[total]` declarations such as `mapStrVS`, `floorFI`, `toF`, `ceilF`,
`joinCodes`, and `valSeqAt`.  None of the uncovered constructors is used on
the entry claim's non-empty all-Float path.  These warnings do not explain or
excuse the proof-local unsoundness found below.

Independent concrete semantics tests were translated with the trusted
translator and run on four normal/boundary inputs.  All assertions completed,
with `krun` exit 0 and final `.K`; see `concrete_semantics_tests.py` and
`17_concrete_semantics_tests.log`.

Because this is `SUPPLIED_SEMANTICS`, no generated-semantics reconstruction
stage applies.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The sole entry claim requires `VS` to be a non-empty finite K `ValSeq` whose
elements all have sort `Float`.  It starts in the standard empty module state
with `#runMad(list(VS))`.  It claims termination with:

`divFloatIntV(absDeviationFold(VS, divFloatIntV(sumFloatSeq(VS), vsLen(VS)), 0.0), vsLen(VS))`.

In plain language, this is a left-to-right Float sum divided by sequence
length, followed by a left-to-right sum of absolute deviations from that mean,
again divided by length.  The destination also requires the call frame,
stack, heap, return state, exception state, and allocation locations to be
restored, with only the exact submitted closure installed in module scope.

The postcondition is result-constraining: it does not use a fresh result
variable, tautology, or one-way implication.  Stage 6 independently confirms
that changing it to the false constant `0.0` is rejected.

### Program pinning

`#runMad` expands `madSolution`, loads it, resolves
`mean_absolute_deviation`, and calls it.  `madSolution` is a manually embedded
AST rather than a run-time file reference, but it is exactly the AST in the
trusted regeneration of `solution.mpy`, including its docstring.  Module
loading, name lookup, argument binding, assignments, call frames, return, and
frame pop execute through the supplied semantics.

However, the call is not executed wholly by fixed semantics: the Float-list
`sum` and the entire `for` loop are preempted by proof-local priority rules.
The loop preemption is unsound, so real-program pinning fails Gate A even
though the embedded AST itself is exact.

There are no auxiliary loop claims.  `sumFloatSeq`, `sumFloatTail`, and
`absDeviationFold` are proof-local recursive functions, and their values enter
the final result directly.

### Satisfying states and concrete substitution

A standard entry configuration with

`VS = vCons(1.0, vCons(2.0, vCons(3.0, vCons(4.0, .ValSeq))))`

satisfies `nonEmptyFloats(VS)`.  The same is true for `[-1.0, 1.0]` and
`[7.25]`.  `ground_claim_check.py` concretely interprets the claim-shaped
fold, then compares it with both Python implementations:

- `[1.0, 2.0, 3.0, 4.0]`: all three bit patterns are
  `3ff0000000000000` (`1.0`);
- `[-1.0, 1.0]`: all three are `3ff0000000000000`;
- `[7.25]`: all three are `0000000000000000`.

Evidence: `16_ground_claim_check.log`.  These witnesses establish
precondition satisfiability and support the intended concrete interpretation;
they do not repair the false operational rule.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`k_rule_inventory.py` inventories every module/import, configuration, syntax
declaration, context, rule, and claim in the selected semantics,
`verification.k`, and `spec.k`.  The corrected inventory is
`k-rule-inventory.tsv`; its generation command and counts are in
`19_inventory_generation_corrected.log`.

It contains 1,116 records after the header:

- 231 syntax declarations;
- 711 rules;
- 5 evaluation contexts;
- 1 configuration;
- 1 reachability claim;
- 167 module/import/require/end-module records.

Flag-bearing records include 148 with `function`, 109 with `total`, 47 with
`priority`, 36 with `concrete`, 28 with `owise`, and 22 with
`no-evaluators`.  There are no local `functional`, `simplification`, or
`simplify` declarations.

For all 928 inventory records classified as supplied-semantics entries, the
disposition is `SELECTED_SEMANTICS_BOUNDARY`: in this mode the byte-identical
trusted tree defines the selected operational language.  This does not bless
the 20 reviewed proof-local entries in `verification.k`.  Unused supplied
constructs remain outside the program path; all constructs actually used are
mapped below.

### Used-construct map and fixed control behavior

| Submitted construct | Declaration | Relevant selected rules |
|---|---|---|
| `Module`, statement sequencing | `syntax.k:56-61` | `core.k:124-127` loads and sequences statements |
| `ImportFrom("typing", "List")` | `syntax.k:43` | `controls.k:35-44`; non-math imports are no-ops |
| `FuncDef`, `Params`, closure | `syntax.k:53,57` | `functions.k:8-13`; module scope receives an exact closure |
| docstring `Expr(Str(...))` | `syntax.k:13,52` | `str.k:13-17`, `controls.k:48`; literal evaluates, then is discarded |
| `Name`, assignment | `syntax.k:12,41` | `core.k:130-154` performs scope-chain lookup; `controls.k:9-31` performs `Assign`/`AugAssign` state writes |
| `Call`, arguments, frames | `syntax.k:28` | `core.k:185-191` and `call.k:14-31` evaluate callee then arguments left-to-right; `call.k:64-83` and `functions.k:63-90` bind, call, return, and pop |
| `BinOp`, Float literal and arithmetic | `syntax.k:10,15` | `operators.k:7-13`; `float.k:20-56,103-113,189-196` routes Float literal, subtraction, absolute value, addition, division, and promotion |
| `For` over `list(VS)` | `syntax.k:45` | `controls.k:63-74`, `list.k:8-9`, and `tuple.k:31-40` iterate, bind `number`, execute the body, and repeat |
| `Return` | `syntax.k:50` | `functions.k:77-90` sets `retV`, restores continuation/environment, and removes the callee scope |
| `len` and `sum` | builtins registry `core.k:157-181` | `builtins.k:17-29,47-56`, `call.k:25-31`, and Float sum continuation `float.k:257-272` |

The fixed rules establish ordinary call/return control and state changes.
`seqstrict`/`strict` plus `#evalArgs` enforce evaluation order.  The list input
is already an unboxed `list(VS)`, so the proof path performs no list
allocation.  The function's plain call frame is allocated at scope 1 and
removed at return.  The real `for` loop writes both `number` and
`total_deviation` in that frame on every iteration.

### Proof-local declarations and rules

The exact proof-local records are inventory rows 1091-1110:

- `madSolution [function,total]` and its equation: exact AST constant;
  terminating, covered, and non-overlapping.
- `#runMad`: exact load-then-call harness; it does not introduce abrupt
  control or fabricate a result.
- `allFloats` and `nonEmptyFloats [function,total]`: constructor-complete.
  Float-head and `owise` non-Float-head cases are disjoint.
- `sumFloatSeq`, `sumFloatTail`, and `absDeviationFold`: structurally
  recursive definitional summaries.  On the guarded all-Float domain, every
  recursive call consumes one `vCons`; base and step rules are disjoint and
  cover all uses.  They are not declared total, and non-Float cases are not
  used.
- The sum operational bridge and loop operational bridge, reviewed
  separately below.

#### Float-list `sum` bridge

`verification.k:64-68` matches the already-resolved value
`builtinV("sum")` at `#applyK`, after argument evaluation.  It requires a
non-empty all-Float list and replaces the fixed iterator fold with
`sumFloatSeq(VS)`.  The defining equations preserve Python's integer-zero
start by applying `intToF(0)` at the first Float addition and then fold
left-to-right.  Fixed sum changes only `<k>` on this unboxed list, so the
arbitrary continuation frame does not omit an observable state effect.

No bridge-free, machine-checked universal connection claim was supplied.
The correspondence follows by a straightforward induction over `VS` from
the fixed `#sumAcc/#sumCont/#sumAccF/#sumContF` rules and is supported by the
concrete and differential tests.  Because there is no false conclusion
witness for this guarded bridge, it is classified as a sound-on-guard
connection-evidence gap, not as unsound.

#### `for`-loop bridge: materially unsound

`verification.k:70-86` matches:

`#loop(list(VS), Name("number"), AugAssign(...))`

under an arbitrary continuation (`...`).  It requires non-empty all-Float
`VS`, a current scope containing Float `mean` and Float
`total_deviation`, and then:

- rewrites the whole loop to `.K`;
- updates `total_deviation` to `absDeviationFold(...)`;
- preserves every other map binding and every other cell.

This does **not** match the fixed semantics' state footprint.
`controls.k:68-73` calls `#bindTgt` before each body execution, and
`tuple.k:32-40` writes `number` in the current scope.  For non-empty `VS`,
fixed execution therefore leaves `number` bound to the last Float.  The
candidate bridge leaves `number` absent or preserves an arbitrary old value.
Its guard also does not pin the lookup binding of `abs`, another context
containment gap, but the `number` omission alone has a complete false
conclusion witness.

Fresh witness files:

- `loop-side-effect-fixed.k`
- `loop-side-effect-extended.k`

Both begin with a one-element all-Float list, Float `mean` and accumulator,
and an old Float binding `number = OLD`.  Both deliberately claim that the
loop updates only the accumulator while preserving `OLD`.  A concrete
satisfying substitution is:

`F=2.0, OLD=9.0, MEAN=2.0, ACC=0.0`.

The same transition under fixed supplied semantics:

`kprove ...loop-side-effect-fixed.k --definition fixed-haskell-kompiled --spec-module LOOP-SIDE-EFFECT-FIXED`

exits 1 with `WarnStuckClaimState`.  Its residual explicitly shows the actual
state `number |-> F` and the unmet implication `F #Equals OLD`; see
`14_loop_side_effect_fixed_symbolic.log`.

The false transition under the candidate-extended definition:

`kprove ...loop-side-effect-extended.k --definition verification-kompiled --spec-module LOOP-SIDE-EFFECT-EXTENDED`

exits 0 and prints `#Top`; see
`15_loop_side_effect_extended_symbolic.log`.

This is a symbolic false-conclusion witness with the concrete satisfying
instance above.  It is not a parser failure, timeout, or ungrounded
speculation.  It directly demonstrates that the priority rule can prove a
state transition contradicted by fixed execution on the intended non-empty
Float-list domain.

The submitted function happens not to read `number` after the loop, and its
frame is later popped.  That does not validate the rule: its ellipsis admits
arbitrary observable continuations, and a globally false operational bridge
cannot be justified by one dead-variable context.  No bridge-free universal
connection theorem narrows it to the exact submitted continuation or proves
the omitted state irrelevant.

As a dependency diagnostic, removing only this loop rule leaves the target
at the symbolic `#iterNext/#loopStep` state and the submitted proof no longer
closes (`21_no_loop_diff.log` and `23_no_loop_positive_proof.log`).  That
diagnostic eventually encounters the Haskell backend's absent concrete
`Int2Float` hook, so it is not used as the unsoundness witness; the clean
fixed-versus-extended witness above is decisive.

Two earlier ground-literal witness attempts (`12_...` and `13_...`) likewise
encountered an unavailable Haskell `FLOAT.sub` hook.  They are retained for
transparency but excluded from the verdict evidence.  The corrected symbolic
witness avoids that infrastructure limitation and yields the required
fixed-semantics residual versus candidate `#Top`.

### Stage 5 conclusion

The loop bridge is an operational shortcut with a false state footprint and
uncontained continuation context.  It makes a false reachability claim
provable.  Therefore Gate A fails, independently of the fact that the target
postcondition describes the right numerical result.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present.  A fresh mutation was created in
scratch and preserved as `evidence/spec-vacuity-fresh.k`.  It changes only the
result-bearing destination of the entry claim to `0.0`.  This is false for the
satisfying documented input `[1.0, 2.0, 3.0, 4.0]`, whose result is `1.0`.

The dry run:

`kprove spec-vacuity-fresh.k --definition verification-kompiled --spec-module MAD-SPEC-VACUITY-FRESH --dry-run`

exited 0, demonstrating successful parsing/building
(`26_vacuity_dry_run.log`).

The actual proof command exited 1 with `WarnStuckClaimState`.  The residual
shows the unmet equality between `0.0` and the original fold-shaped returned
value; see `27_vacuity_proof.log`.  This is the expected unmet
result obligation, not an unrelated failure.

The target claim is therefore non-vacuous and result-constraining.  Passing
this gate does not cure the unsound operational theory used to obtain its
positive `#Top`.

## 7. Proven-versus-assumed accounting

### What the successful reachability run establishes

Under the combined theory consisting of the selected supplied semantics plus
all rules in `MAD-VERIFICATION`, `kprove` establishes that every non-empty
all-Float symbolic `VS` starting in the exact entry configuration reaches the
fold-shaped result and restored caller state.

That statement is only a theorem of the combined theory.  Since the combined
theory contains the false loop transition above, it is not a legitimate
partial-correctness proof of the real fixed-semantics program.

### Trust ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| Trusted prompt, canonical implementation, and translator | Defines intent, executable oracle, and source-to-`.mpy` bridge | Acceptable trusted input; byte comparisons and hashes pass |
| Entire supplied `reference-semantics/` tree | Defines syntax, configuration, control, state, calls, and primitives | Required selected-semantics boundary; candidate copy is exact |
| K builtin theories/hooks imported by the supplied semantics (`INT`, `BOOL`, `STRING`, `MAP`, `LIST`, `K-EQUAL`, `FLOAT`) | Low-level mathematical and concrete execution primitives | Acceptable selected-semantics/toolchain boundary |
| Proof-relevant opaque Float symbols `intToF`, `addF`, `subF`, `absF`, `divFloatIntV` | Construct the mean and deviation result | Acceptable fixed external primitive boundary for a structural theorem; LLVM concrete rules and tests support their Python interpretation, but Haskell does not prove IEEE algebra |
| Other supplied symbolic/opaque symbols | Listed below; unused by this claim | Do not affect target closure, but remain part of the broad selected semantics |
| `sumFloatSeq`, `sumFloatTail`, `absDeviationFold` | Proof-local fold summaries in result and bridges | Equations are terminating, disjoint, and complete on every guarded use |
| Priority-40 `sum` bridge | Replaces fixed builtin execution | Structurally credible on its guard, but supported only by informal induction and finite concrete evidence; no universal K connection claim |
| Priority-40 loop bridge | Replaces real loop and supplies the final accumulator | Illegitimate: false state footprint, arbitrary continuation, no connection theorem, and machine-checked false-conclusion witness |
| Exact embedded `madSolution` AST | Connects entry harness to submitted program | Byte-identical trusted regeneration supports the bridge; the loop is nevertheless preempted |
| Python differential tests and LLVM assertions | Empirical source/canonical and concrete-semantics evidence | Finite support only; not a replacement for the K proof or a bridge theorem |
| Informal arithmetic interpretation | Identifies the fold-shaped term as mean absolute deviation | Sound as ordinary left-fold mathematics conditional on the supplied Float primitive interpretation; ground cases agree |

The complete supplied-symbol inventory is in `k-rule-inventory.tsv`.  The
symbols explicitly marked `symbol(...)` are:

- Float/support: `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
  `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
  `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
  `roundFN`, and `sqrtF`;
- other supplied domains: `md5hexCodes`, `sortVS`, and `sortKeyVS`;
- proof-local, equation-defined symbols: `sumFloatSeq`, `sumFloatTail`, and
  `absDeviationFold`.

Of those, `md5hexCodes`, the 19 Float symbols carrying `no-evaluators`, and
the two sort symbols are explicitly opaque to the symbolic backend.
`floorFI`, `toF`, and `ceilF` have only concrete equations for their covered
sort cases.  Only `intToF`, `addF`, `subF`, `absF`, and `divFloatIntV` are
result-bearing for this proof.  Their opacity is not circular: they are fixed
external arithmetic primitives and the theorem remains structural in them.
The illegitimate circularity is instead the program-defined loop computation
being replaced by an over-broad operational rule.

### Decision

Fresh reconstruction confirms that the submitted positive claim is
syntactically well formed, non-vacuous, result-constraining, and empirically
aligned with the canonical Python function.  Those facts cannot substitute
for sound execution.  The proof-local loop bridge demonstrably proves a
false state transition and is used to bypass the real symbolic loop.  This
meets the decision criterion for a materially unsound proof rule.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
