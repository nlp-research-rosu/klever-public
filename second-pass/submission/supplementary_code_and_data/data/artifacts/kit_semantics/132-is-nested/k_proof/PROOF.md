VALIDATED

## What is proven

Under the supplied reference semantics, for every finite `IntSeq` `CS` for
which `bracketInput(CS)` is true, loading the exact translated body of
`is_nested` and calling it with `str(CS)` reaches a Boolean `RESULT` satisfying

```k
RESULT ==Bool nestedResult(CS)
```

`nestedResult(CS)` is true exactly when the four characters `[`, `[`, `]`, `]`
occur in that order as a subsequence. This is equivalent to the prompt's
property: `[[]]` is itself a valid nested bracket subsequence, and every valid
bracket subsequence containing a nested pair has `[[]]` as a further
subsequence.

This is a partial-correctness result in the Kit sense. The proof covers the
exact function body, module binding, argument evaluation, loop execution,
return, frame restoration, and returned Boolean under the supplied semantics.

## Formal claims

`SPEC.loop` proves that, in the exact reachable plain function frame, the
fixed-semantics `#loop` over a bracket-only suffix `CS` changes local `state`
from `S` to `nestedScan(CS, S)`. Its precondition is
`0 <= S <= 4` and `bracketInput(CS)`. The local `bracket` value may change;
the original `string` binding and all framed cells are preserved.

`SPEC.program` starts from the reference semantics' initial configuration,
loads the exact `FuncDef` emitted in `solution.mpy`, calls it with symbolic
`str(CS)`, and constrains the returned Boolean with the equation above.

Both required positive claims are proved by the single complete-spec command.
Selecting only `SPEC.program` would remove `SPEC.loop` from the active claim
set, so `prove.sh` intentionally proves the complete `SPEC` module together.

## Proof-extension inventory

The inventory below was rebuilt from `verification.k` and `spec.k` after the
positive proof, rather than copied from the construction notes.

### `nestedStep`

- Class: definitional summary.
- Semantic role: reasons about the mathematical DFA state; it does not match
  or rewrite any Python computation.
- Domain: all pairs of K `Int` values `(C, S)`.
- Matched context and justification scope: exactly
  `nestedStep(C, S)`; there are no configuration cells or continuations.
- Context containment: exact term equality.
- State footprint: none.
- Value influence: supplies the next value used by `nestedScan`, then
  `nestedResult`, `SPEC.loop`, and `SPEC.program`.
- Value justification: the five equations exactly encode the two Python
  tests. The disjoint state regions are `S < 2`, `2 <= S < 4`, and `S >= 4`;
  the first two regions partition on code equality with 91 (`[`) or 93 (`]`).
  These cases are exhaustive over all integers and pairwise disjoint.
- Control and value validation: no control is replaced. The complete spec
  reached `#Top`; the independent brute-force oracle produced zero mismatches.

### `nestedScan`

- Class: definitional summary.
- Semantic role: folds `nestedStep` over an `IntSeq`; it does not replace
  execution.
- Domain: every `IntSeq` and initial K `Int`.
- Matched context and justification scope: exactly
  `nestedScan(CS, S)`.
- Context containment: exact term equality.
- State footprint: none.
- Value influence: fixes the final local `state` in `SPEC.loop` and the value
  tested by `nestedResult`.
- Value justification: the empty equation returns `S`; the constructor
  equation consumes exactly one head code and recurses on the strict tail.
  The equations are exhaustive, disjoint, terminating, and total.
- Control and value validation: no control is replaced. The loop claim proved
  with `#Top`; the independent oracle covered all bracket strings of lengths
  0 through 12.

### `bracketInput`

- Class: definitional summary.
- Semantic role: expresses the prompt's input-domain precondition only.
- Domain: every `IntSeq`.
- Matched context and justification scope: exactly `bracketInput(CS)`.
- Context containment: exact term equality.
- State footprint and value influence: no state is touched; its Boolean
  controls claim applicability.
