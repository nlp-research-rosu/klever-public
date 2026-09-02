VALIDATED

## What is proven

Under the supplied `MPY` semantics, the `parse_music` closure whose body is the
AST in `solution.mpy` satisfies the `SPEC.parse-music` reachability claim for
every finite symbolic `CS:IntSeq`.

Starting with:

- `parse_music` bound to that exact closure;
- argument `str(CS)`;
- an empty heap, empty call stack, `NoExc`, and the standard builtins scope;

the call returns `ref(0)`, the heap contains
`0 |-> list(musicResult(CS))`, the call frame has been removed, the caller
environment is restored, `ret` is `noRet`, and `exc` remains `NoExc`.

This is a K reachability proof of partial correctness. It does not independently
claim termination, although the represented inputs are finite `IntSeq` values
and the implementation consumes one constructor per loop iteration.

## Formal claim and validation scope

The complete claims are in `spec.k`.

- **Program boundary:** the theorem starts at a call with the module binding
  pinned to `closureVal("music_string", .ParamNames, parseMusicBody, 0)`.
  `parseMusicBody` and `parseMusicCharBody` unfold to the exact translated
  function body. Module import/loading trivia is outside the boundary.
- **Input domain:** all `str(CS)` values for finite `CS:IntSeq`; there is no
  validity precondition. This is broader than the prompt's valid music strings.
- **Observed final state:** returned reference, referenced result list,
  environment, scopes, heap allocation counter, stack, return state, exception
  state, and exit code.
- **Intended property:** on valid note tokens, `musicResult` emits `4` for
  `o`, `2` for `o|`, and `1` for `.|`, in order.

`SPEC.scan-loop` is the loop invariant. At a loop head with unprocessed codes
`CS`, pending duration `CUR`, and accumulated list `ACC`, it proves that fixed
execution leaves:

```text
current = scanCurrent(CS, CUR)
result  = scanResult(CS, CUR, ACC)
```

The whole-function claim executes the first iteration itself when the input is
nonempty, applies the exact-frame invariant to the remaining tail, executes the
final pending-whole-note flush, returns, and pops the frame.

For valid tokens, the human-facing interpretation follows by the three token
cases:

- `o` sets the pending value to `4`; whitespace or end-of-input flushes `4`.
- `o|` sets `4`, changes it to `2` at `|`, appends it, and resets the state.
- `.|` sets `1`, appends it at `|`, and resets the state.

Whitespace never emits a second value. Repeating these cases over the token
sequence gives exactly the prompt's output order.

## Proof-extension inventory

There are no trusted primitives, opaque result symbols, simplification axioms,
priority rules, or operational bridges in the proof-local theory.

### `parseMusicBody` and `parseMusicCharBody`

- **Class / role:** definitional summaries of source syntax; they name the
  exact AST and then unfold before fixed semantics executes it.
- **Domain / context:** nullary, total syntax constants; no configuration is
  matched and no continuation or cell is omitted.
- **State footprint / value influence:** the equations themselves read and
  write no state. Their expanded AST subsequently executes through fixed
  lookup, iteration, branch, append, return, and frame rules.
- **Justification:** direct comparison with `solution.mpy`; `prove.sh` also
  checks that the implementation copied into the concrete driver is identical.
- **Dependents / validation:** both positive claims. The changed-body probe in
  `spec-body-mutation.k` changes the `o` assignment from `4` to `5`; the
  original result claim is rejected with a concrete stuck state.

### `nextCurrent` and `nextResult`

- **Class / role:** definitional summaries of one mathematical state-machine
  step; they do not replace a `<k>` computation.
- **Domain:** every `C:Int`, pending `CUR:Int`, and accumulator `ACC:ValSeq`.
- **Coverage / overlap:** `nextCurrent` partitions `C` into `111`, `46`, and
  neither. `nextResult` partitions into pipe with `CUR == 4`, pipe with
  `CUR =/= 4`, other delimiter with `CUR == 4`, and the complementary no-append
  cases. The guards cover the domain and are pairwise disjoint.
- **State footprint / value influence:** mathematical values only; they define
  the final pending value and list used by both claims.
