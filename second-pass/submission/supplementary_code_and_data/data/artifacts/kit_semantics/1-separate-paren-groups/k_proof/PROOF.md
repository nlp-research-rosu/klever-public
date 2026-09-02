VALIDATED

# What is proven

Under the supplied `MPY` semantics, `separate_paren_groups` is partially
correct for every `str(IntSeq)` accepted by `validParenInput`: ASCII space
(code 32) is ignored, the only other characters are balanced `(` and `)`, no
prefix has negative depth, and final depth is zero.

If the call terminates, it returns `ref(0)` and heap location `0` contains
`list(separateParenGroupsSpec(S))`.  The mathematical specification emits the
space-free current group exactly when its nesting depth returns to zero.
The theorem also fixes normal control completion: empty stack, `noRet`,
`NoExc`, and exit code 0.

This is a partial-correctness result.  It is a theorem about the exact
translated function body and the supplied reference semantics, not a general
proof of CPython or of the translator.

# Formal claims

`spec.k` contains two claims, proved together:

1. `SPEC.loop-invariant` starts at the fixed semantics' recurring
   `#loop(str(S), Name("char"), BODY)` configuration.  It quantifies over the
   remaining input, depth, current group, emitted output, continuation, local
   scope, heap frame, stack, and allocation counters.  Fixed-semantics
   execution changes the output heap from `list(OUT)` to
   `list(scanParenGroups(S,D,CUR,OUT))`.
2. `SPEC.function-correct` starts with
   `Call(Name("separate_paren_groups"), str(S))`.  Scope 0 binds that name to
   a closure containing the exact `solution.mpy` body.  It requires
   `validParenInput(S)` and concludes that heap location 0 contains
   `list(separateParenGroupsSpec(S))`.

The proof obligations are:

- Base: an empty remaining iterator leaves `OUT` unchanged.
- Step: space preserves all scanner accumulators; every other character is
  concatenated, changes depth, and appends/reset exactly when the new depth is
  zero.
- Entry: lookup, call setup, parameter binding, initialization, the loop
  circularity, return lookup, frame pop, and heap escape establish the result.

# Proof-extension inventory

## `scanParenGroups`

- Class: definitional summary.
- Semantic role: names the mathematical value of the loop accumulator; it
  does not rewrite `<k>` and does not replace program execution.
- Domain: all `IntSeq`, integer depths, current `IntSeq`, and `ValSeq`
  accumulators.
- Matched context: value terms only; no continuation, binding, control stack,
  or framed cell is matched.
- Justification scope and containment: the empty and `iCons` equations are
  exhaustive.  The single `iCons` equation uses nested total conditionals for
  code 32, code 40, and the source's remaining branch, including both possible
  zero-depth outcomes.
- State footprint: none.  It reads only its arguments.
- Value influence: determines the list stored in the target heap cell and thus
  the final returned list.
- Value justification: structural recursion on a strictly shorter remaining
  `IntSeq`; its state transitions are the same equations discharged by
  `SPEC.loop-invariant`.
- Dependents: both formal claims.
- Validation: universal loop claim `#Top`; false-result and body-sensitivity
  probes rejected; 325 independent finite cases had zero mismatches.

## `separateParenGroupsSpec`

- Class: definitional summary.
- Semantic role: initializes `scanParenGroups` with depth 0 and empty current
  and output accumulators; no execution is replaced.
- Domain: all `IntSeq`.
- Matched context/state footprint: value term only; no cells.
- Value influence: final postcondition.
- Justification: one unconditional equation to
  `scanParenGroups(S, 0, .IntSeq, .ValSeq)`.
- Dependents: `SPEC.function-correct`.

## `validParenInput` and `validParenSuffix`

- Class: definitional summary of the formal input domain.
- Semantic role: precondition only; no execution is replaced.
- Domain: all `IntSeq` and all integer depths.
- Coverage: empty, space, open parenthesis, close at positive depth, close at
  nonpositive depth, and every other character.  Cases are exhaustive and
  pairwise disjoint; recursive cases consume one constructor.
- State footprint/value influence: no cells; controls whether the entry theorem
  applies.
- Justification: direct balanced-parenthesis prefix-depth definition.
- Dependents: `SPEC.function-correct`.

## `SPEC.loop-invariant`

- Class: derived reachability claim used coinductively as a loop circularity.
- Semantic role: reasons about fixed execution at the exact `#loop` head.  It
  is not an ordinary rewrite and does not preempt a semantics rule.
- Domain: every `IntSeq`, depth, current group, output list, and matching
  complete configuration.
- Matched context: exact translated loop body; arbitrary preserved
  continuation; current environment `L`; exact five-key local frame
  (`paren_string`, `groups`, `current`, `depth`, `char`); framed outer scopes
  and heap; group heap location `H`; stack, allocation cells, return,
  exception, and exit cells.
- State footprint: the fixed semantics may update `char`, `current`, `depth`,
  and heap location `H`.  All other listed cells are preserved.
