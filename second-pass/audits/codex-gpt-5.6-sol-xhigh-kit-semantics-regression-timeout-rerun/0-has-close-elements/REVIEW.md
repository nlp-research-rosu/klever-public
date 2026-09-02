# Independent adversarial audit: 0-has-close-elements

## Outcome

The candidate contains a legitimate partial-correctness proof of the generated
program under the supplied MPY semantics. I independently rebuilt every
definition from source, reran all four positive claims, audited every
candidate-authored proof rule, checked both operational bridges against
bridge-free definitions and observable continuations, and rejected a fresh
false result mutation for the expected unmet obligation.

The final status is **PASS / LEGIT**. The proof is conditional on the explicitly
supplied MPY semantics, its opaque Float primitives, the trusted translator, and
the K toolchain. Those are normal and disclosed boundaries for
SUPPLIED_SEMANTICS mode; no candidate rule smuggles a correctness conclusion
across them.

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` directory is present, so the mount does not
contradict the rendered mode. The candidate has a
`/candidate/reference-semantics` directory with the same 24 entries. Recursive
`diff --no-dereference -rqs` reported every file identical and exited 0. Both
trees contain only regular files and directories. No symlink exists anywhere
under `/candidate`, and neither semantics tree has a special filesystem entry.

The candidate therefore passes the condition-aware semantics integrity gate.
This establishes provenance of the fixed semantics only; it does not bless
candidate rules in `verification.k`.

### Required artifacts and untrusted generation evidence

The following required candidate artifacts are present and regular files:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `verification.k`,
`spec.k`, `prove.sh`, and `PROOF.md`. One structured trace is present:
`codex-trace/2026/07/23/rollout-...jsonl`; all 1,420 lines parse as JSON. The
5,395,764-byte generation log and the trace were treated only as claims. They
claim four `#Top` results, a `VALIDATED` report, and zero differential
mismatches, but none of those claims was reused as proof evidence.

Candidate-built `runtime-kompiled`, `verification-base-kompiled`,
`verification-inner-kompiled`, `verification-kompiled`, `__pycache__`, logs,
and traces were not copied into the audit build and were never supplied to K.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`:
SHA-256
`00b2e074e127a6a9d1376278bef732933760ab706057ec755a8c2642217b557a`.
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`:
SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
There are no missing, changed, extra, mistyped, or symlinked entries in the
required candidate semantics tree.

