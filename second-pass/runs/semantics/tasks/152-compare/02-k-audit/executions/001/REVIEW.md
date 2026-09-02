# Independent adversarial audit — 152-compare

The candidate is **not a legitimate proof**. Fresh reconstruction does produce
`#Top`, the formal postcondition constrains the returned list, and the submitted
program is pinned exactly. However, the universal proof closes under a
proof-local operational bridge that is false over its declared match domain.
For a nonempty integer input the bridge skips the real tuple-target bindings
and preserves stale `score` and `prediction` values. The extended definition
therefore proves a concrete false state transition that the bridge-free supplied
semantics rejects. This is a material Gate A soundness failure, independently of
the fact that the stale local bindings are later popped in this particular
`compare` function.

Audit work was isolated in `/tmp/audit-work/compare152`. Candidate caches and
compiled definitions were neither copied nor used. Commands, statuses, bounded
outputs, reviewer-authored tests, and the exhaustive K inventory are under
[`/audit-output/evidence/`](/audit-output/evidence/).

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. The mount therefore does not
contradict the rendered mode; this is not an infrastructure breach.

The recursive candidate/reference comparison returned exit 0 with no
differences. The type-and-mode inventory shows the same directories and regular
files, all candidate semantics entries are non-symlinks, and there are no
missing or additional entries inside `candidate/reference-semantics/`.
Evidence:

- [mount and file-type inventory](/audit-output/evidence/01_mount_inventory.log)
- [recursive semantics diff](/audit-output/evidence/01_semantics_diff.log)
- [representative integrity hashes](/audit-output/evidence/01_integrity_hashes.log)

`candidate/prompt.py` and `candidate/py2mpy.py` are byte-identical to the
trusted mounted files. Both `cmp` commands exited 0:

- [prompt comparison](/audit-output/evidence/01_prompt_cmp.log)
- [translator comparison](/audit-output/evidence/01_translator_cmp.log)

### Missing generation records

The following requested provenance artifacts are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`
- any structured trace matching `*trace*` or `*.jsonl`

The exact check is in
[01_required_artifacts.log](/audit-output/evidence/01_required_artifacts.log).
These are provenance-integrity failures and limit reconstruction of how the
candidate was generated. They do not prevent an independent source rebuild,
and no candidate prose, trace, prior `#Top`, or compiled cache was used as proof
evidence. No `PROOF.md` was submitted. The root-level `__pycache__` was ignored
and not copied.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt asks for an output array with one absolute score/guess
difference at every corresponding position; the documented input arrays have
equal length. The trusted canonical implementation is:

```python
return [abs(x-y) for x,y in zip(game,guess)]
```

Thus, on the stated equal-length domain the result has the same length and
element `i` is `abs(game[i] - guess[i])`. Both Python implementations also
truncate to the shorter input through `zip`, although unequal lengths are
outside the stated contract.

The candidate `solution.py` initializes a fresh result list, traverses
`zip(game, guess)`, appends `abs(score - prediction)`, and returns the list.
It is a different surface formulation of the same algorithm. The formal proof
domain is narrower than the untyped prose: it quantifies over finite K
`IntSeq`s, i.e. integer lists. The prompt does not explicitly state a numeric
type, although its examples and intended HumanEval usage are integer-valued.

### Trusted translation

The trusted translator regenerated the scratch copy of `solution.mpy`.
Generation exited 0, `cmp` exited 0, and both files have SHA-256
`4b4ee08ff7597115a3cc37699d5bdf9e27497cdaee3314a7d8c4f07f5ced704a`:

- [translator command](/audit-output/evidence/02_translate_regenerate.log)
- [byte-identity check](/audit-output/evidence/02_translation_identity.log)
- [hashes](/audit-output/evidence/02_translation_hashes.log)

### Independent differential test

[`differential_compare.py`](/audit-output/evidence/differential_compare.py)
loads `/reference/canonical.py` and the scratch copy of the generated
`solution.py` through independent module loaders. It covers:

- both prompt examples;
- empty input;
- zero, positive, and negative subtraction/absolute-value boundaries;
- negative equality and mixed signs;
- arbitrary-size Python integers up to magnitude `10**100`;
- all pairs of equal-length vectors of lengths 0, 1, and 2 over
  `{-3,-1,0,1,3}` (651 cases);
