# Independent adversarial review: 0-has-close-elements

The reconstructed K proof is legitimate: it executes a constructor AST that is
mechanically identical to the trusted retranslation of the submitted program,
constrains the returned Boolean to a nontrivial recursive predicate, closes from
clean source, and rejects a fresh reachable false result. I classify it as
`CONCERNS / LEGIT`, rather than `PASS`, because two intent bridges remain
conditional: the Haskell proof treats the three result-bearing float operations
as opaque supplied primitives, and the formal entry uses the supplied semantics'
legal unboxed read-only list representation rather than proving a separate
heap-reference-to-unboxed equivalence claim. Neither limitation is a
candidate-added oracle or an unsound rule.

All candidate prose, logs, traces, compiled definitions, and prior reports were
treated only as untrusted claims. All executable work used the isolated tree at
`/tmp/audit-work/reconstruction`; no candidate-built definition or cache was
copied. Reviewer-authored scripts, inputs, and bounded logs are in
`/audit-output/evidence/`.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount exists, so there is no rendered-mode
contradiction and no infrastructure breach.

The candidate's `run-input.json` identifies problem `0-has-close-elements` and
condition `kit-semantics`. `metrics.json`, `codex-last.txt`,
`codex-output.log`, `PROOF.md`, `prove.log`, and the structured trace claim a
successful validated proof; those claims were not used as proof evidence. The
structured JSONL trace was independently parsed in full: 485 records, one final
message, and 98 recorded tool-call items. See
[`stage1-trace-summary.log`](evidence/stage1-trace-summary.log) and its parser
[`inspect_trace.py`](evidence/inspect_trace.py).

The independent integrity command is recorded in
[`stage1-integrity.log`](evidence/stage1-integrity.log). Its results were:

- Every required candidate artifact checked there is a regular file. The
  candidate/reference source scans found no symlinked entries.
- `/candidate/prompt.py` and `/reference/prompt.py` are byte-identical, with
  SHA-256 `00b2e074e127a6a9d1376278bef732933760ab706057ec755a8c2642217b557a`.
- `/candidate/py2mpy.py` and `/reference/py2mpy.py` are byte-identical, with
  SHA-256 `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- `diff --recursive --brief --no-dereference` between the candidate and trusted
  `reference-semantics/` trees exited 0. The accompanying type listing covers
  every directory and file; there are no missing, additional, changed,
  mistyped, or symlinked candidate semantics entries.
- Both JSON metadata files parse. No required source/proof artifact is missing.

The candidate's `runtime-kompiled/`, `verification-kompiled/`, archived backend
diagnostic, bytecode, and claimed proof logs were deliberately excluded from
the scratch copy. Their presence in `/candidate` is not provenance evidence and
did not contaminate reconstruction. The exact source-only copy command and
resulting tree are in [`prepare-scratch.log`](evidence/prepare-scratch.log).

Stage 1 result: pass; no infrastructure error and no integrity failure.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a finite `List[float]` and a float threshold, return `True` exactly when
there are two distinct list positions `i != j` such that
`abs(numbers[i] - numbers[j]) < threshold`. The inequality is strict. Equal
values at different positions count as two elements; a list element is never
paired with its own position. Empty and singleton lists return `False`.

The trusted canonical implementation enumerates ordered pairs and returns at
the first witness. The candidate implementation enumerates the same ordered
pairs, sets a Boolean accumulator to `True` on a witness, and never resets it.
The absence of an early return changes work performed but not the result on the
annotated float domain. All branches are reachable across the intended domain:
empty/nonempty outer and inner loops, `i == j`/`i != j`, strict comparison
true/false/equal-boundary, and accumulator false/true.

### Translation identity

The trusted translator was run on the scratch copy of `solution.py`; `cmp`
against the submitted `solution.mpy` exited 0. Both MPY files have SHA-256
`b49190cd71b98cdec4d585f2562eb950cdbfc019a6b2bcb50be241d75cc98e37`.
The exact command, compile check, hashes, and statuses are in
[`stage2-fidelity.log`](evidence/stage2-fidelity.log).

### Independent Python differential

[`stage2_differential.py`](evidence/stage2_differential.py) loads the trusted
entry point from `/reference/canonical.py` and the generated entry point from
the scratch `solution.py` by independent file imports. Its complete deterministic
input set is preserved in
[`stage2-differential-inputs.json`](evidence/stage2-differential-inputs.json).
The scope is:

- both documented examples;
- empty and singleton inputs;
- equal values, zero and negative thresholds, signed zero, subnormal neighbors,
  and strict-equality/just-above boundaries;
- true witnesses occurring early and late;
- NaN and infinity elements/thresholds;
- exhaustive lists of length 0 through 4 over a four-value grid at five
  thresholds; and
- 750 seeded representative lists of length 0 through 10.

The exact command in [`stage2-differential.log`](evidence/stage2-differential.log)
exited 0: 2,473 cases, 1,384 true and 1,089 false, zero mismatches, and zero
non-Boolean results. This is finite fidelity evidence, not a universal proof.

Stage 2 result: pass; the candidate implements the trusted canonical behavior
on all audited cases, and the submitted MPY is the trusted translation.

## 3. Clean proof reconstruction

The scratch tree contains the trusted semantics, prompt, canonical, and
translator plus only the candidate's `solution.py`, submitted MPY copy,
`verification.k`, and `spec.k`. Candidate-built definitions and caches were not
reused.

Fresh builds from source:

| Purpose | Exact command | Result |
|---|---|---|
| Concrete definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled` | exit 0; [`stage3-kompile-llvm.log`](evidence/stage3-kompile-llvm.log) |
| Proof definition | `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled` | exit 0; [`stage3-kompile-haskell.log`](evidence/stage3-kompile-haskell.log) |