Evidence: [stage1 script](/audit-output/evidence/stage1_integrity.sh),
[integrity log](/audit-output/evidence/stage1-integrity.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract and canonical behavior

The trusted prompt asks whether a `List[float]` contains two distinct positions
whose values are strictly closer than a Float threshold. The trusted canonical
implementation enumerates every ordered pair of indices, ignores equal
indices, and returns `True` as soon as
`abs(numbers[i] - numbers[j]) < threshold`; otherwise it returns `False`.

The candidate implementation scans all unordered pairs using `i < j`. It does
not return early: it initializes `result = False`, sets it to `True` for any
close pair, never resets it, and returns it after both loops. This is a
different control strategy but the same Boolean algorithm over the annotated
domain.

### Trusted regeneration

In the clean scratch directory I ran:

```text
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
```

The command exited 0. `regenerated-solution.mpy` and the scratch copy of the
submitted `solution.mpy` are byte-identical, both with SHA-256
`11fe46f0b302e79be6c8d42b04df01617944d424796b7e96605eb4ec24274ada`.

### Independent differential test

The reviewer-authored test imports the trusted canonical and candidate entry
points as separate modules. Its 12,903 inputs include:

- both documented examples;
- empty and singleton lists;
- both outcomes of `i < j`;
- exact, immediately-inside, and immediately-outside strict-distance
  thresholds;
- duplicates, signed zero, negative thresholds, negative elements, NaN, and
  infinities;
- every list of lengths 0 through 4 over
  `{-2.0, -0.5, -0.0, 0.0, 0.5, 2.0}` at seven thresholds;
- 2,000 deterministic seeded random cases of lengths 0 through 9.

Both true and false result paths were exercised (7,999 true and 4,904 false).
There were zero mismatches and no divergent exceptions. This is finite bridge
evidence, not a replacement for the K proof.

Evidence: [fidelity script](/audit-output/evidence/stage2_fidelity.sh),
[differential program](/audit-output/evidence/differential_audit.py),
[complete inputs](/audit-output/evidence/differential-inputs.json), and
[results](/audit-output/evidence/stage2-fidelity.log).

## 3. Clean proof reconstruction

All candidate and trusted source artifacts needed for execution were copied to
`/tmp/audit-work/0-has-close-elements`. The semantics copy came from the
trusted `/reference` tree after the candidate tree had passed recursive
identity checking. No candidate compiled definition or K cache entered
scratch.

The live environment is K v7.1.293 and Python 3.10.12. I freshly built:

1. `audit-runtime-kompiled`, LLVM backend, main module `MPY-KRUN`;
2. `audit-verification-base-kompiled`, Haskell backend, main module
   `VERIFICATION-BASE`;
3. `audit-verification-inner-kompiled`, Haskell backend, main module
   `VERIFICATION-INNER`;
4. `audit-verification-kompiled`, Haskell backend, main module `VERIFICATION`.

Every build exited 0. This layering is material: the inner claim is proved in a
definition without the inner bridge; the outer state/control claims are proved
in a definition without the outer bridge; only the final entry claim sees both
already-justified bridges.

| Positive claim | Fresh definition | Exit | Exact output |
|---|---|---:|---|
| `SPEC-INNER.inner-loop` | `VERIFICATION-BASE` | 0 | `#Top` |
| `SPEC-OUTER-STATE.outer-loop-state` | `VERIFICATION-INNER` | 0 | `#Top` |
| `SPEC-OUTER.outer-loop` | `VERIFICATION-INNER` | 0 | `#Top` |
| `SPEC.target` | `VERIFICATION` | 0 | `#Top` |

The proof logs contain the exact commands, exit status, bounded output, and an
explicit exact-`#Top` check:
[reconstruction script](/audit-output/evidence/stage3_reconstruct.sh),
[inner claim](/audit-output/evidence/stage3-prove-inner.log),
[outer state](/audit-output/evidence/stage3-prove-outer-state.log),
[outer control](/audit-output/evidence/stage3-prove-outer-control.log), and
[target](/audit-output/evidence/stage3-prove-target.log). Build logs are indexed
in [evidence/README.md](/audit-output/evidence/README.md).

This stage passes. No timeout, resource failure, or other infrastructure
uncertainty affected reconstruction.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC-INNER.inner-loop` says: starting at the exact translated inner `for`
loop over `REM`, in the exact function frame, execution consumes the loop,
changes `result` from `RB` to
`RB or rowClose(F,T,I,J,REM)`, advances `j` by the length of `REM`, and leaves
`other` at the final element (or its prior value for empty `REM`). It preserves
`i`, `number`, bindings, environment, heap, allocation counters, caller frame,
return state, exception state, exit code, and the arbitrary following
continuation. Its precondition requires Float elements in `REM` and `ALL` and a
Float current outer value.

`SPEC-OUTER-STATE.outer-loop-state` says: starting at the exact translated
outer loop over `REM`, execution accumulates
`RB or closeRows(REM,ALL,T,I)`, advances `i`, and records the actual final
values of `number`, `j`, and `other`. It is deliberately general in `REM` and
the current locals; that generality is sound because the state equations
describe the loop it actually executes.

`SPEC-OUTER.outer-loop` appends the exact
`Return(Name("result")) ~> #endcall` continuation. It says the call returns the
same accumulated Boolean and restores environment 0, removes the callee scope,
restores `scopeLoc`, and pops the exact caller frame under fixed call/return
semantics.

`SPEC.target` says: for every finite `ValSeq VS` whose members are K Floats and
every K Float threshold `T`, calling the exact
`has_close_elements` closure returns `hasClose(VS,T)` from a clean module
state.

### Exact program and initial-state pinning

The entry claim does not use a free or arbitrary function body. Its closure
contains `HC-FUNCTION-BODY`; the three `HC-*` macros expand to the exact
function, outer-loop, and inner-loop constructor subtrees in the byte-identical
`solution.mpy`.

As an independent reachability check, fresh LLVM execution of the actual
submitted `solution.mpy` ended with `.K` and produced exactly the entry
claim's module state:

- environment 0;
- module scope 0 containing only
  `has_close_elements |-> closureVal(("numbers","threshold"), exact body, 0)`;
- parent scope `-1 |-> builtinsScope`;
- `scopeLoc = 1`, empty heap and stack, `noRet`, `NoExc`, and exit code 0.

Thus the claim's seeded closure is not a substituted algorithm or unreachable
fabricated state. It is the actual post-module state, and the `<k>` call
executes the exact submitted function body. The skipped top-level
`ImportFrom("typing","List")` has already executed as the supplied semantics'
non-`math` import no-op before this state.

Evidence: [module poststate](/audit-output/evidence/stage4-module-poststate.log)
and the construct/rule [map](/audit-output/evidence/used-construct-map.md).

### Satisfying witnesses and result constraint

The entry precondition is satisfiable. Three explicit witnesses were checked:

| `numbers`, `threshold` | Formal pair formula | Canonical | Candidate |
|---|---:|---:|---:|
| `[]`, `1.0` | false | false | false |
| `[1.0,2.8,3.0,4.0,5.0,2.0]`, `0.3` | true | true | true |
| `[0.0,1.0]`, `1.0` | false | false | false |

All values have the required Float sort/type. The first witnesses the empty
base cases; the second witnesses a satisfying close pair; the third witnesses
strict inequality at equality.

The postcondition is result-constraining. `hasClose` expands structurally to
`closeRows(VS,VS,T,0)`, which visits each outer index and uses `rowClose` to
include exactly indices `J` with `I < J`. Each included atom is
`closeVals(F,G,T)`. On every target use, the guarded simplification equates
that symbol to exactly the supplied-semantics term
`floatLt(absF(subF(F,G)),T)`. There is no unconstrained RHS variable,
tautological implication, omitted return cell, or existentially chosen result.

The exact reviewer harness function has AST identity with `solution.py`; nine
LLVM assertions end in `.K`, `NoExc`, exit code 0. Evidence:
[witness program](/audit-output/evidence/stage4_witness.py),
[Python results](/audit-output/evidence/stage4-python-witnesses.log),
[K harness](/audit-output/evidence/concrete_audit.py), and
[K results](/audit-output/evidence/stage4-krun-concrete-witnesses.log).

This stage passes.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-generated inventory covers all 26 K source files used by the
proof: the supplied `semantics.k` and helper tree, `verification.k`, and
`spec.k`. It enumerates 239 syntax declarations, 154 function declarations,
116 `total` declarations, zero `functional` declarations, 23
`symbol(...), no-evaluators` opaque declarations, 47 priority rules, 11
simplification rules, 725 total rules, five evaluation contexts, one
configuration, and four claims. Every entry is keyed by file, source line,
attributes, normalized text, and source SHA-256.

Evidence: [full inventory](/audit-output/evidence/rule-inventory.md),
[inventory generator](/audit-output/evidence/rule_inventory.py), and
[per-population decisions](/audit-output/evidence/rule-assessment.md).

The 695 supplied-semantics rules are the byte-identical fixed semantics
selected by this mode. The actual reachable constructor slice was checked in
detail: module loading and sequencing; import no-op; closure creation; scope
lookup; left-to-right call/argument evaluation; frame creation and parameter
binding; assignment; list iteration; `For` and `If`; Int and Float literals;
Int addition/comparison; Float subtraction, absolute value, and comparison;
Return; and frame cleanup. The other supplied rules have disjoint constructors,
operation strings, or callable guards and do not contribute to these claims.

### Candidate proof extensions

All 30 candidate rules are assessed individually or by exhaustive
constructor-family in `rule-assessment.md`. The material conclusions are:

- The three macros are exact syntax aliases, not operational shortcuts.
- `allFloatVS`, `rowClose`, `closeRows`, `hasClose`, `lastV`, `advance`,
  `outerJ`, and `outerOther` have exhaustive constructor cases. Recursive
  equations descend on a sequence tail. Every overlap either has disjoint
  guards or the same normalized value.
- The guarded `applyBin("-")` simplification is the supplied Float subtraction
  dispatch with the proven sort membership exposed; its overlap agrees.
- Boolean `orBool` associativity is an ordinary truth-table identity.
- `closeVals` is a conservative definitional extension, not an oracle for the
  task answer. Given any model of the supplied theory, it can be interpreted
  as `floatLt(absF(subF(X,Y)),T)` whenever `X` and `Y` are Floats and arbitrarily
  off-domain. That model extension satisfies the sole identifying equation.
  Every theorem-reachable occurrence is on-domain. No rule rewrites it to
  `true` or `false`, and it contains no pair-search conclusion.

### Operational bridges and priorities

The inner bridge matches the same arbitrary suffix as its supporting
`SPEC-INNER` claim and pins all nine cells, the exact module/function binding,
the exact callee frame, empty heap, locations, return/exception state, and exit
code. The supporting claim closes under `VERIFICATION-BASE`, where the bridge
does not exist. The bridge changes only `result`, `j`, and `other`.

The outer bridge is the exact initial-state instance of the general
`SPEC-OUTER-STATE` theorem. That theorem closes under `VERIFICATION-INNER`,
where the outer bridge does not exist. The bridge changes only `result`, `i`,
`number`, `j`, and `other`. It does not consume Return, `#endcall`, frame pop,
exceptions, cleanup, or an arbitrary following continuation.

Priority 40 merely lets each exact proved bridge preempt the generic
`#loop` unrolling rule. It does not broaden either match or serve as a
justification.

Fresh operational-context tests put an observable assignment immediately after
each loop. For the inner bridge, fixed and extended definitions both execute
the continuation and end with `i = 99`. For the outer bridge, both execute a
post-loop assignment and end with `result = true`. All four claims exit 0 with
exact `#Top`.

An independently authored body-sensitivity mutation changes the reachable
one-element inner increment from `j + 1` to `j + 2` while demanding the real
body's `j = 1` poststate. Its dry run exits 0, proving the artifact builds. The
actual proof exits 1 with `WarnStuckClaimState`; the residual has `"j" |-> 2`.
This is the expected execution mismatch, not a parser error, timeout, or
unrelated crash.

Evidence: [context spec](/audit-output/evidence/operational-context.k),
[fixed/extended logs](/audit-output/evidence/stage5-inner-context-base.log),
[outer extended log](/audit-output/evidence/stage5-outer-context-extended.log),
[body mutation](/audit-output/evidence/bridge-body-mutation.k), and
[mutation residual](/audit-output/evidence/stage5-body-mutation-proof.log).

No inventoried candidate rule is unsound, so there is no unsound-rule false
conclusion witness to report. This stage passes.

## 6. Fresh non-vacuity test

I did not reuse or modify the candidate's `spec-vacuity.k`. The fresh mutation
uses the satisfying intended-domain input `[0.0]` with threshold `1.0`. The
real program and formal `hasClose` result are false because there are no two
distinct positions. The destination is deliberately changed to true.

The mutation exercises the entry call and both loop layers. Its `--dry-run`
command exits 0, so parsing and claim construction succeed. The proof command
exits 1 with `WarnStuckClaimState`; the final complete configuration has:

```text
<k>
  false ~> .K
</k>
```

That residual directly exhibits the unmet result obligation. It is meaningful
non-vacuity evidence and shows the successful target theorem discriminates a
false returned Boolean.

Evidence: [fresh mutation](/audit-output/evidence/nonvacuity-mutation.k),
[runner](/audit-output/evidence/stage6_nonvacuity.sh),
[dry run](/audit-output/evidence/stage6-mutation-dry-run.log), and
[failed proof](/audit-output/evidence/stage6-mutation-proof.log).

This stage passes.

## 7. Proven versus assumed accounting

### Precisely proven

Under the freshly built supplied MPY theory plus the audited candidate
definitions and derived bridges, K proves:

> For every finite K `ValSeq VS` whose elements are Floats and every K Float
> `T`, if the exact translated `has_close_elements` call from the specified
> clean module state terminates, its returned K Bool is
> `hasClose(VS,T)`.

The recursive definition of `hasClose` is the disjunction over exactly the
index pairs `i < j` of the exact supplied Float operation
`floatLt(absF(subF(VS[i],VS[j])),T)`. The proof also establishes the stated
loop-local poststates and exact call-frame cleanup. This is partial
correctness; K reachability does not independently establish a resource bound
or total termination theorem.

### Trust and assumption ledger

| Boundary | Effect | Dependents | Assessment and evidence |
|---|---|---|---|
| Byte-identical supplied MPY semantics | Defines configuration, control, binding, lists, calls, returns, and Float operations | Every claim | Acceptable and required by SUPPLIED_SEMANTICS mode. Used slice statically reviewed; fresh LLVM execution and K assertions agree. |
| Trusted `py2mpy.py` translator | Connects `solution.py` to constructor program | Program identity | Acceptable mounted input. Regeneration is byte-identical; function AST and module poststate are checked. Semantic preservation is not itself a K theorem. |
| K v7.1.293 compiler, LLVM/Haskell backends, solver, and builtin theories | Executes and proves the K definitions | Every dynamic result | Foundational toolchain trust. Fresh builds, four positive claims, two distinct negative mutations, and four context claims discriminate errors. |
| Supplied opaque `subF`, `absF`, `floatLt` | Carries Float subtraction, absolute value, and strict comparison symbolically | Every close-pair atom | Acceptable low-level primitive boundary. The candidate preserves the exact terms and does not assume their truth. Supplied `[concrete]` equations execute K Float operations; LLVM and Python differentials provide finite support. |
| Proof-local opaque `closeVals` | Solver-facing name for the exact three-operation atom | `rowClose`, `closeRows`, target | Acceptable conservative definition on every target use, as established in stage 5. It is not an unconstrained returned value or task-answer axiom. |
| Structural interpretation of `rowClose`/`closeRows` as an index-pair disjunction | Bridges the recursive term to the English phrase “any two distinct elements” | Intent adequacy | Transparent finite-sequence induction, checked rule by rule. Canonical differential coverage supports the bridge but is not the universal proof. |
| Unboxed `list(ValSeq)` claim input | Models a read-only list argument without heap allocation | Entry and loop claims | Acceptable supplied-semantics input form. The function never mutates the list; the supplied semantics explicitly permits bare read-only list values. |

The imported but theorem-irrelevant supplied opaque symbols are:
`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `divF`, `addF`, `mulF`,
`powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, `sqrtF`, `sortVS`, and `sortKeyVS`. They are listed in
the exhaustive inventory but do not occur on a reachable target path. Together
with the three used Float symbols, these account for all 22 opaque declarations
in the supplied tree; `closeVals` is the twenty-third opaque declaration in
the complete proof inventory.

Finite evidence is correctly scoped:

- 12,903 canonical-versus-candidate Python comparisons support implementation
  fidelity only;
- nine fresh LLVM assertions support the used concrete MPY slice only;
- actual module execution supports reachability of the exact entry state;
- neither testing nor candidate prose substitutes for the four symbolic
  reachability proofs.

### Gate and decision summary

- Gate A, real-program soundness: **PASS**. Exact bodies execute under
  progressively bridge-free definitions; state/control footprints match;
  equations and priorities are sound; operational and result mutations
  discriminate.
- Gate B, intent adequacy: **PASS**. The formal Float-list domain matches the
  annotated contract, strict pair predicate, examples, and canonical behavior.
  No material behavior is omitted within that domain.
- Gate C, trust/evidence auditability: **PASS**. Every assumption, opaque
  symbol, command, input scope, oracle, and result is accounted for in
  reviewer-authored evidence.

The low-level K/translator/Float boundaries are explicit and acceptable for the
selected supplied-semantics problem. They do not create a material adequacy
gap, so the appropriate completed-audit decision is PASS rather than CONCERNS.

Evidence commands, bounded logs, sources, and hashes are indexed in
[evidence/README.md](/audit-output/evidence/README.md). Tool versions are in
[toolchain-versions.log](/audit-output/evidence/toolchain-versions.log).

VERDICT: PASS
LEGITIMACY: LEGIT