- 2,000 deterministic generated equal-length cases of lengths 0 through 20;
- both unequal-length truncation directions claimed by the stronger K theorem.

The run exercised 2,664 cases and found zero mismatches. The seed, exact
generator, named inputs/results, generated-input digest, command, and exit 0
are preserved in
[02_python_differential.log](/audit-output/evidence/02_python_differential.log).
This is finite bridge evidence, not a universal proof.

## 3. Clean proof reconstruction

### Fresh definitions

K version 7.1.337 was available independently at `/usr/bin`. All definitions
were built from the scratch source copy. No candidate-compiled directory or
cache existed in that copy.

The concrete LLVM definition compiled from the supplied source with exit 0:
[03_kompile_runtime.log](/audit-output/evidence/03_kompile_runtime.log).
The compiler reported non-exhaustiveness warnings in unused operations such as
float conversions, `mapStrVS`, `joinCodes`, and `valSeqAt`; none is reachable
from `compare`.

Reviewer-authored concrete cases were translated by the trusted translator and
executed through the fresh LLVM definition. The final configuration had
`.K`, `NoExc`, an empty stack, and exit code 0. It covered the examples, empty
input, sign and equality boundaries, mixed signs, and both unequal-length
directions:

- [reviewer Python source](/audit-output/evidence/k_concrete_cases.py)
- [translated MPY source](/audit-output/evidence/k_concrete_cases.mpy)
- [translation command](/audit-output/evidence/03_translate_k_concrete.log)
- [concrete execution](/audit-output/evidence/03_krun_reviewer_cases.log)

The candidate's four concrete assertions were also independently executed with
exit 0:
[03_krun_candidate_cases.log](/audit-output/evidence/03_krun_candidate_cases.log).

### Positive proof claims

The Haskell proof definition compiled from `verification.k` with exit 0:
[03_kompile_verification.log](/audit-output/evidence/03_kompile_verification.log).
The complete three-claim target module returned exit 0 and printed `#Top`:
[03_kprove_target.log](/audit-output/evidence/03_kprove_target.log).

For unambiguous per-claim evidence, exact copies of the three claims were placed
in separate reviewer modules in
[`target-claims-separated.k`](/audit-output/evidence/target-claims-separated.k).
Each was run independently:

| Claim | Exit | Result | Evidence |
|---|---:|---|---|
| Universal integer-sequence claim | 0 | `#Top` | [log](/audit-output/evidence/03_kprove_target_universal.log) |
| Prompt example 1 | 0 | `#Top` | [log](/audit-output/evidence/03_kprove_target_example_one.log) |
| Prompt example 2 | 0 | `#Top` | [log](/audit-output/evidence/03_kprove_target_example_two.log) |

A separate Haskell definition whose main module is `COMPARE-COMMON` excludes
the proof-local loop bridge. It compiled with exit 0, and all four finite
operational claims returned `#Top` with exit 0:

- [bridge-free build](/audit-output/evidence/03_kompile_operational.log)
- [bridge-free finite proofs](/audit-output/evidence/03_kprove_operational.log)

These fresh `#Top` results establish closure under the respective definitions.
They do not validate the proof-local rule, which fails Stage 5.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

None of the three entry claims has an explicit `requires` clause.

1. **Universal claim.** `GAME` and `GUESS` range over arbitrary finite
   `IntSeq`s. From a fresh module environment, empty heap, allocation counters
   1/0, empty call stack, `noRet`, and `NoExc`, load the candidate definition
   and call `compare` on unboxed integer lists. The postcondition requires:
   `ref(0)` in `<k>`, exactly one heap object at location 0 containing
   `absDiffs(intVals(GAME), intVals(GUESS))`, heap counter 1, the installed
   global closure, restored environment/scope counter, empty stack, `noRet`,
   and `NoExc`. It proves the prompt's equal-length case and a stronger
   zip-truncating unequal-length case.
2. **Example claim 1.** The same initial and final cell conditions are ground
   for the first prompt example and require exactly `[0,0,0,0,3,3]`.
3. **Example claim 2.** The same conditions are ground for the second prompt
   example and require exactly `[4,4,1,0,0,6]`.

The returned reference and exact heap content are constrained; the claims are
not tautologies, free-result claims, or one-way implications.

### Exact program identity

