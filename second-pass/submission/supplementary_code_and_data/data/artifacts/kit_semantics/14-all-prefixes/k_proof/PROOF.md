VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, for every symbolic string value
`str(INPUT:IntSeq)`, the reachability proof establishes that any terminating
execution which loads the translated function, binds it as `all_prefixes`, and
calls it with that input reaches the target configuration with:

- `.K` in the computation cell;
- `NoExc`, modeled exit code `0`, an empty call stack, and the caller
  environment restored;
- `result |-> ref(0)` in module scope; and
- heap location `0` containing
  `list(prefixesAcc(.IntSeq, INPUT, .ValSeq))`.

The exhaustive definition of `prefixesAcc` consumes the input from left to
right. For codes `c1 ... cn`, it constructs the value sequence
`[str(c1), str(c1 c2), ..., str(c1 ... cn)]`. For the empty input it constructs
the empty value sequence. Thus the returned list contains every nonempty prefix
from shortest to longest.

This is a partial-correctness reachability proof in K. It does not separately
state a liveness theorem.

## Formal claim and scope

The target claim is `SPEC.all-prefixes` in `spec.k`. Its program boundary is:

1. the harmless translated `from typing import List`;
2. the exact translated `all_prefixes` definition from `solution.mpy`;
3. lookup and invocation of that program-defined closure on a symbolic
   `str(INPUT)`; and
4. assignment of the returned reference to the module variable `result`.

The claim starts from the supplied semantics' standard module and builtins
scopes, an empty heap, and empty control state. The formal input domain is every
finite `IntSeq`, which is exactly the supplied semantics' representation of a
string value. Non-string Python values are outside the typed task contract.

The observed final state includes the returned reference and its heap content,
module bindings, allocation counter, environment, stack, return state,
exception state, exit code, and completed computation. Function-local
`prefix`, `char`, and the function frame are not externally observable and are
removed by the fixed call semantics.

`SPEC.loop-invariant` covers the exact translated `for` loop. At a loop head
with accumulated prefix `P`, remaining characters `R`, and output `ACC`, it
establishes:

- final output `prefixesAcc(P, R, ACC)`;
- final local prefix `finishPrefix(P, R)`; and
- final loop-target value `finishChar(CH, R)`.

## Proof-extension inventory

The inventory below was rebuilt from `verification.k` and `spec.k` after the
successful proof. There are no imported proof-local modules beyond those
files.

### `prefixesAcc`

- **Class:** Definitional summary.
- **Semantic role:** Names a mathematical output value; it does not match a
  `<k>` cell or replace program execution.
- **Domain:** All `P:IntSeq`, `R:IntSeq`, and `ACC:ValSeq`.
- **Matched context / justification scope / containment:** Pure
  `prefixesAcc(P,R,ACC)` terms only; no continuation, bindings, cells, frames,
  or operational context are matched. The equations cover that exact complete
  term domain.
- **State footprint:** None.
- **Value influence:** Determines the final list in both the loop claim and the
  target claim.
- **Value justification:** The `.IntSeq` equation returns `ACC`. The `iCons`
  equation appends `str(P + current-character)` and recurses on the strict tail.
  These constructor cases are exhaustive and disjoint.
- **Dependents:** `SPEC.loop-invariant` and `SPEC.all-prefixes`.
- **Control/value validation:** Not an operational bridge. Structural descent
  proves termination of the definition; concrete K assertions cover empty,
  singleton, multi-character, whitespace, and punctuation inputs; the false
  postcondition is rejected.

### `finishPrefix`

- **Class:** Definitional summary.
- **Semantic role:** Describes the final value of a function-local string after
  the loop; it does not replace execution.
- **Domain:** All two `IntSeq` arguments.
- **Matched context / justification scope / containment:** Pure function terms
  only, with exhaustive `.IntSeq` and `iCons` cases.
- **State footprint:** None.
- **Value influence:** Constrains only the loop claim's local `prefix` binding;
  the binding is deallocated before the target claim terminates.
- **Value justification:** Each step concatenates the next one-character
  string and recurses on the strict tail.
- **Dependents:** `SPEC.loop-invariant`.
- **Validation:** Constructor-disjoint, total, structurally decreasing, and
  exercised by the successful loop proof.

### `finishChar`

- **Class:** Definitional summary.
- **Semantic role:** Describes Python's retained loop-target binding after the
  loop; it does not replace execution.