Every positive target claim was then run with the dependencies needed to make
the circularities available:

| Target reached by the command | Exact claim selection | Result |
|---|---|---|
| Inner loop | `kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.inner-loop` | `#Top`, exit 0; [`stage3-kprove-inner.log`](evidence/stage3-kprove-inner.log) |
| Outer loop | `kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.inner-loop,SPEC.outer-loop` | `#Top`, exit 0; [`stage3-kprove-outer.log`](evidence/stage3-kprove-outer.log) |
| Entry theorem | `kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.inner-loop,SPEC.outer-loop,SPEC.has-close-elements` | `#Top`, exit 0; [`stage3-kprove-entry.log`](evidence/stage3-kprove-entry.log) |

The warnings in these logs are unused-variable warnings from the fixed
semantics/spec; none is a stuck claim or nonzero build/proof status.

An additional reviewer ground-Haskell experiment is preserved in
[`stage4-kprove-ground.log`](evidence/stage4-kprove-ground.log). It is not a
target proof and is not counted as positive or negative evidence: it exits on
the backend's documented missing evaluator for the concrete `FLOAT.sub` hook,
before it can discharge the ground obligation. Clean LLVM execution and all
symbolic target proofs remain available, so this optional diagnostic is not an
audit infrastructure breach. It directly exposes the float trust boundary
accounted for in stage 7.

Stage 3 result: pass; every positive proof target reconstructs to `#Top`/0 from
source.

## 4. Adequacy and real-program pinning

### Plain-language claim restatement

`SPEC.inner-loop` starts at an actual supplied-semantics `#loop` over a remaining
sequence `YS`. Its precondition says that `x` and every member of `YS` are
floats, `threshold` is a float by sort, `result` is Boolean, indices `i` and `j`
are integers, and the module frame does not shadow builtin `abs`. It removes the
loop, changes `result` from `R` to `R or closeInner(X,T,I,J,YS)`, increments `j`
once per remaining element, existentially retains the final `y`, and frames the
rest of the configuration.

`SPEC.outer-loop` starts at the actual outer `#loop` over `XS`, with both `XS`
and the full `numbers` sequence `ALL` all-float and builtin `abs` unshadowed. It
removes the loop, changes `result` from `R` to
`R or closeOuter(T,I,XS,ALL)`, increments `i` once per outer element, and
existentially hides final locals that do not affect the return. The summary is
valid even for the claim's deliberately general `I`, `XS`, and `ALL`: the real
body scans `ALL` for each element of `XS` and compares the current integer
indices.