`compareDef`, `compareBody`, and `appendBody` are macros, not substitute
executable rules. After macro expansion, parsing `Module(compareDef)` produced
byte-identical KORE to parsing the trusted-translator-verified submitted
`solution.mpy`; both KORE files have SHA-256
`222eb11395b3e956e1514d055e66518f686209f66993eb24340ccc6b7434a58c`:

- [submitted-program parse](/audit-output/evidence/04_kast_solution_ast.log)
- [macro-program parse](/audit-output/evidence/04_kast_macro_ast.log)
- [identity comparison](/audit-output/evidence/04_macro_program_identity.log)
- [hashes](/audit-output/evidence/04_macro_program_hashes.log)
- [reviewer macro program](/audit-output/evidence/macro-program.mpy)

The real definition therefore executes before the bridge redex is reached:
the function is installed, arguments are looked up/evaluated, a call frame is
created, `result` is allocated, `zip` is resolved and evaluated, and `For`
becomes the exact `#loop` redex. The proof-local rule then replaces the real
loop execution.

### Satisfying witnesses

The common precondition is realizable exactly as written. For the universal
claim, for example, choose `GAME = [1,-2]` and `GUESS = [4,-2]` in the specified
fresh configuration; the claimed K result is `[3,0]`. The two ground claims'
own initial configurations are witnesses for their preconditions. The K
substitutions, canonical results, and generated-Python results all agree:
[04_claim_witnesses.log](/audit-output/evidence/04_claim_witnesses.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`K-RULE-INVENTORY.md`](/audit-output/evidence/K-RULE-INVENTORY.md) inventories
every local `configuration`, `syntax`, `context`, `rule`, and `claim` in all 24
supplied K source files, `semantics.k`, `verification.k`, `spec.k`, and
`operational-spec.k`. Each item includes its exact source text, source lines,
attributes, classification, and source-file hash. The inventory contains:

- 1 configuration and 5 evaluation contexts;
- 232 syntax declarations, including every `function`, `total`, macro, strict,
  symbol, and no-evaluator declaration;
- 704 rules: 617 ordinary, 32 `[concrete]`, 26 `[owise]`, and 29 priority rules;
- 7 positive claims.

There are no local `[simplification]` rules and no `[functional]`
declarations. The source-level attribute search is preserved in
[05_special_attributes.log](/audit-output/evidence/05_special_attributes.log).

The following disposition covers every item in that inventory:

| Files/items | Dependency and determination |
|---|---|
| `semantics.k`, `syntax.k` | Import shell plus AST syntax. The submitted constructors all have matching declarations. No local semantic rule exists in `semantics.k`. |
| `core.k`, `call.k`, `functions.k` | Reachable configuration, sequencing, lookup, argument evaluation, allocation, call-frame, return, and pop rules. Their evaluation order and affected cells match the real submitted control flow. |
| `controls.k`, `iter.k`, `builtins.k` | Reachable assignment/expression/for protocol and `zip`/`abs` rules. The fixed loop performs `#iterNext`, tuple binding, body execution, and iteration in order. `zip` stops at the shorter list; `abs` uses mathematical `absInt`. Other builtin rules are unreachable from this program. |
| `operators.k`, `int.k` | Reachable binary dispatch and integer subtraction; the used equations are ordinary unbounded-integer mathematics. Other operators are unreachable. |
| `list.k`, `tuple.k` | Reachable list allocation, append mutation, tuple construction, and tuple-target binding. Crucially, `#bindTgt` writes both loop variables on every nonempty iteration. Other collection operations are unreachable. |
| `str.k` | Only the ASCII docstring literal is reachable; it is evaluated and then discarded by `Expr(_:Val)`. Other string rules are unreachable. |
| `methods.k` | Supplies the common method value domain imported by call routing; its concrete string/list method equations do not match the reachable append redex, which is handled by `list.k`. |
| `assert.k`, `bool.k`, `comprehension.k`, `dict.k`, `float.k`, `range.k`, `set.k`, `sort.k`, `subscript.k` | No constructor or redex from these domain-specific rules is reachable in the target claims. They are fixed supplied-semantics items, not candidate proof extensions, and have no target value/control/state dependency. |
| `concrete.k` | Imported only by `MPY-KRUN`, not by the Haskell target proof. It affects concrete test evidence but not target claim closure. |
| `verification.k` items | Audited individually below. |
| `spec.k`, `operational-spec.k` claims | Audited for domain, result constraint, cell framing, and realizable preconditions in Stages 3–4. |