- **Justification:** each equation is the corresponding branch of
  `parseMusicCharBody`; the invariant machine-checks the connection to fixed
  execution for symbolic character and pending values.
- **Dependents / validation:** `scanCurrent`, `scanResult`,
  `SPEC.scan-loop`, and `SPEC.parse-music`; the prompt LLVM run and the
  differential test exercise all three token branches.

### `scanCurrent` and `scanResult`

- **Class / role:** total definitional folds over `IntSeq`.
- **Domain / descent:** every finite `IntSeq`; base equations cover
  `.IntSeq`, and step equations recurse only on the strict constructor tail.
  Base and step patterns do not overlap.
- **Context / state footprint:** no configuration match and no execution
  replacement. They summarize only the pending integer and result `ValSeq`.
- **Value justification:** composition of the exhaustively defined
  `nextCurrent` and `nextResult` steps.
- **Dependents / validation:** both positive claims. `SPEC.scan-loop` is the
  universal fixed-semantics connection theorem for these two values.

### `musicResult`

- **Class / role:** total definitional final-result summary.
- **Domain / coverage:** every finite `CS:IntSeq`. Since `scanCurrent` has sort
  `Int`, the guards `==Int 4` and `=/=Int 4` are exhaustive and disjoint.
- **State footprint / value influence:** no operational state; it fixes the
  observable final heap list in `SPEC.parse-music`.
- **Value justification:** it uses `scanResult` and exactly the source's final
  `if current == 4: result.append(current)`.
- **Dependents / validation:** the whole-function claim, false-postcondition
  probe, concrete prompt example, and differential test.

### `SPEC.scan-loop`

- **Class / role:** derived auxiliary reachability claim used coinductively as
  the loop invariant, not an ordinary rewrite or operational bridge.
- **Matched context:** exact loop term and body; exact local keys
  `music_string`, `result`, `current`, and `char`; the result heap location;
  arbitrary parent scope, continuation suffix, other scopes, and other heap
  entries.
- **Justification scope / containment:** the claim itself is machine-checked
  over that complete symbolic match domain using fixed `MPY` rules. The body
  has no return, break, continue, allocation, or exception effect. Framed
  control cells and the continuation are preserved.
- **State footprint:** reads the four pinned locals and result heap entry;
  changes `char`, `current`, and that list; preserves the input/reference,
  parent, continuation, and all framed cells.
- **Value justification:** the exhaustive state-step equations above, connected
  to the exact body by this claim.
- **Dependent / validation:** `SPEC.parse-music`; focused and full proof runs
  both print `#Top`.

### Validation-only mutation constants

`mutatedParseMusicBody` and `mutatedParseMusicCharBody` are exact syntax aliases
used only by `spec-body-mutation.k`. No positive claim references them, so they
do not contribute to target closure. They exist solely to make body sensitivity
reproducible.

## Exact commands and actual outputs

The complete executable record is `prove.sh`; the captured run is
`prove-output.log`. The end-to-end command was:

```bash
./prove.sh > prove-output.log 2>&1
```

It exited `0`. Its substantive commands and observed results were:

```bash
python3 py2mpy.py solution.py > solution.mpy
# Exit: 0

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
# Exit: 0 (only supplied-semantics compiler warnings)

krun concrete-example.mpy --definition runtime-kompiled
# Exit: 0
# Final <k>: .K
# Final <exit-code>: 0
# Result heap list:
# [4, 2, 1, 2, 2, 1, 1, 1, 1, 4, 4]

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
# Exit: 0 (only supplied-semantics unused-variable warnings)

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.scan-loop
# Output: #Top
# Exit: 0

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
# Output: #Top
# Exit: 0

kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
# WarnStuckClaimState; actual empty result versus required [99]
# Exit: 1 (expected)

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
# WarnStuckClaimState; changed body returns [] for "o" versus required [4]
# Exit: 1 (expected)

python3 differential_test.py
# differential cases=7266 mismatches=0
# Exit: 0
```

Tool versions used:

```text
K version v7.1.293
Python 3.10.12
```

## Gate results

### Gate A — PASS