- Value justification: the empty sequence is accepted and each constructor is
  accepted exactly when its head is code 91 or 93 and its tail is accepted.
  The equations are exhaustive, disjoint, structurally decreasing, and total.
- Validation: all concrete and oracle inputs satisfy this predicate by
  construction.

### `nestedResult`

- Class: definitional summary.
- Semantic role: names the requested mathematical Boolean without replacing
  program execution.
- Domain: every `IntSeq`.
- Matched context and justification scope: exactly `nestedResult(CS)`.
- Context containment: exact term equality.
- State footprint: none.
- Value influence: it is the `SPEC.program` postcondition.
- Value justification: its sole exhaustive equation is
  `nestedScan(CS, 0) ==Int 4`. State 4 is reached only after consuming, in
  order, an opening bracket, another opening bracket, a closing bracket, and
  another closing bracket; it then saturates.
- Validation: the direct brute-force four-index oracle is independent of the
  DFA equations and reported zero mismatches over 8,191 inputs.

### `SPEC.loop`

- Class: derived reachability lemma used coinductively as the loop
  circularity.
- Semantic role: symbolically executes the fixed semantics; it is not an
  operational rewrite or bridge.
- Domain: bracket-only `CS`, `0 <= S <= 4`, environment location 1, and the
  exact plain local frame containing only `state`, `bracket`, and `string`.
- Matched context: the exact translated loop body at `#loop(str(CS), ...)`,
  an arbitrary trailing `<k>` continuation, the exact local frame at location
  1 with parent 0, framed outer scopes, and all other generated configuration
  cells framed unchanged.
- Justification scope and context containment: the reachability claim itself
  is universally quantified over the displayed continuation and framed cells,
  so every matched context lies in the machine-checked claim. It introduces no
  abrupt control and the source loop contains no `break`, `continue`, return,
  exception, heap operation, or output.
- State footprint: reads and writes local `state` and `bracket`; reads the
  iterated suffix; preserves the `string` binding and all framed cells.
- Value influence and justification: the final `state` determines the returned
  Boolean. `nestedScan` fixes it with exhaustive equations.
- Dependents: `SPEC.program`.
- Control and value validation: the claim proved `#Top` on its own and again
  in the complete spec. There is no operational bridge to compare. The body
  mutation probe changed the observed result and was rejected.

There are no proof-local operational bridges, trusted primitives,
`[simplification]` rules, priority rules, opaque symbols, macros, or ordinary
rewrites over Python terms.

## Exact commands and actual outputs

The complete reproducible command sequence is in `prove.sh`. It was run from
`/workspace`:

```bash
chmod +x prove.sh
./prove.sh
```

Actual overall result: exit 0.

The positive proof commands recorded there are:

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual Haskell compilation result: exit 0. It printed only supplied-semantics
unused-variable warnings for `As` and `Bs` in `semantics/str.k`.

Actual positive proof output and status:

```text
#Top
```

Exit: 0.

The concrete LLVM commands were:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
krun concrete_tests.mpy --definition runtime-kompiled
```

Actual LLVM compilation result: exit 0, with the supplied semantics' existing
non-exhaustiveness warnings in unrelated helpers and unused-variable warnings
in `semantics/str.k`. Actual `krun` result: exit 0 with final cells:

```text
<k> .K </k>
<env> 0 </env>
<scopeLoc> 1 </scopeLoc>
<heap> .Map </heap>
<heapLoc> 0 </heapLoc>
<stack> .List </stack>
<ret> noRet </ret>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

The independent differential command was:

```bash
python3 validation.py
```

Actual output and status:

```text
oracle=brute-force four-index subsequence search
domain=all square-bracket strings of lengths 0..12
checked=8191
mismatches=0
```

Exit: 0. `validation.py` also checks that the function AST embedded in
`concrete_tests.py` is identical to `solution.py`.

The A5 false-result mutation command was:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit 1 with `WarnStuckClaimState`; its residual `<k>` value was
`false ~> .K`, which cannot match the deliberately false target `true`.
`prove.sh` recorded:

```text
EXPECTED FAILURE: false-result mutation was rejected
```