`SPEC.has-close-elements` begins in the exact initial configuration, loads the
module, binds the named function, evaluates the two arguments, creates the real
call frame, runs the full function body and both loop claims, returns, pops the
frame, and leaves a Boolean in `<k>`. Its precondition is precisely
`allFloatVS(VS)` with `T:Float`. Its postcondition is the equivalence
`?R ==Bool hasClose(VS,T)`, not an implication or a free result. The same `?R`
occurs in the final `<k>` cell and the ensure condition. The module map is
existential only because the newly installed closure is not an observable
HumanEval result; heap, allocator, stack, return, exception, and exit cells are
explicitly constrained.

### Exact program identity

The entry claim embeds the function body through the three macro names in
`verification.k`. To avoid relying on visual similarity, the reviewer parsed
the trustedly regenerated `solution.mpy` and the entry claim's embedded module
under the freshly compiled `VERIFICATION` syntax with `kast --expand-macros`
and JSON output. `cmp` exited 0; both expanded ASTs have SHA-256
`55b292a94203e577d681afa28753320c954e177f074329bc8caf95d783b11c02`.
See [`stage4_ast_pin.sh`](evidence/stage4_ast_pin.sh), the independently written
embedded term [`stage4-embedded-module.mpy`](evidence/stage4-embedded-module.mpy),
and [`stage4-ast-pin.log`](evidence/stage4-ast-pin.log). Thus the theorem does
not execute a substituted program.

### Satisfying state and concrete substitutions

A concrete entry state satisfying every entry precondition is the exact initial
configuration in `spec.k` with
`VS = vCons(1.0, vCons(1.125, .ValSeq))` and `T = 0.25`. Every list member is a
K `Float`; the initial environment/scope/heap/stack/return/exception/exit cells
are explicitly present. Unfolding `hasClose` selects the two unequal indices
and yields `abs(1.0 - 1.125) < 0.25`, hence `true`.

[`stage4_witness.py`](evidence/stage4_witness.py) independently unfolds the
recursive result and compares it with both Python implementations. Its logged
results are:

- `[1.0, 1.125], 0.25`: claimed `true`, canonical `true`, generated `true`;
- `[1.0, 1.5], 0.5`: claimed `false`, canonical `false`, generated `false`;
- `[], 0.5`: claimed `false`, canonical `false`, generated `false`.

The exact result is in [`stage4-witness.log`](evidence/stage4-witness.log).
Separately, the exact generated body plus six normal/boundary assertions was
translated and executed on the freshly built LLVM semantics. `krun` ended in
`.K`, `NoExc`, and exit cell 0; see
[`stage4-concrete.log`](evidence/stage4-concrete.log) and its generators
[`stage4_concrete.sh`](evidence/stage4_concrete.sh) and
[`stage4_generate_concrete.py`](evidence/stage4_generate_concrete.py).

Stage 4 result: pass; the theorem is satisfiable, result-constraining, and
mechanically pinned to the real submitted program.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`stage5-rule-inventory.md`](evidence/stage5-rule-inventory.md) is a
source-derived exhaustive inventory of every top-level `configuration`,
`syntax`, `rule`, `context`, and `claim` in all 24 supplied K files plus
`verification.k` and `spec.k`. It records source line, normalized complete item,
attributes, and a per-item reached/unreached/local assessment. The inventory
contains 957 items: one configuration, 235 syntax declarations, 713 rules, five
contexts, and three claims. Attribute counts include 152 functions, 114 total
declarations, 25 symbols, 22 `no-evaluators` opaque declarations, 45 priority
rules, 35 concrete rules, 26 `owise` rules, five macro declarations, and two
strict/seqstrict declaration groups. There are no local or supplied
`simplification` or `functional` declarations. The generation command and
counts are in [`stage5-inventory.log`](evidence/stage5-inventory.log).

