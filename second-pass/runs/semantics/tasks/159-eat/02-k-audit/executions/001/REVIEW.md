# Independent adversarial audit — 159-eat

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program under the supplied MPY semantics. Both positive
claims were rebuilt from source and proved independently. The sole proof-local
equation is an exact name for the submitted function closure; it neither
summarizes nor bypasses the function body. A separate bridge-free claim, built
against only the fixed supplied semantics, proves that loading the submitted
function AST produces that same closure.

The final status is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, because four
explicitly requested generation-accounting artifacts and a structured trace
are absent. That is an audit-provenance limitation, not a soundness or adequacy
failure: all proof-critical source artifacts are present and were reconstructed
independently.

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`. The required trusted mount
`/reference/reference-semantics` is present, so the mount does not contradict
the rendered mode. There is no infrastructure breach.

A physical, non-following walk found no symlink anywhere in either semantics
tree. Recursive `diff -ruN --no-dereference` returned 0. Candidate and trusted
trees have the same directories, regular files, and bytes; there are no
missing, additional, mistyped, changed, or symlinked entries below
`reference-semantics/`.

The following byte comparisons also returned 0:

- `/candidate/prompt.py` versus `/reference/prompt.py`;
- `/candidate/py2mpy.py` versus `/reference/py2mpy.py`;
- `/candidate/reference-semantics/` versus
  `/reference/reference-semantics/`.

The evidence, including physical file types, SHA-256 values, exact comparison
commands, and K version, is in
[stage1_integrity.log](evidence/stage1_integrity.log). The selected tools were
`kompile`, `kprove`, and `krun` version `v7.1.337`.

### Missing provenance artifacts

The following requested artifacts are absent:

- `/candidate/run-input.json`;
- `/candidate/metrics.json`;
- `/candidate/codex-last.txt`;
- `/candidate/codex-output.log`;
- any structured generation trace matching the audited trace search.

Consequently, there were no candidate claims in those files to credit. Their
absence is the reason for the final `CONCERNS` status. It does not prevent
independent identification of the task because the trusted prompt, canonical
program, translator, supplied semantics, submitted Python, submitted MPY,
specification, and verification module are all present.

The candidate's `__pycache__/solution.cpython-310.pyc` is an untrusted cache. It
was not copied into either build and was never loaded. Candidate `prove.sh`,
concrete tests, and other prose-like evidence were inspected only as claims.
The exact source dump is
[source_artifacts.log](evidence/source_artifacts.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For integer inputs `number`, `need`, and `remaining`, each in `0..1000`
inclusive, let:

```text
eaten_now = min(need, remaining)
```

The required result is:

```text
[number + eaten_now, remaining - eaten_now]
```

Thus, if `need <= remaining`, the result is
`[number + need, remaining - need]`; otherwise it is
`[number + remaining, 0]`. This restatement follows both
`/reference/prompt.py` and the two branches of
`/reference/canonical.py`.

`/candidate/solution.py` implements exactly those branches. It uses a final
unconditional return instead of a source-level `else`, but that return is
reached exactly when the preceding branch did not return.

### Trusted translation

The exact command was:

```bash
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
```

It exited 0. Byte comparison with the submitted `solution.mpy` exited 0, and
both files had SHA-256:

```text
49f9697d0fa8809c3144fc5b812d49e68db0cdbb56b74617e8c089e0a8c6e78a
```

See
[stage2_translation_check.sh](evidence/stage2_translation_check.sh) and
[stage2_translation_check.log](evidence/stage2_translation_check.log).

### Independent differential execution

[differential_test.py](evidence/differential_test.py) imports the trusted and
candidate entry points from their exact paths. It does not reuse proof
equations. In addition to comparing both Python implementations, it compares
each result with the independently written `min(need, remaining)` formula.

The input set contained:

- all four documented examples;
- empty, mixed-extreme, and all-extreme cases;
- both sides of the branch and equality at
  `need = remaining - 1`, `remaining`, and `remaining + 1`, where in-domain;
- the complete cube `0..20` on all three arguments;
- 20,000 deterministic PRNG draws from the full documented cube, seed 159.

There were 29,314 unique cases and zero mismatches. Exact command:

```bash
python3 /audit-output/evidence/differential_test.py
```

Exit status was 0; see
[differential_test.log](evidence/differential_test.log). This is finite
adequacy evidence, not a substitute for the K proof.

## 3. Clean proof reconstruction

All source inputs needed for execution were copied to `/tmp/audit-work`.
Candidate-built caches and definitions were neither copied nor referenced. The
scratch build used the trusted copy of the supplied semantics, not a
candidate-provided compiled definition.

### Concrete definition and execution

Exact build:

```bash
cd /tmp/audit-work/rebuild
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled
```

The command exited 0. The warnings about non-exhaustive total functions concern
unused portions of the fixed supplied language (string mapping, floats,
joining, and subscripting); none occurs in `eat`. The bounded build output is
[kompile_concrete.log](evidence/kompile_concrete.log).

Running the submitted MPY:

```bash
cd /tmp/audit-work/rebuild
krun solution.mpy --definition concrete-kompiled
```

exited 0 with `.K`, `NoExc`, exit code 0, and the module scope bound `"eat"` to
the exact closure body later used by the proof. See
[krun_solution_module.log](evidence/krun_solution_module.log).

The independently authored
[concrete_semantics_test.py](evidence/concrete_semantics_test.py) was translated
with the trusted translator and run through the freshly built LLVM definition.
It checks examples, empty input, extrema, equality, and both strict sides of
the branch. `krun` exited 0 with all assertions consumed, `.K`, `NoExc`, and
exit code 0. See
[translate_concrete_semantics_test.log](evidence/translate_concrete_semantics_test.log)
and
[krun_concrete_semantics_test.log](evidence/krun_concrete_semantics_test.log).

### Candidate proof definition

Exact build:

```bash
cd /tmp/audit-work/rebuild
kompile verification.k \
  --backend haskell \
  --main-module EAT-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0; see
