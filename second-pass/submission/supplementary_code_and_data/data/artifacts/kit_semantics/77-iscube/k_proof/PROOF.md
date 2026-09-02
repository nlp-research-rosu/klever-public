VALIDATED

## What is proven

Under the supplied `MPY` semantics, the `iscube` name resolves to the exact
closure translated from `solution.py`, its integer argument is evaluated and
bound normally, and the call returns `isCubeInt(INPUT)` for every K `Int`
`INPUT`. This is a partial-correctness reachability result: when the call
terminates, its returned Boolean is the recursively defined exhaustive cube
search on the input's nonnegative magnitude.

The proof includes ordinary name lookup, argument binding, the sign-normalizing
`if`, candidate initialization, the connected loop summary, `return`, frame
pop, and restoration of the caller configuration. `identity-spec.k` separately
proves that loading the translated `FuncDef` produces the exact
`iscubeClosure` used by the entry claim.

Validation scope:

- Program boundary: `Call(Name("iscube"), Int(INPUT))` with the exact closure
  body from `solution.mpy`; no program-defined helper is trusted or omitted.
- Input domain: every mathematical integer, matching the prompt's valid
  integer assumption.
- Observable final state: the returned `Bool`; environment, scopes, heap,
  stack, return state, exception state, exit code, and allocation counters are
  restored or preserved as stated by the complete configuration.
- Intended property: the result is true exactly when the input equals the cube
  of an integer.

## Formal claim

`SPEC.iscube-entry` starts in module environment `0` with
`"iscube" |-> iscubeClosure`, an empty heap and stack, `noRet`, `NoExc`, and
exit code `0`:

```k
<k> Call(Name("iscube"), Int(INPUT:Int)) => isCubeInt(INPUT) </k>
```

`isCubeInt(A)` searches `cubeSearch(-A, 0)` when `A < 0` and
`cubeSearch(A, 0)` otherwise. `cubeSearch(A, C)` returns true when
`C*C*C == A`, false when `C*C*C > A`, and otherwise continues at `C + 1`.
For nonnegative magnitude, the integer cubes are strictly increasing and
unbounded, so this definition is true exactly when some nonnegative candidate
cubes to the magnitude. A negative cube root corresponds by negating that
candidate.

The proof is layered:

1. `IDENTITY.solution-loads-exact-closure` connects the translated function
   definition to `iscubeClosure`.
2. `CONNECTION.search-loop` proves the recurring `#while` configuration using
   fixed semantics only.
3. `SOURCE-CONNECTION.search-loop-source` validates the source `While` state
   through its fixed one-step transition and the independently proved exact
   `#while` connection rule.
4. `SPEC.iscube-entry` proves the arbitrary-integer entry call.

## Proof-extension inventory

### `cubeOf`, `cubeSearch`, and `isCubeInt`

- Extension/class: the `cubeOf` equation, three guarded `cubeSearch`
  equations, and two guarded `isCubeInt` equations are definitional summaries.
- Semantic role: they name mathematical values; they do not match or replace a
  Python computation.
- Domain: all K integers. The `cubeSearch` guards `==`, `>`, and `<` are
  disjoint and exhaustive. The `isCubeInt` guards `< 0` and `>= 0` are
  disjoint and exhaustive.
- Matched context/containment/state footprint: no operational configuration is
  matched; no cell is read or written.
- Value influence: these symbols determine the loop bridge result and the
  entry postcondition.
- Value justification: `cubeOf(I) = I*I*I`; `cubeSearch` is the exhaustive
  increasing candidate search. Its recursion terminates on ground integers
  because integer cubes are unbounded above. `isCubeInt` performs the exact
  sign normalization used by the Python body.
- Dependents: both connection theorems, the operational bridge, and
  `SPEC.iscube-entry`.
- Control/value validation: `CONNECTION.search-loop` proves the value against
  fixed execution universally; ground claims prove `8 -> true` and
  `9 -> false`; the opposite result at `8` is rejected.

### `iscubeClosure`

- Extension/class: nullary definitional abbreviation.
- Semantic role: names the exact `closureVal` body and does not execute or skip
  it.
- Domain/context/state: one closed value, no operational match, no state
  footprint.
- Value influence: fixes the binding selected by the entry call.
- Justification/dependents: its equation is constructor-for-constructor equal
  to `solution.mpy`; `IDENTITY.solution-loads-exact-closure` proves normal
  loading yields that value. The entry and ground claims depend on it.
- Validation: regenerating `solution.mpy` succeeds; the identity claim prints
  `#Top`; changing `candidate += 1` to `candidate += 2` makes the identity
  mutation fail at exit 1 with the altered closure in the residual.

### Exit-equality simplification