Every supplied item marked `SUPPLIED-REACHED` was checked against the path below.
Every item marked `SUPPLIED-UNREACHED` has a constructor/operator/call shape that
cannot occur in the closed submitted AST and cannot overlap a reachable redex
under the relevant sorts and guards. Such rules remain part of the selected
fixed semantics, but no general claim that its unused language subset is a full
CPython model is needed for this theorem. The static scan finds no task-answer
syntax/rule/claim in the supplied baseline, no simplification/functional rule,
and no candidate priority rule; see
[`stage5-static-scan.log`](evidence/stage5-static-scan.log).

### Mapping every used construct

| Submitted construct | Declaration and operational path |
|---|---|
| `Module`, `Stmts` | `MPY-SYNTAX`; `#loadAll`, head/tail statement sequencing, and `.Stmts` termination in `core.k` |
| `ImportFrom("typing","List")` | `Stmt` syntax; the non-math `ImportFrom` `owise` no-op in `controls.k` |
| `FuncDef`, `Params` | syntax plus unannotated closure binding in `functions.k` |
| `Call(Name(...), args)` | `Name/#look` LEGB lookup in `core.k`; explicit callee-then-left-to-right-arguments route in `call.k`; closure frame creation and parameter binding in `call.k`/`functions.k` |
| `Assign` and literals | `Assign` strict RHS and current-frame write in `controls.k`; `Int`/`Bool` literal rules in `core.k`; `Float` literal rule in `float.k` |
| `For` over `numbers` | strict iterable evaluation, `For -> #loop`, loop-step rules in `controls.k`; `list` iterator rules in `list.k`; `Name` target binding in `tuple.k` |
| `If` | strict condition, `truthy(Bool)`, and `#branch` true/false rules in `core.k`/`controls.k` |
| integer `i != j` | comparison contexts/dispatch in `operators.k`; integer `!=` in `int.k` |
| `x - y` | `BinOp` `seqstrict(2,3)` and dispatch in `operators.k`; guarded abstract-Val bridge in `verification.k`; supplied `subF` |
| `abs(...)` | builtin lookup in `builtinsScope`, call argument evaluation, builtin dispatch, guarded bridge in `verification.k`; supplied `absF` |
| strict `< threshold` | left-then-right comparison contexts, guarded bridge in `verification.k`; supplied `floatLt` |
| `j += 1`, `i += 1` | strict RHS plus current binding update in `controls.k`; integer addition in `int.k` |
| `Return(result)` | strict result evaluation, `retV`, frame pop, environment/stack/scope restoration in `functions.k` |

Evaluation order is consequently faithful: each assignment/augmentation
evaluates its RHS first, `BinOp` evaluates left then right, comparisons evaluate
left then wrapped right, `Call` evaluates the callee before arguments and
arguments left-to-right, and loop iterables are evaluated once. The only state
changes are the module closure binding and transient local call frame/stack/ret
state. The formal bare input list is read but never allocated or mutated; the
heap and exception/exit state are preserved.

### Every candidate-local declaration and rule

| Local extension | Classification and decision |
|---|---|
| `HC-INNER-BODY`, `HC-OUTER-BODY`, `HC-FUNCTION-BODY` syntax and three macro rules | Compile-time definitional abbreviations. Expanded-AST byte comparison establishes exact identity; they replace no runtime step. Sound. |
| `allFloatVS` declaration plus empty/cons equations | Definitional predicate. Constructor cases are disjoint and exhaustive and recursion descends on `ValSeq`. Sound. |
| `advanceIndex` declaration plus empty/cons equations | Definitional counter summary. Cases are disjoint/exhaustive and structurally descending. Sound for every integer start. |
| `asFloat` declaration plus float/non-float equations | Definitional projection. The Float case and guarded `notBool isFloat(V)` case are disjoint and cover `Val`; the arbitrary `0.0` non-float default is never selected under any claim's float preconditions. Sound on the complete guard and harmless outside the theorem. |
| Guarded `applyBin("-",X,Y)` | Derived dispatch lemma, not a `BinOp` or call interception. With both guards, `asFloat(X/Y)` are identities, so the RHS is exactly the supplied Float/Float rule `subF(X,Y)`. Its overlap agrees; mixed/int guards are false. Sound. |
| Guarded `applyBuiltin("abs",X,.Vals)` | Derived dispatch lemma after genuine name lookup, callee routing, and argument evaluation. On the Float overlap its RHS is exactly supplied `absF(X)`. Sound. |
| Guarded `applyCmp("<",X,Y)` | Derived dispatch lemma after genuine operand evaluation. On the Float overlap its RHS is exactly supplied `floatLt(X,Y)`. Sound. |
| `closeV` declaration/equation | Definitional summary of the exact supplied `floatLt(absF(subF(...)),...)` term. It does not rewrite program control; all theorem uses have float arguments. Sound. |
| `closeInner` declaration plus empty/cons equations | Definitional existential fold over remaining inner elements. Cases are disjoint/exhaustive, recursion descends, index increments match the body, and `i != j` matches control. Sound. |
| `closeOuter` declaration plus empty/cons equations | Definitional existential fold over outer elements against full `ALL`. Cases are disjoint/exhaustive, recursion descends, and the outer index increments exactly once. Sound. |
| `hasClose` declaration/equation | Starts `closeOuter` at index 0 with the same full list in both positions. Sound. |