- Value justification: the claim itself is proved from fixed semantics and the
  truthful equations above, producing `#Top`.
- Dependents: `SPEC.function-correct`.
- Control validation: the source body executes through `#iterNext`,
  `#loopStep`, `#bindTgt`, its statements, and `#loopLbl`; there is no
  return/frame-pop/exception bridge.

There are no task-local operational bridges, priority rules, opaque
result-bearing symbols, trusted primitives, or ordinary `<k>` rewrite rules in
`verification.k`.

# Reproducible commands and actual results

The complete reproducer is `./prove.sh`; its final run exited 0.

```bash
python3 py2mpy.py solution.py > solution.mpy
```

Actual result: exit 0; `solution.mpy` contains the translated import and exact
function AST.

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
krun concrete-tests.mpy --definition runtime-kompiled
```

Actual result: both commands exited 0.  `krun` ended with `<k> .K </k>`,
`<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>`.  `kompile` printed
non-fatal exhaustiveness/unused-variable warnings originating in the supplied
reference semantics.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual result: both commands exited 0.  The positive target proof printed:

```text
#Top
```

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: expected exit 1 with `WarnStuckClaimState`.  For valid witness
`"()"`, the residual heap was
`0 |-> list(vCons(str(iCons(40,iCons(41,.IntSeq))),.ValSeq))`, contradicting
the deliberately empty expected list.

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: expected exit 1 with `WarnStuckClaimState`.  Replacing the
opening-parenthesis increment by a decrement made the residual heap
`0 |-> list(.ValSeq)`, contradicting the unchanged correct `["()"]`
postcondition.

```bash
python3 differential_test.py
```

Actual output and exit 0:

```text
DIFFERENTIAL_CASES=325
MISMATCHES=0
CONCRETE_SOURCE_BODY_MATCH=True
```

# Gate results

- Gate A — PASS.  The exact closure body executes under fixed semantics; all
  relevant operational cells are present; there is no execution bridge or
  oracle; summary equations are total, disjoint by conditional construction,
  and structurally descending; `"()"` is a satisfiable witness; both
  result-sensitivity and body-sensitivity mutations fail as required.
- Gate B — PASS.  The formal domain is exactly the prompt's balanced
  parentheses plus ignored ASCII spaces.  The `IntSeq`/heap-list model is
  adequate for these characters and results.  The emitted-group definition
  matches the requested top-level balanced partition, including nesting and
  adjacent groups.
- Gate C — PASS.  Commands, artifacts, input scopes, outputs, mutation
  residuals, and the independent oracle construction are recorded and
  reproducible.  Formal facts, trust assumptions, finite evidence, and excluded
  behavior are separated below.

# Trust boundary

- `py2mpy.py` is supplied and unmodified.  Its translation from CPython AST to
  MPY constructors is trusted.  It affects the program body consumed by both
  execution and proof.  Evidence: successful translation, visible
  `solution.mpy`, and the AST identity check between the solution and LLVM
  smoke-test copy.
- The supplied, unmodified `reference-semantics/` modules are the fixed
  operational model.  Relevant trusted rules/functions are in `MPY-CORE`,
  `MPY-STR`, `MPY-LIST`, `MPY-OPERATORS`, `MPY-CONTROLS`, `MPY-FUNCTIONS`,
  `MPY-CALL`, and `MPY-TUPLE`; they determine lookup, calls, scope/heap state,
  string iteration/concatenation/comparison, list allocation/append, control,
  and return.  Both claims depend on them.  LLVM execution supplies finite
  evidence; it is not a proof of equivalence with CPython.
- K v7.1.293 and its Haskell backend are trusted to implement reachability
  proof checking correctly.  The positive result is conditional on that tool
  and the supplied semantics.
- Opaque float, sort, digest, and other unrelated primitives present in the
  imported reference semantics are unreachable from this program and have no
  dependent task claim.

# Empirically supported facts

`concrete-tests.py` executes the prompt example plus adjacent groups, deep
nesting, and spaces-only input under the LLVM semantics.  Its assertions all
pass.  `differential_test.py` uses an independently constructed grammar
`group := "(" group* ")"`, forms top-level group sequences through five total
parenthesis pairs, injects five space layouts, and compares 325 cases with the
Python implementation.  It reports zero mismatches.  These are finite evidence,
not substitutes for the universal K claims.

# Excluded behavior

- Inputs containing characters other than ASCII space, `(`, and `)`, unmatched
  closes, or nonzero final depth are outside `validParenInput`.
- Unicode/CPython string behavior beyond those three ASCII characters is not
  modeled or claimed.
- The module-level `typing.List` import and installation of the function
  definition are not the target theorem.  The entry claim starts from a scope
  whose selected binding is pinned to the exact translated closure.
- Total correctness/termination, performance, memory exhaustion, and
  equivalence of the supplied MPY semantics to all of CPython are not claimed.