The A1 body-sensitivity command was:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit 1 with `WarnStuckClaimState`; changing the initial
assignment from `state = 0` to `state = 4` made the empty-string execution
reach `true ~> .K`, which cannot match the original expected result `false`.
`prove.sh` recorded:

```text
EXPECTED FAILURE: body mutation was rejected
```

Tool versions used:

```text
Python 3.10.12
K version v7.1.293 (build date Fri Oct 03 13:32:35 CDT 2025)
```

## Gate results

### Gate A — PASS

- A1: the exact program-defined body from `solution.mpy` executes under the
  fixed semantics. There is no call or loop bridge. The body mutation was
  rejected with the changed concrete result visible in the residual.
- A2: no execution is skipped. The loop claim explicitly accounts for the
  local `state` and `bracket` writes and frames every other cell.
- A3: fixed rules perform lookup, argument evaluation, iteration, assignment,
  comparison, return, and frame popping. The loop claim matches the exact
  reachable plain frame and proves its arbitrary continuation framing.
- A4: every proof-local function is exhaustive and terminating; `nestedStep`
  guards are pairwise disjoint. No false, overlapping, opaque, or
  execution-preempting rule was found.
- A5: the empty string is a realizable input satisfying `bracketInput`; it
  returns false. The mutation requiring true exited 1 with the unmet result in
  the residual.

### Gate B — PASS

- B1: the formal domain is exactly the prompt's strings containing only square
  brackets. Empty strings are included.
- B2: the supplied semantics models strings as ASCII code sequences. The only
  admitted characters, `[` and `]`, are ASCII, and all used constructs have
  fixed semantic rules. Python and K integers both avoid fixed-width overflow
  in the modeled computation.
- B3: the four-state summary recognizes `[[]]` as a subsequence. The
  equivalence with a valid nested bracket subsequence follows in both
  directions as stated under “What is proven” and is independently supported
  by the brute-force oracle.
- B4: all six prompt examples agree with the implementation, LLVM execution,
  and the stated formal result.

### Gate C — PASS

- C1: the trust ledger below names all external components and their effect.
  No unproved proof-local primitive affects the result.
- C2: every concrete, differential, mutation, and proof command is preserved
  in existing artifacts and in `prove.sh`, with its input scope, oracle, actual
  result, and exit interpretation recorded above.
- C3: the universal fact established by `kprove`, finite empirical evidence,
  trust assumptions, and excluded behavior are stated separately.

## Trust boundary

- The supplied, unmodified `reference-semantics/` definition is trusted as the
  model of the supported Python subset. It determines value, binding, control,
  local state, and exception behavior for both claims. Existing compiler
  warnings concern supplied helpers outside this program's execution path.
- `py2mpy.py` is trusted as the fixed CPython-AST transliterator. The exact
  mandated command regenerated `solution.mpy`, and the formal claim contains
  the same constructor body.
- K v7.1.293, its Haskell prover/backend, LLVM backend, SMT integration, and
  host runtime are trusted implementation components.
- The plain-language reading of “valid subsequence ... nested” as existence of
  `[[]]` in subsequence order is justified mathematically above and supported
  empirically; the finite test does not replace the universal K proof.

## Empirically supported facts

`concrete_tests.py` runs the six supplied examples plus `""`, `"[["`, and
`"]]][[]]"` through LLVM. All assertions completed with `NoExc` and exit code
0. `validation.py` independently enumerates index quadruples rather than
reusing the proof equations and found zero mismatches across every bracket
string of lengths 0 through 12.

## Excluded behavior

- Inputs that are not strings containing only `[` and `]` are outside the
  formal precondition, exactly as stated by the prompt.
- The theorem begins in the supplied semantics' fresh module configuration; it
  does not claim behavior under arbitrary rebinding of `is_nested`.
- This Kit establishes partial correctness. A separate liveness theorem is not
  claimed, although all concrete tests terminate and the source loop consumes
  one character per iteration.
- Behavior of CPython features not modeled by the supplied semantics is not
  claimed.