There is no candidate rule matching `Call`, `#applyK`, `#loop`, `FuncDef`,
`Return`, configuration cells, or the final result. There is no local opaque
symbol, priority rule, simplification, axiom-like claim, or unconstrained
oracle. Pairwise overlap inspection of the only three extensions to supplied
functions is recorded by the exact source matches in the static-scan log.

The three reachability claims themselves preserve the full real control path.
The inner and outer claims are ordinary circularities over the supplied
`#loop`; neither skips a function body or invents state. The entry claim loads
and calls the exact module and uses those circularities only when execution
reaches the corresponding loop heads.

No materially unsound rule was found, so this review makes no unsoundness claim
requiring a false-conclusion witness. Unused supplied operations are explicitly
classified as unreachable rather than being mislabeled unsound without a
relevant witness.

Stage 5 result: pass; the proof theory has no execution bypass or false
candidate-local equation on the theorem domain.

## 6. Fresh non-vacuity test

The candidate's `mutation-spec.k` was read only as an untrusted prior claim. The
reviewer independently wrote [`stage6-false-empty.k`](evidence/stage6-false-empty.k).
It uses the exact submitted module and exact initial configuration with
`list(.ValSeq)` and threshold `0.5`. This is a concrete satisfiable entry state:
`allFloatVS(.ValSeq)` is true, the outer loop is empty, and the real function
returns `false`. The mutation changes only the result-constraining obligation to
`ensures ?R ==Bool true`.

The dry-run command

`kprove stage6-false-empty.k --definition verification-kompiled --spec-module AUDIT-VACUITY --claims SPEC.inner-loop,SPEC.outer-loop,AUDIT-VACUITY.false-empty-result --dry-run`

exited 0 and produced the backend invocation, establishing that the mutation
imports and builds; see [`stage6-dry-run.log`](evidence/stage6-dry-run.log).
The same command without `--dry-run` exited 1 with
`WarnStuckClaimState`. Its residual final `<k>` value is `false ~> .K`, and the
diagnostic says destination unification succeeded but the implication check
failed. This is exactly the unmet `false == true` obligation, not a parser
error, timeout, unrelated crash, or unreachable mutation. See
[`stage6-kprove-false-empty.log`](evidence/stage6-kprove-false-empty.log).

Stage 6 result: pass; the proof discriminates a fresh false result.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Relative to the supplied `MPY` proof semantics and the candidate-local sound
definitions audited above, for every finite K `ValSeq` satisfying
`allFloatVS(VS)` and every K `Float` threshold `T`, if the exact submitted module
load and call terminate from the stated initial configuration, the returned K
Boolean equals:

`closeOuter(T, 0, VS, VS)`

which structurally unfolds to the disjunction over all ordered distinct index
pairs of:

`floatLt(absF(subF(VS[i], VS[j])), T)`.

The loop-control, index-exclusion, accumulator monotonicity, binding, frame,
return, and state-preservation facts are proved by K reachability. The theorem
is partial correctness; it does not separately prove termination, although the
submitted loops iterate structurally finite sequences.