- Extension/class: derived lemma
  `C*C*C == A => cubeSearch(A,C)` under `notBool (C*C*C < A)`.
- Semantic role: simplifies a pure Boolean obligation after fixed execution;
  it replaces no program step.
- Domain: all integers satisfying the guard. Integer trichotomy leaves exactly
  equality (both sides true) or greater-than (both sides false), so the rule is
  true over its complete guard.
- Context/state/value: no operational context or state footprint; it fixes the
  loop-exit Boolean used by both connection theorems.
- Validation: the bridge-free universal connection proof closes; the
  `candidate += 2` witness reaches `false` against the true summary and is
  rejected.

### Scope-deletion simplification

- Extension/class: derived map lemma
  `((1 |-> S) REST)[1 <- undef] => REST` when key `1` is absent from `REST`.
- Semantic role: normalizes the exact map update produced by fixed frame-pop
  execution; it does not skip Python execution.
- Domain: maps satisfying the explicit absence guard. There is no inconsistent
  overlap because K maps have unique keys and the guard excludes key `1` from
  the remainder.
- Context/state/value: pure map term; it affects only the proof's expression of
  the final `<scopes>` cell and no returned value.
- Justification/dependents: the standard update/delete identity for finite
  maps; both connection theorems depend on it.
- Validation: the fixed-semantics connection theorem closes for an arbitrary
  preserved remainder `SC:Map`.

### `CONNECTION.search-loop`

- Extension/class: derived reachability lemma/circularity.
- Semantic role: proves, without an operational bridge, the exact `#while`
  execution and final frame cleanup.
- Domain/matched context: arbitrary integers `A,C`; exact cube guard and
  `candidate += 1` body; singleton `Return(...) .Stmts`; `#endcall`; empty
  trailing K continuation; env `1`; exact local bindings at scope `1`;
  arbitrary disjoint preserved `SC`; scope location `2`; empty heap; heap
  location `0`; exactly one `frame(.K,0,1)`; `noRet`, `NoExc`, exit code `0`.
  The generated counter is framed and preserved.
- State footprint: returns `cubeSearch(A,C)`, restores env `0`, removes local
  scope `1`, restores scope location `1`, empties the stack, and preserves all
  remaining cells.
- Value/control justification: fixed `MPY` semantics plus the truthful
  definitions and derived lemmas above.
- Dependents: the exact executable rule in `connection-rule.k`.
- Validation: bridge-free definition, `#Top`, exit 0. With the bridge-enabled
  definition the identical claim closes at depth 1. Mutating the loop step to
  `+= 2` fails on the ground `A=1,C=0` witness.

### `CONNECTION-RULE` operational bridge

- Extension/class: operational bridge encoding the already proved
  `CONNECTION.search-loop` theorem.
- Semantic role: replaces the exact recurring `#while` execution, return, and
  frame pop with its proved result.
- Domain/matched context/state footprint/value influence: identical to
  `CONNECTION.search-loop`, including its empty continuation, exact stack,
  local bindings, framed remainder, and every explicit cell. Its result
  determines the returned Boolean.
- Justification scope/containment: the rule's LHS, RHS, and complete
  configuration are identical to the bridge-free theorem; therefore every
  rule match lies within the theorem domain.
- Dependents: `SOURCE-CONNECTION.search-loop-source`, `SPEC.iscube-entry`, and
  the ground-value claims.
- Control/value validation: bridge-free versus bridge-enabled executions both
  print `#Top`; a widened singleton-return suffix is rejected and remains at
  `#while`; body and false-result mutations are rejected.

### `SOURCE-CONNECTION.search-loop-source`

- Extension/class: derived reachability lemma.
- Semantic role: validates that the source `While` control state reaches the
  same result after the fixed `While => #while` step.
- Domain/context/state: the exact source-loop configuration stated by the
  claim; the only difference from the `#while` theorem is the one fixed
  `While => #while` semantics step.
- Justification: it imports only `CONNECTION-RULE`, whose exact `#while`
  behavior was independently proved bridge-free. It introduces no additional
  rule into the entry definition.
- Dependents: validation evidence only.
- Validation: `#Top`, exit 0. The extra `Assign("probe",7)` continuation does
  not match `CONNECTION-RULE` after the fixed source step and exits 1.

## Exact commands and actual outputs

The complete reproducible command is:

```bash
./prove.sh > prove.log 2>&1
```

Actual exit: `0`.

`prove.sh` contains the exact translator, LLVM, Haskell, `krun`, `kprove`,
mutation, context, and differential commands. The final `prove.log` contains
six positive `#Top` lines, each from an exit-0 `kprove` command:

```text
IDENTITY                         #Top
CONNECTION                       #Top
SOURCE-CONNECTION                #Top
SPEC                             #Top
GROUND-VALUES                    #Top
CONNECTION with main, depth 1    #Top
```

The LLVM `krun concrete_tests.mpy --definition runtime-kompiled` run completed
with `<k> .K </k>`, `<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>`.
All compile commands exited 0. Compiler warnings shown in `prove.log` are from
the supplied semantics' broad unused/non-exhaustive cases plus one intentionally
unused matched map value; no compiler error occurred.

Negative validation outputs are actual expected failures:

```text
EXPECTED FAILURE: identity mutation exit 1
EXPECTED FAILURE: connection mutation exit 1
EXPECTED FAILURE: widened bridge context exit 1
EXPECTED FAILURE: false postcondition exit 1
```

The connection mutation residual returns `false` where `cubeSearch(1,0)` is
true. The false-postcondition residual for input `8` contains `<k> true </k>`
against the mutated target `false`. The context probe remains at `#while` with
the extra `Assign("probe",7)` suffix, showing the operational bridge did not
accept the widened context.
Full residuals are preserved in `identity-mutation.log`,
`connection-mutation.log`, `bridge-context-probe.log`, and
`spec-vacuity.log`.

The independent differential output is:

```text
inputs: 2001
range: -1000..1000
mismatches: 0
```

## Gate results

- Gate A — PASS.
  - A1: normal loading is connected to the exact closure; both closure and loop
    body mutations fail.
  - A2: the sole operational bridge has a full-configuration connection
    theorem covering result, env, scopes, locations, heap, stack, return,
    exception, exit, and framed generated-counter state.
  - A3: lookup/binding execute normally; bridge contexts are identical to
    their justification domains; a broader continuation does not match.
  - A4: function guards are exhaustive/disjoint, recursion is ground-total,
    and both simplification equations are true over their guards.
  - A5: input `8` is realizable, produces true, and the false target is
    rejected at exit 1.
- Gate B — PASS.
  - B1: the formal domain is all integers, with no hidden restriction.
  - B2: the used subset has mathematical unbounded integers, matching Python
    integer arithmetic for these operations; no text, collection, float,
    concurrency, or external-state behavior is involved.
  - B3: the recursive summary is mathematically the exhaustive search for a
    cube root after sign normalization; this intent bridge is derived above
    and independently tested, though not encoded as a quantified existential
    K theorem.
  - B4: examples and mutations agree with the implementation and prompt.
- Gate C — PASS.
  - C1: all proof extensions and external trust are inventoried here.
  - C2: artifacts, exact commands, logs, input scopes, oracle, and actual
    results are present and reproducible.
  - C3: formal results, mathematical adequacy reasoning, finite evidence, and
    excluded behavior are separated explicitly.

## Trust boundary

- The supplied read-only `reference-semantics/` definition is trusted as the
  execution model. The formal claims establish facts under that definition,
  not directly under the full CPython implementation.
- `py2mpy.py` is trusted to transliterate CPython AST faithfully. The delivered
  term is regenerated on every `prove.sh` run, concrete execution uses it, and
  the identity theorem pins its exact function body.
- The K compiler, Haskell backend, SMT reasoning, LLVM backend, and their
  runtime dependencies are trusted proof/execution infrastructure.
- The equivalence between increasing nonnegative cube search and the
  human-facing existential phrase “cube of some integer” is a standard
  mathematical adequacy argument, not a separately quantified K claim. The
  recursive definition, sign correspondence, strict monotonicity, and
  unboundedness supply the argument; differential evidence supports it
  finitely.
- No opaque value primitive, trusted Python helper, or unproved
  program-derived oracle is used.

## Empirically supported facts

- `concrete_tests.mpy` executes the exact implementation under the supplied
  LLVM semantics on all six prompt examples plus `-64`, `-2`, `8`, and `27`;
  all assertions pass and the exit code is 0.
- `differential_test.py` compares `solution.iscube` with an independent set of
  cubes generated from roots `-10..10` over every input `-1000..1000`:
  2,001 inputs and zero mismatches.
- `GROUND-VALUES` independently constrains two distinct K outcomes:
  `iscube(8) == true` and `iscube(9) == false`.
- Finite evidence supports adequacy and implementation alignment; the
  universal program-to-summary connection comes from the K proofs, not from
  testing.

## Excluded behavior

- The K theorem is partial correctness and does not itself prove termination
  or a resource bound. Mathematically the candidate loop terminates for every
  integer, but very large magnitudes may be slow in CPython.
- Non-integer, invalid, or resource-exhausting inputs are outside the prompt's
  input contract.
- Full CPython behaviors not used by this function, implementation-specific
  limits, and external state are outside the supplied reference semantics and
  theorem.