- **A1:** the exact program-defined body, binding, arguments, environment,
  branches, append calls, return, and frame cleanup execute under fixed
  semantics. Changing the whole-note assignment to `5` makes the ground `"o"`
  theorem fail with the actual empty list.
- **A2:** no operational bridge skips any state transition. The claim observes
  the returned value, heap list, allocation counter, scopes, stack, return
  state, exception state, and exit code.
- **A3:** lookup, left-to-right calls, mutation, continuation, return, and
  binding use supplied rules. The loop invariant pins the exact local frame and
  body; it does not admit closure cells or a broader body.
- **A4:** all proof-local total functions have exhaustive, non-overlapping
  equations and structurally decreasing recursion. No false or opaque
  simplification rule is present.
- **A5:** the empty string is a realizable witness and yields `[]`. Requiring
  `[99]` in `spec-vacuity.k` is rejected with exit `1` and a residual whose
  actual heap contains `.ValSeq`.

### Gate B — PASS

- The formal input sort includes every valid prompt string and does not
  strengthen the contract.
- The supplied string model is sufficient for the task's ASCII tokens; the
  theorem does not depend on unsupported full-Python facilities.
- The three token cases above connect the execution summary to the legend.
  The prompt example and whitespace layouts agree with the independent oracle.
- The implementation and requested entry signature agree with `prompt.py`.

### Gate C — PASS

- The trust ledger below names every component outside the theorem and its
  effect.
- `prove.sh`, both mutation specs, the concrete driver, differential test, and
  captured output all exist and contain exact reproducible commands/results.
- Formal results, mathematical adequacy reasoning, finite evidence, and
  excluded behavior are separated explicitly.

## Trust boundary

| Component outside this theorem | Effect and dependents | Evidence |
|---|---|---|
| Supplied `reference-semantics/` | Defines all modeled Python value, binding, control, heap, and return behavior used by both claims. | Read-only supplied input; LLVM prompt execution and mutation residuals exercise the relevant rules. |
| K v7.1.293 compiler, Haskell backend, SMT solver, and LLVM backend | Establish and execute the K judgments; all formal conclusions depend on them. | Two positive `#Top`/exit-0 runs, two discriminating exit-1 runs, LLVM exit 0. |
| Supplied `py2mpy.py` and CPython AST parsing | Determines `solution.mpy`; program-identity reasoning depends on faithful translation. | Translation succeeds; `solution.mpy` visibly contains the exact source AST; the concrete driver uses the identical function text. |
| Human-facing interpretation of `musicResult` as the note legend | Affects intent adequacy, not Gate A's connection between execution and `musicResult`. It is not a separate machine-checked K claim. | Exhaustive three-token case analysis above and 7,266 independent-oracle cases with zero mismatches. |

There is no proof-local trusted primitive or conditional value oracle.

## Empirically supported facts

`differential_test.py` uses Python's `str.split()` plus the independent literal
dictionary `{"o": 4, "o|": 2, ".|": 1}` as its oracle. It does not call or
reimplement the K summary equations.

Its complete scope is every note sequence of length 0 through 5 over the three
tokens, rendered with each of five separators (`" "`, `"  "`, tab, newline,
and CRLF) and with no, leading, trailing, or both surrounding separators,
plus the prompt example. Duplicate empty layouts are counted as executed
cases. Result: `7,266` comparisons and `0` mismatches.

The LLVM run executes the exact implementation text and the prompt assertion
under `MPY-KRUN`; it terminates at `.K` with exit code `0`.

These finite checks support intent/model adequacy. They are not used as a
universal proof or as a substitute for `SPEC.scan-loop`.

## Excluded behavior

- The theorem is partial correctness and does not state a separate liveness
  theorem.
- Module loading and the no-op handling of `from typing import List` are outside
  the call boundary.
- Inputs are modeled as `str(IntSeq)` values; non-string arguments, CPython
  type errors, memory exhaustion, and behavior absent from the supplied subset
  semantics are excluded.
- For strings outside the prompt's note language, the formal theorem still
  characterizes this implementation by `musicResult`, but no HumanEval
  correctness meaning is claimed for those strings.