[kompile_verification.log](evidence/kompile_verification.log).

The original two-claim spec was proved with:

```bash
cd /tmp/audit-work/rebuild
kprove spec.k \
  --definition verification-kompiled \
  --spec-module EAT-SPEC
```

Actual result: `#Top`, exit 0. See
[kprove_all_claims.log](evidence/kprove_all_claims.log).

Each submitted positive claim was then copied without changing its
precondition, execution, or postcondition into a one-claim audit module and run
independently:

```bash
cd /tmp/audit-work/rebuild
kprove spec-branch-sufficient.k \
  --definition verification-kompiled \
  --spec-module EAT-SPEC-BRANCH-SUFFICIENT

kprove spec-branch-insufficient.k \
  --definition verification-kompiled \
  --spec-module EAT-SPEC-BRANCH-INSUFFICIENT
```

Both printed `#Top` and exited 0. Preserved source copies are
[spec_positive_branch_sufficient.k](evidence/spec_positive_branch_sufficient.k)
and
[spec_positive_branch_insufficient.k](evidence/spec_positive_branch_insufficient.k);
outputs are
[kprove_branch_sufficient.log](evidence/kprove_branch_sufficient.log) and
[kprove_branch_insufficient.log](evidence/kprove_branch_insufficient.log).

### Bridge-free module-load connection

To check the proof's manual initial closure binding independently, a second
Haskell definition was built from only the fixed supplied semantics:

```bash
cd /tmp/audit-work/rebuild
kompile reference-semantics/semantics.k \
  --backend haskell \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition fixed-verification-kompiled
```

It exited 0. The audit claim in
[module_load_connection.k](evidence/module_load_connection.k) starts at
`#loadAll(Module(FuncDef(...)))`, where the `FuncDef` is the submitted MPY
function AST, and requires the fixed module-loading rule to produce the exact
closure used by `verification.k`. It neither imports `verification.k` nor uses
`eatClosure`.

```bash
cd /tmp/audit-work/rebuild
kprove /audit-output/evidence/module_load_connection.k \
  --definition fixed-verification-kompiled \
  --spec-module AUDIT-MODULE-LOAD-CONNECTION
```