The fixed supplied tree contains 25 declared symbols: `sortVS`, `sortKeyVS`,
`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
and `sqrtF`. None occurs in the submitted program, its entry claims,
`intVals`, `absDiffs`, or the loop bridge. They therefore cannot affect target
control, state, or result. They remain part of the broad supplied language
trust boundary, not evidence for this theorem.

### Mapping of every used syntactic construct

| Submitted construct | Declaration | Execution rules |
|---|---|---|
| `Module`, statement sequence | `syntax.k`; `core.k` | `#loadAll`, statement sequencing, `.Stmts` |
| `FuncDef`, `Params`, `Return` | `syntax.k` | `functions.k` definition, call frame, binding, return/pop |
| `Expr(Str(...))` | `syntax.k` | `str.k` literal conversion; `controls.k` expression discard |
| `Assign(Name("result"), ListExpr())` | `syntax.k` | `list.k` allocation; `controls.k` current-scope assignment |
| `For` | `syntax.k` | `controls.k` `For => #loop`, iterator step/done/yield rules |
| `TupleExpr` loop target | `syntax.k` | `tuple.k` tuple construction, `#unpackSeq`, `#bindTgt` |
| `Call(Name("zip"), ...)` | `syntax.k` | `core.k` lookup/arg order; `call.k` dispatch; `builtins.k` zip and iterator |
| `Attribute(...,"append")` and call | `syntax.k` | `call.k` bound method routing; priority append rule in `list.k` |
| `Call(Name("abs"), BinOp("-",...))` | `syntax.k` | `operators.k` dispatch; `int.k` subtraction; `builtins.k` abs |
| `Name` reads | `syntax.k` | scope-chain lookup in `core.k` |

No used construct is silently fabricated or unmodeled in the supplied
semantics.

### Candidate-local extension inventory

1. **`intVals`** — a total definitional summary from algebraic `IntSeq` to
   integer-valued `ValSeq`. Its two equations are disjoint, exhaustive on
   `IntSeq`, structurally decreasing, and mathematically true.
2. **`absDiffs`** — a result-bearing definitional summary. Its three equations
   are pairwise disjoint: left empty, left nonempty/right empty, or both
   nonempty integer heads. The recursive case decreases both lists and uses
   `absInt(A -Int B)`. It is partial outside integer-headed lists, but all entry
   uses are under `intVals`, so every target use is covered. It is not an
   unconstrained oracle.
3. **`appendBody`, `compareBody`, `compareDef`** — macro-only syntax and
   expansion rules. The exact-KORE comparison in Stage 4 proves that the
   expansion is the submitted translated program.
4. **The priority-40 `#loop` rule** — an operational bridge. It matches any
   active scope whose map binds `"result"` to heap reference `H`, any heap list
   accumulator `ACC`, the exact zip iterator, loop target, and body, and an
   arbitrary `<k>` continuation. It reads `<env>`, `<scopes>`, and `<heap>`;
   writes the result heap object to
   `valSeqConcat(ACC, absDiffs(GAME,GUESS))`; frames the continuation, scope
   allocation, heap allocation counter, stack, return, exception, and exit
   cells; and leaves every scope binding unchanged.

`intVals`, `absDiffs`, and the macros are acceptable. The loop bridge is not.
It preempts the fixed `#loop` rule, skips `#iterNext`, skips `#bindTgt`, skips
each real append call, and has no bridge-free universal connection theorem over
its complete match domain. The finite bridge-free claims do not supply such a
theorem.

### Concrete false-conclusion witness

[`bridge-context-spec.k`](/audit-output/evidence/bridge-context-spec.k) uses
one-element integer inputs `GAME=[1]`, `GUESS=[2]`, the exact candidate loop
target/body, `result -> ref(0)`, and stale bindings `score=99`,
`prediction=88`. This state satisfies every guard of the proof-local bridge.

The extended definition proves the following false transition with exit 0 and
`#Top`: the result heap becomes `[1]` while the stale bindings remain 99 and 88.
See
[05_bridge_false_conclusion_proves.log](/audit-output/evidence/05_bridge_false_conclusion_proves.log).

The bridge-free supplied semantics executes the same loop and reaches heap
`[1]`, `score=1`, and `prediction=2`. It rejects the stale-binding destination
with exit 1 and a `WarnStuckClaimState` whose residual prints those correct
bindings:
[05_bridge_false_conclusion_fixed_rejects.log](/audit-output/evidence/05_bridge_false_conclusion_fixed_rejects.log).