- **Domain:** Every initial `CH:Val` and `R:IntSeq`.
- **Matched context / justification scope / containment:** Pure function terms
  only, with exhaustive `.IntSeq` and `iCons` cases.
- **State footprint:** None.
- **Value influence:** Constrains only the loop claim's local `char` binding;
  the binding is deallocated before the target claim terminates.
- **Value justification:** Empty input retains `CH`; each nonempty step replaces
  it with the current one-character string and recurses on the strict tail.
- **Dependents:** `SPEC.loop-invariant`.
- **Validation:** Constructor-disjoint, total, structurally decreasing, and
  exercised by the successful loop proof.

### `SPEC.loop-invariant`

- **Class:** Derived reachability lemma used coinductively as the loop
  circularity.
- **Semantic role:** Summarizes exact fixed-semantics execution after its own
  base and inductive obligations are proved; it is not an ordinary rewrite in
  `verification.k`.
- **Domain:** Arbitrary remaining `R`, accumulated prefix `P`, output `ACC`,
  previous `CH`, input binding, heap location, environment location, framed
  scopes, framed heap, continuation, and omitted preserved configuration cells.
- **Matched context:** The exact `#loop(str(R), Name("char"), BODY)` generated
  by the fixed `For` rules; the exact assignment, string concatenation, bound
  `append`, and expression-discard body; the local bindings for `string`,
  `prefixes`, `prefix`, and `char`; heap location `H` containing `list(ACC)`;
  and an arbitrary trailing continuation represented by the `<k>` frame.
- **Justification scope and context containment:** The machine-checked claim is
  quantified over the same arbitrary continuation and framed maps that it
  matches. The body contains no return, break, continue, exception operation,
  or cleanup effect. Each nonempty iteration executes lookup, string
  concatenation, target binding, list mutation, statement discard, and the
  fixed loop back-edge before the circularity applies to the strict tail.
- **State footprint:** Reads the computation, environment, listed local
  bindings, and heap list. Writes `prefix`, `char`, and the contents of heap
  location `H`. Preserves `string`, `prefixes`, the environment, other
  scope/heap entries, the continuation, and all omitted cells.
- **Value influence:** Supplies the exact list content used by the target
  claim. Its values are fixed by the three exhaustive summaries above.
- **Dependents:** `SPEC.all-prefixes`.
- **Control/value validation:** `SPEC.loop-invariant` itself prints `#Top`.
  The full target also prints `#Top`. A material body mutation is rejected and
  shows `["a","b","c"]` rather than the expected `["a","ab","abc"]`.

`SPEC.all-prefixes` is the target theorem, not an additional proof extension.
The audit found no proof-local simplification axioms, priority rules,
operational bridges, opaque/no-evaluator symbols, or trusted primitives.

## Reproduction commands and actual results

The complete sequential runner is `./prove.sh`. It exited `0`. Its substantive
commands and recorded results are:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 test_solution.py
# CPython oracle cases passed: 8

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
# Exit: 0 (reference-semantics compiler warnings are recorded in kompile-llvm.out)

python3 py2mpy.py concrete-validation.py > concrete-validation.mpy
krun concrete-validation.mpy --definition runtime-kompiled
# Exit: 0
# Relevant final cells: <k> .K </k>, <exc> NoExc </exc>,
#                       <exit-code> 0 </exit-code>
# Full output: krun.out

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
# Exit: 0

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant
# Output: #Top
# Exit: 0
# Full output: kprove-loop.out

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
# Output: #Top
# Exit: 0
# This command proves every claim in spec.k.
# Full output: kprove.out

kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
# Expected output: WarnStuckClaimState; residual AssertionError,
#                  modeled <exit-code> 1
# Actual process exit: 1
# Full output: vacuity.out

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
# Expected output: WarnStuckClaimState; residual AssertionError,
#                  modeled <exit-code> 1
# Actual process exit: 1
# Full output: body-mutation.out
```

The LLVM concrete assertions cover `""`, `"a"`, `"abc"`, `"xy"`, `"a a"`,
and `"!?"`. The independent CPython oracle additionally covers `"prefix"` and
`"0123456789"`.

## Gate A — PASS

- **A1, program identity and body sensitivity:** The target claim embeds the
  translated body shown in `solution.mpy`; the program-defined closure executes
  under the fixed semantics from definition through return and frame pop.
  `spec-body-mutation.k` changes `prefix = prefix + char` to `prefix = char`.
  On witness `"abc"`, K reaches `["a","b","c"]`, the assertion fails, and
  `kprove` exits `1`.
- **A2, operational state:** No operational bridge exists. The loop claim
  explicitly constrains every state location the loop modifies and frames the
  remainder.
- **A3, binding/evaluation/control:** Fixed rules perform callee lookup,
  argument evaluation, closure binding, string iteration, attribute binding,
  append dispatch, return, and frame cleanup. The loop claim matches the exact
  body and is quantified over its accepted continuation.
- **A4, logical consistency:** Each proof-local total function has exactly the
  disjoint `.IntSeq` and `iCons` cases. Recursive calls consume the strict tail.
  There are no overlapping guards or fallback equations.
- **A5, non-vacuity:** `"abc"` is a realizable witness. The intended run
  produces `["a","ab","abc"]`. `spec-vacuity.k` deliberately omits `"ab"`;
  the residual shows the actual and wrong heap lists, `AssertionError`, and
  modeled exit code `1`. The mutation is rejected with process exit `1`.

## Gate B — PASS

- **Input alignment:** The task's annotated domain is `str`; the theorem covers
  every finite string value in the supplied semantics and adds no length or
  character restriction.
- **Model alignment:** The proof uses only the supplied model's ordinary
  function calls, finite string iteration and concatenation, list allocation,
  `append`, and return. It does not depend on unsupported Python behavior.
  Non-string calls and full CPython behaviors outside this subset are excluded.
- **Property alignment:** The base/step equations for `prefixesAcc`
  definitionally produce each successively extended prefix in shortest-to-
  longest order. Empty input produces `[]`, matching the contract.
- **Implementation alignment:** The implementation accumulates one character
  per loop iteration and appends the new accumulated string. Concrete and
  mutation evidence agree with the source examples and contract.

## Gate C — PASS

### Trust ledger

- **Supplied reference semantics:** Trusted as the fixed execution model named
  by the task. It affects all claims at value, control, heap, scope, and call
  levels. Evidence consists of the symbolic proof plus LLVM concrete
  assertions. Correct correspondence of that supplied model to all of CPython
  is outside this theorem.
- **`py2mpy.py`:** Trusted as the task-supplied fixed AST transliterator.
  `solution.mpy` is regenerated by the required command and its function body
  is visibly identical to the body embedded in `SPEC.all-prefixes`.
- **K toolchain and Haskell proof backend:** Trusted for parsing, rewriting,
  reachability reasoning, and the `#Top` result.
- **CPython test oracle:** Empirical evidence only. `test_solution.py`
  independently defines the expected result with slicing and `range`; no formal
  claim depends on this oracle.

There is no unproved proof-local value or control assumption. The LLVM compiler
reports non-exhaustiveness warnings in unrelated supplied-reference functions
(`mapStrVS`, float helpers, `joinCodes`, and out-of-bounds `valSeqAt`) and
unused-variable warnings in `strLt`. None of those symbols occurs on this
program's execution or proof path. The Haskell build and both positive proofs
exit successfully.

### Reproducible evidence

- `concrete-validation.py` is the K-side finite test artifact. Its oracle is an
  explicit expected list in each assertion. Complete input scope:
  `""`, `"a"`, `"abc"`, `"xy"`, `"a a"`, `"!?"`. Result: zero failed
  assertions, `.K`, `NoExc`, modeled exit code `0`.
- `test_solution.py` is the independent CPython-side artifact. Its oracle is
  `[string[:end] for end in range(1, len(string) + 1)]`. Complete input scope:
  the six K cases plus `"prefix"` and `"0123456789"`. Result: eight of eight
  passed, zero mismatches.
- `spec-vacuity.k` and `spec-body-mutation.k` are persistent negative evidence
  artifacts with full residuals in `vacuity.out` and `body-mutation.out`.

Finite tests support adequacy; they are not used as a substitute for the
universal symbolic reachability proof.

## Excluded behavior

- Calls with a non-string argument are outside the typed HumanEval contract and
  the formal `str(INPUT:IntSeq)` precondition.
- The theorem is about the supplied MPY semantics, not every feature or error
  mode of full CPython.
- As required by the Kit workflow, the reachability claims establish partial
  correctness and do not independently prove termination.