Actual result: `#Top`, exit 0. See
[kompile_fixed_haskell.log](evidence/kompile_fixed_haskell.log) and
[kprove_module_load_connection.log](evidence/kprove_module_load_connection.log).

## 4. Adequacy and real-program pinning

### Claim 1: sufficient stock

The precondition requires:

- symbolic K integers `NUMBER`, `NEED`, and `REMAINING`, each from 0 through
  1000;
- `NEED <= REMAINING`;
- module environment 0;
- the exact `"eat"` closure in scope 0, with the fixed builtins scope at -1;
- next scope location 1, empty heap with next heap location 0, empty call stack,
  no pending return, no exception, and exit code 0.

The postcondition requires the call to return exactly `ref(0)`, allocation of
heap location 0 as:

```text
list(vCons(NUMBER +Int NEED,
     vCons(REMAINING -Int NEED, .ValSeq)))
```

and `heapLoc` 1. All framed cells remain exact.

### Claim 2: insufficient stock

The machine-state requirements are identical, but the branch precondition is
`REMAINING < NEED`. The postcondition requires exactly:

```text
list(vCons(NUMBER +Int REMAINING,
     vCons(0, .ValSeq)))
```

at heap location 0, returned as `ref(0)`.

For mathematical integers, `NEED <= REMAINING` and `REMAINING < NEED` are
disjoint and exhaustive. Together, the claims cover the entire stated input
cube.

### Execution and control-flow correspondence

The target claims start at the function invocation rather than at
`#loadAll(solution.mpy)`. This is not a substituted implementation:

1. trusted translation is byte-identical to the submitted MPY;
2. `eatClosure` expands to exactly that translated parameter list, body,
   lexical parent 0, and statement order;
3. the fixed-semantics module-load connection proved in Stage 3 independently
   establishes that the submitted `FuncDef` creates the same closure;
4. after that binding, fixed `Call`, lookup, argument evaluation, frame,
   parameter binding, `If`, comparison, arithmetic, list allocation, `Return`,
   and frame-pop rules execute the real body.

There is no helper or loop claim and no body summary. In the true branch,
`Return` correctly discards the later top-level return. In the false branch,
the empty `else` leaves that top-level return to execute. The list reference
escapes the callee while the callee scope is removed, matching the fixed heap
and frame rules.

The returned reference, heap address, list shape, and both integer elements are
fixed by the postconditions. There is no free result variable, implication-only
result, or tautological postcondition.

### Satisfiable witnesses

[claim_witnesses.py](evidence/claim_witnesses.py) and
[claim_witnesses.log](evidence/claim_witnesses.log) provide one ground witness
per claim:

- sufficient: `(5, 6, 10)` satisfies the first precondition and yields
  `[11, 4]` in the claimed formula, trusted canonical Python, and candidate
  Python;
- insufficient: `(2, 11, 5)` satisfies the second precondition and yields
  `[7, 0]` in all three.

The command exited 0.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

There is no generated `semantic.k` in this supplied-semantics submission. The
applicable sources are the fixed
`reference-semantics/semantics.k`, its 23 required helper files, and the
proof-local `verification.k`.

[k_rule_inventory.py](evidence/k_rule_inventory.py) lexically enumerates every
declaration block from the trusted selected tree and the candidate verification
module. Its complete output,
[k_rule_inventory.log](evidence/k_rule_inventory.log), contains an exact source
location, complete normalized declaration, attributes, origin, reachability
classification, and per-entry assessment for all 930 entries:

| Kind | Count |
|---|---:|
| Configuration | 1 |
| Context | 5 |
| Ordinary rules | 696 |
| Syntax declarations | 228 |
| Total | 930 |

Attribute-bearing declaration-block counts are: 146 `function`, 107 `total`,
25 `symbol`, 45 `priority`, 35 `concrete`, 26 `owise`, 4 `macro`, 2 `strict`,
and 1 `seqstrict`. There are zero `functional`, `simplification`, or `anywhere`
declarations. The inventory also separately lists every opaque/no-evaluator
symbol and every priority rule.