This is the required concrete false conclusion witness on finite integer-list
inputs. It also demonstrates the complete state-footprint defect, not merely
an absent explanatory lemma. The current `compare` body returns `result` and
then pops its local scope, so the bad bindings are not visible in this one
entry postcondition. That does not make the globally false priority rule sound:
its declared match domain accepts other continuations and observable local
state, and the extended theory demonstrably proves a transition the selected
semantics forbids. A rule narrowed to an exact return continuation, or a sound
summary that reproduces the final bindings and is proved by a bridge-free
universal theorem, was not submitted.

## 6. Fresh non-vacuity test

The reviewer-authored
[`spec-vacuity.k`](/audit-output/evidence/spec-vacuity.k) changes a
result-constraining obligation for a satisfying in-domain input:
`compare([1],[2])` is falsely required to return heap list `[2]` instead of
`[1]`.

`kprove --dry-run` parsed and built the mutation successfully with exit 0:
[06_vacuity_dry_run.log](/audit-output/evidence/06_vacuity_dry_run.log).
The real proof run exited 1 with `WarnStuckClaimState`. Its residual shows
`ref(0)` and actual heap list `[1]`, so the failure is exactly the unmet false
result obligation, not a parser error, missing import, timeout, or unrelated
crash:
[06_vacuity_expected_failure.log](/audit-output/evidence/06_vacuity_expected_failure.log).

The entry claim is therefore non-vacuous and result-sensitive. This passes the
non-vacuity subtest but cannot cure the independently false operational bridge.

## 7. Proven versus assumed accounting

### What `#Top` establishes

Under the *extended* theory consisting of the supplied semantics plus every
rule in `verification.k`, K establishes that for arbitrary finite K integer
sequences from the claim's fresh initial configuration, the exact submitted
program reaches a returned heap list equal to recursive `absDiffs` of the two
inputs, truncating at the shorter sequence. It also establishes the two ground
examples. Because the extension theory admits the false loop transition shown
in Stage 5, this is not a legitimate reachability proof about the selected
supplied semantics or real program.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Supplied `reference-semantics` source tree | All K execution | Authorized fixed semantics after exact integrity comparison. Its language is a Python subset, not CPython as a whole. |
| K 7.1.337 compiler/backends and K builtins for maps, lists, strings, unbounded integers, subtraction, equality, and `absInt` | Builds, concrete runs, every proof | Normal low-level toolchain/mathematics trust boundary. |
| Trusted mounted CPython-AST translator | `solution.py` to `solution.mpy` identity | Acceptable designated bridge; byte identity was independently regenerated. |
| Trusted canonical implementation and prompt | Human-facing intent comparison | Acceptable trusted inputs. The differential test is finite evidence only. |
| Integer-only formal domain | Universal theorem | Narrower than untyped prose; consistent with all supplied examples, but non-integer numeric behavior is not proved. |
| 25 fixed opaque/symbolic supplied-semantics operations listed in Stage 5 | None of the target claims | Acceptable as irrelevant to this theorem; no target result or control dependency. |
| `intVals` and `absDiffs` equations | Universal postcondition and loop summary | Truthful, guarded, terminating over every target use. |
| Proof-local priority loop bridge | Universal target closure and both bridge-enabled examples | **Illegitimate.** It replaces program-defined execution, omits loop-target state changes, lacks a bridge-free universal connection theorem, and enables the recorded false conclusion. |
| Four bridge-free finite K proofs and concrete K/Python differentials | Empirical connection evidence | Useful finite evidence; not a universal equivalence proof and not a replacement for sound K reasoning. |
| Missing run metadata/traces | Provenance only | Auditability limitation; does not excuse or cause the semantic defect. |

Gate summary:

- Fresh reconstruction: pass (`#Top` and exit 0 for every positive target).
- Program identity/result constraint/precondition satisfiability: pass.
- Fresh false-postcondition non-vacuity: pass.
- Real-program extension soundness (Gate A): **fail**, with a machine-checked
  false-conclusion witness.
- Intent/evidence: integer-domain and missing-provenance limitations are
  documented, but the Gate A failure already determines legitimacy.

The candidate therefore meets the decision boundary for `FAIL / NOT_LEGIT`:
its reconstructed proof depends on a materially unsound proof rule.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