The ordinary mathematical bridge from the recursive equations to “there exist
two distinct positions closer than the threshold” is an inspected structural
induction: `closeInner` is exactly the remaining inner disjunction,
`closeOuter` is exactly the remaining outer disjunction, and `hasClose` starts
both at the full list and index 0. Ordered-pair enumeration is equivalent to the
prompt's unordered existential question. This interpretation does not replace
the K proof.

### Trust ledger

| Boundary | Effect on theorem | Status/evidence |
|---|---|---|
| Supplied `MPY` operational semantics | Defines syntax, evaluation, state, calls, loops, and return | Fixed by the rendered mode and byte-identical to the trusted mount. Used rules were statically audited; clean LLVM execution supports the intended path. Acceptable fixed-semantics boundary. |
| `subF`, `absF`, `floatLt` | These three opaque Haskell symbols determine every proximity test and therefore the returned Boolean | Their candidate bridges are exact overlaps with supplied rules. Supplied `[concrete]` rules call the LLVM float hooks. The K proof is conditional on their intended meaning; finite concrete evidence supports but cannot universally prove the CPython bridge. Concerning but legitimate. |
| Other imported `symbol(...)` declarations | None occurs on a reachable submitted-program/proof-summary path | Exhaustively inventoried: `intFloatDiv`, `divII`, `floatMod`, `floorFI`, `toF`, `ceilF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, `sortVS`, `sortKeyVS`, and `md5hexCodes`. They have no dependent target claim here. |
| K builtins and tooling | Integer/Boolean/map/list reasoning, compilation, reachability engine, SMT reasoning, and LLVM execution | Standard trusted proof/execution infrastructure. Exact fresh commands and status signals are preserved. Acceptable low-level trust boundary. |
| Trusted `py2mpy.py` | Connects Python source to the constructor program | Trusted mounted input; byte-identical candidate copy; fresh output byte-identical to submission; macro-expanded proof AST identical. Strong reproducible identity evidence. |
| Bare `list(VS)` formal argument | The formal call passes the semantics' explicitly legal unboxed read-only list, while ordinary translated list literals allocate heap references | The function only reads/iterates `numbers`; supplied `For(ref(...))` dereferences to the same list structure. Concrete heap-backed executions agree, but no separate universal reachability lemma proves this representation bridge. Concerning but not an execution bypass. |
| Trusted canonical and prompt interpretation | Connects formal `hasClose` and implementation behavior to HumanEval intent | Structural inspection plus 2,473 canonical/generated Python comparisons. Finite evidence supports, not proves, universal equivalence. |

To strengthen the reachable primitive and representation bridges independently,
[`stage7_k_differential.py`](evidence/stage7_k_differential.py) used the trusted
canonical result as oracle, appended 212 finite normal/boundary assertions to
the exact generated source, translated them with the trusted translator, and
executed them on the freshly built LLVM definition. The preserved cases are in
[`stage7-k-differential-inputs.json`](evidence/stage7-k-differential-inputs.json).
[`stage7-k-differential.log`](evidence/stage7-k-differential.log) records
translation exit 0, `krun` exit 0, `.K`, `NoExc`, exit cell 0, and zero Python
mismatches. These include heap-backed list literals. This is finite empirical
support only.

The larger Python differential includes NaN and infinities, but the clean K
differential is finite-valued. In addition, the Haskell backend diagnostic
shows that it cannot ground-evaluate `FLOAT.sub`. Consequently, universal
agreement of the supplied opaque float primitives with all CPython binary64
special cases remains assumed. This limitation does not allow a false theorem
under the selected K semantics, but it prevents an unconditional `PASS` at the
natural-language bridge.

### Final decision

Real-program soundness passes: exact body execution, complete relevant state
footprint, faithful binding/evaluation/control, valid equations and overlaps, a
satisfiable entry state, and meaningful non-vacuity. Intent adequacy passes for
the annotated `List[float]`/float domain and strict distinct-position property.
Evidence is reproducible and the trust boundary is explicit. The opaque-float
and unboxed-list bridges are limitations of what is universally established,
not materially unsound proof rules or substituted execution. The correct
classification is therefore legitimate with concerns.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