All 928 fixed-semantics entries are byte-identical to the trusted selected
semantics. Entries on the execution path were reviewed against the state and
control transitions below. The remaining fixed rules have syntactic heads for
unused operations—floats, strings, dictionaries, sorting, iteration,
subscripts, builtins, methods, assertions, comprehensions, and related
helpers—and cannot match or generate a term on this program's closed execution
path. This is narrower than asserting that the full supplied language is a
complete Python semantics; the full tree is the selected fixed semantics for
this audit.

### Used construct-to-rule map

| Submitted construct | Declaration and execution rules |
|---|---|
| `Module`, `FuncDef`, `Params`, statement sequence | `syntax.k:53,56-61`; `core.k:124-127`; `functions.k:14-16` |
| `Call(Name("eat"), ...)` | `syntax.k:12,28,37`; `call.k:19-21,69-74`; `core.k:130-154,185-191` |
| `Int` arguments and literal 0 | `syntax.k:9`; `core.k:194` |
| `If` and truth conversion | `syntax.k:49`; `controls.k:51-54`; `core.k:199-205` |
| `Compare(..., CmpOp("<=", ...))` | `syntax.k:30,32`; `operators.k:15-17`; `int.k:23` |
| `BinOp` addition and subtraction | `syntax.k:15`; `operators.k:12`; `int.k:9,13` |
| `ListExpr` and fresh allocation | `syntax.k:17`; `list.k:13-15`; `core.k:117-121,185-191,213-219` |
| `Return` and call-frame cleanup | `syntax.k:50`; `functions.k:8-11,63-90` |

The configuration fixes environment, scope map, heap, allocation counters,
stack, return state, exception state, and exit code. `seqstrict` evaluates
binary operands left-to-right; the comparison contexts evaluate left then
right; the shared argument loop and list-literal loop evaluate elements
left-to-right. The integer rules map `+`, `-`, and `<=` to the corresponding
unbounded K integer operations. The two `#branch` rules are disjoint. List
construction calls `#alloc`, whose freshness guard holds because the claim
starts with an empty heap and heap location 0. The closure call creates scope
1, binds the three parameters in order, pushes the continuation, and `#pop`
restores environment/scope state while retaining the newly allocated list.

No relevant rule overlap, priority preemption, unconstrained allocation,
exceptional path, or omitted observable cell was found. The only fixed
priority rules that can generally concern heap references do not intercept the
integer condition or arithmetic in this body. The generic `[owise]` `Call` rule
is the intended route; the other fixed call interceptors require distinct
attribute-shaped callees such as `math.sqrt` or `hashlib.md5`.

### Proof-local inventory

`verification.k` contributes exactly two inventoried entries:

1. `syntax Val ::= "eatClosure" [function]`;
2. one unconditional equation from `eatClosure` to
   `closureVal(parameters, submitted-body, 0)`.

Classification: **definitional constant**, not an operational bridge. It has
no cell footprint, no continuation match, no priority, no opaque output, no
result equation, and no branch shortcut. Its value influences the callee body,
but the value is completely fixed by the one equation. There are no overlapping
guards or uncovered cases for the nullary symbol. The module-load connection
is a bridge-free universal check of the only configuration in which the
submitted top-level definition is loaded, and the target claims then execute
the body with fixed semantics.

The local rule does not encode either expected answer. The only occurrences of
`NUMBER +Int NEED`, `REMAINING -Int NEED`,
`NUMBER +Int REMAINING`, and zero as result formulas are in the claim
postconditions and in arithmetic produced by execution.

### Opaque and total declarations

The fixed selected semantics includes opaque/no-evaluator functions for floats,
sorts, and an MD5 helper. None is reachable from the submitted syntax or the
target claims, and no such symbol appears in either postcondition. The LLVM
compiler's non-exhaustiveness warnings similarly concern unused fixed
functions. They are recorded as part of the language trust boundary and do not
provide an oracle or false conclusion for the intended integer domain.

No candidate-local rule was found unsound, so there is no unsoundness allegation
requiring a false-conclusion witness. The narrower evidence limitation is that
this audit validates the used supplied-semantics fragment, not every behavior
of the full MPY language on programs containing unused constructs.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; none was credited.

The fresh mutation
[spec_false_result.k](evidence/spec_false_result.k) preserves the first claim's
real call, exact machine state, full satisfiable precondition, returned
reference, and second list element. It changes only the first result element:

```text
NUMBER +Int NEED
```

becomes:

```text
NUMBER +Int NEED +Int 1
```

This is false for every satisfying input; `(5, 6, 10)` is the explicit witness,
because the real first element is 11 and the mutation requires 12.

The mutation first built successfully:

```bash
cd /tmp/audit-work/rebuild
kprove /audit-output/evidence/spec_false_result.k \
  --definition verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT \
  --dry-run
```

Exit status was 0; see
[kprove_false_result_dry_run.log](evidence/kprove_false_result_dry_run.log).

The actual proof command was:

```bash
cd /tmp/audit-work/rebuild
kprove /audit-output/evidence/spec_false_result.k \
  --definition verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT
```

It exited 1 with `WarnStuckClaimState`. The residual reached the exact real
heap:

```text
vCons(NUMBER +Int NEED,
  vCons(REMAINING -Int NEED, .ValSeq))
```

and failed the expected implication because it would need:

```text
NUMBER +Int NEED +Int 1 #Equals NUMBER +Int NEED
```

This is the intended unmet result obligation, not a parser error, missing
import, timeout, unrelated crash, or unreachable mutation. The bounded output
is [kprove_false_result.log](evidence/kprove_false_result.log).

## 7. Proven versus assumed accounting

### Precisely proven

Under the supplied MPY semantics, for every K-integer triple in the documented
`0..1000` cube, invoking the exact submitted `eat` closure from the specified
clean state reaches a normal state that:

- returns a fresh reference to heap address 0;
- stores a two-element list at that address;
- stores `[NUMBER + NEED, REMAINING - NEED]` when
  `NEED <= REMAINING`;
- stores `[NUMBER + REMAINING, 0]` when
  `REMAINING < NEED`;
- advances the heap counter to 1;
- restores the caller environment and empty stack;
- has no pending return, no exception, and exit code 0.

The two claims cover the whole intended integer domain. The module-load
connection establishes, without `eatClosure`, that the submitted top-level
`FuncDef` produces the closure assumed by those entry claims. The false mutation
demonstrates that the successful proof discriminates the exact returned value.

### Trust and assumption ledger

1. **Trusted supplied semantics.** The fixed MPY tree is the semantics selected
   by the problem condition. Its candidate copy is byte-identical. All formal
   conclusions are relative to that semantics. The used fragment was reviewed
   in detail; unused language features are excluded from the theorem.
2. **K implementation and builtin theories.** `kompile`, the LLVM and Haskell
   backends, `kprove`, and K's integer, Boolean, map, and list theories are
   trusted primitives. They affect execution and the arithmetic proof. Fresh
   builds and the non-vacuity residual are reproducible evidence, not proofs of
   the toolchain itself.
3. **Trusted translator.** The mounted translator is trusted to map the Python
   subset to MPY. Its generated bytes equal the submitted MPY. The module-load
   and target K proofs concern those bytes.
4. **Python-to-intent bridge.** The claim that the prompt means the
   `min(need, remaining)` formula is an ordinary-language interpretation,
   supported by the trusted canonical implementation, all four examples, and
   29,314 differential cases. Differential testing is finite and is not used
   to close the K claims.
5. **Opaque fixed symbols.** The selected semantics contains opaque float,
   sorting, and hash symbols. They affect no reachable term, control decision,
   heap value, or postcondition in this proof. There is no proof-local opaque
   or fresh program-derived result.
6. **Partial correctness scope.** The requested logical status is partial
   correctness. The submitted function is straight-line and the reconstructed
   symbolic executions do reach the postconditions without a circularity, but
   the report does not generalize termination or behavior beyond the stated
   integer domain and clean initial state.
7. **Generation provenance.** The four missing accounting files and missing
   structured trace prevent a complete audit of how the candidate was
   generated. No mathematical or semantic proof step depends on them.

Gate A (real-program soundness and non-vacuity) passes. Gate B (intent and
domain adequacy) passes. The independent evidence is reproducible, but the
candidate's generation provenance is incomplete; this is the sole concern and
does not make the proof illegitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
