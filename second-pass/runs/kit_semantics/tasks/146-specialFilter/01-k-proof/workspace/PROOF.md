VALIDATED

## What is proven

Under the supplied MPY semantics, `specialFilter` is partially correct for every
arbitrary finite list of integers, with no bound on list length or integer
magnitude. If the call terminates, it returns the number of input integers that
are greater than 10 and whose first and last decimal digits are odd.

The target claim loads the exact translated function body, resolves the
`specialFilter`, `str`, and `ord` bindings through the real scope chain, creates
and pops the real call frame, executes the real loop body, and constrains the
final `<k>` result to `specialCount(INPUT)`. It also observes that the module
binding remains, the local frame is removed, and the environment, heap,
allocation counters, stack, return state, exception state, and exit code have
their stated final values.

This is a partial-correctness theorem, not a separate liveness theorem.

## Formal claim

The required target is `SPEC.special-filter` in `spec.k`:

- Domain: `INPUT:ValSeq` satisfying `allInts(INPUT)`.
- Program boundary: `#loadAll(Module(FuncDef(...)))` for the exact
  `solution.mpy` body, followed by
  `Call(Name("specialFilter"), list(INPUT))`.
- Result: `specialCount(INPUT)`.
- Observable final state: result, module binding, environment, scope counter,
  heap, heap counter, stack, return state, exception state, and exit code.

`specialCount` is structurally recursive over the entire symbolic `ValSeq`.
Its disjoint step cases add one exactly when the projected integer is greater
than 10 and both endpoint decimal character codes are odd. Decimal digit
character codes have the same parity as their digit values because ASCII
`'0'` has even code 48.

`SPEC.filter-loop` is the loop circularity. In the exact reachable call
context, it proves that running the loop over any remaining symbolic
`INPUT:ValSeq` increases `count` by `specialCount(INPUT)`. Its empty and
inductive cases collectively cover arbitrary finite inputs.

## Proof-extension inventory

No added rule bypasses a program-defined operation, call, loop, return, or
state transition. No added trusted primitive is used.

| Extension | Class and semantic role | Domain, context, state, and value justification | Dependents and validation |
|---|---|---|---|
| `filterBody()`, `specialFilterStmts()` | Definitional syntactic summaries (macros) | Expand to the exact constructors in `solution.mpy`; they name syntax and replace no execution. No cells are read or changed by macro expansion. | Both claims. Translator reproduction and the changed-body probe validate body sensitivity. |
| `allInts` | Definitional summary | Total structural predicate: empty is true; a cons is integer-headed and recursively integer-only. Equations terminate and do not overlap. | Claim preconditions. The theorem quantifies directly over native `ValSeq`, not fixed sizes. |
| `definedProjectInt`, `projectIntTotal`, the `#Ceil` characterization, cast orientations, collapse, and idempotence | Derived cast/projection lemmas | `projectIntTotal(V)` is usable only when the fixed sort predicate `isInt(V)` is entailed. The `#Ceil` equation connects it to K's partial `Val :> Int` cast; orientation rules preserve definedness. It reads no configuration cells and cannot manufacture an unguarded value. | The two dispatch twins and `specialCount`. Ground `[15]` and non-qualifying witnesses, plus the opposite-value probe, validate value sensitivity. |
| Guarded `applyCmp(">", V, I)` twin | Derived lemma restating a frozen equation | Complete match is the pure function term under `isInt(V)`. Projection reduces to the same integer selected by the frozen `applyCmp(">", I1:Int, I2:Int) => I1 >Int I2` rule. It has no continuation or state footprint. | Symbolic `num > 10`. The original static rule and twin agree on overlap. |
| Guarded `applyBuiltin("str", V, .Vals)` twin | Derived lemma restating a frozen equation | Complete match is the pure builtin function under `isInt(V)`. Its RHS is exactly the frozen `str(Int)` equation with the defined integer projection. It affects the digit branches but no state or control. | Symbolic `str(num)`. Ground LLVM execution and differential tests validate the concrete behavior. |
| `firstDecimalCode`, `lastDecimalCode` | Definitional summaries | Exact endpoint selections from the fixed `Int2String`/`strToCodes` representation. Every integer string is nonempty, so index 0 and `length - 1` are valid. | Digit predicates and `specialCount`. Supported by K smoke execution and the independent decimal-string oracle. |
| `firstDigitOdd`, `lastDigitOdd`, `isSpecial` | Definitional summaries | Exact modulo-2 predicates over endpoint decimal character codes. Total equations have no competing cases. | Human-facing property and recursive summary. |
| `specialCount` equations | Definitional summary | Structural recursion decreases the `ValSeq`. Empty, non-integer, `<= 10`, first-even, last-even, and both-odd cases are exhaustive and pairwise disjoint. On the theorem domain only integer cases are reachable. | Both claims. The program-to-summary connection is proved by the loop circularity rather than assumed as a result lemma. |
| `SPEC.filter-loop` | Derived auxiliary reachability claim / circularity | Matches the exact loop term, return continuation, active scope, module binding, call frame, empty heap, counters, return/exception state, and exit code reached by the target call. It executes the fixed loop body and changes only the locals shown in its RHS. | `SPEC.special-filter`. It is proved together with the target by the untrusted aggregate `kprove` command. |

### Equation audit

- All recursive definitions descend structurally.
- Projection uses are guarded by `definedProjectInt`.
- The dispatch twins agree with the frozen static equations on their overlap.
- `specialCount` guards are exhaustive and disjoint: non-integer; integer not
  greater than 10; greater than 10 with first digit even; first digit odd and
  last digit even; or both odd.
- No rule states or directly assumes the aggregate result of the program.

## Exact commands and actual outputs

The executable record is `prove.sh`; the complete 481-line output of the final
run is in `prove.log`.

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual results:

- Translator commands: exit 0. A later
  `python3 py2mpy.py solution.py | cmp - solution.mpy` also exited 0.
- LLVM compilation: exit 0, with supplied-semantics exhaustiveness and unused
  variable warnings recorded in `prove.log`.
- `krun`: exit 0 and final `<k> .K </k>`, `<exc> NoExc </exc>`,
  `<exit-code> 0 </exit-code>` after all smoke assertions.
- Haskell compilation: exit 0, with only supplied `str.k` unused-variable
  warnings.
- Aggregate `kprove`: output `#Top`, exit 0. This one command proves every
  claim in `spec.k`; it uses no `--trusted` flag.

The independent differential command in `prove.sh` was:

```bash
python3 test_solution.py
```

Actual output and exit:

```text
cases=1006 mismatches=0
Exit: 0
```

The three negative commands are also in `prove.sh`:

```bash
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
kprove spec-body-mutation.k --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
kprove spec-value-mutation.k --definition verification-kompiled \
  --spec-module SPEC-VALUE-MUTATION
```

Actual results:

- False empty-list result: `WarnStuckClaimState`, actual `<k> 0 ~> .K </k>`,
  exit 1.
- Mutated `count = 1` body with expected result 0: `WarnStuckClaimState`,
  actual `<k> 1 ~> .K </k>`, exit 1.
- Opposite interpretation `[15] => 0`: `WarnStuckClaimState`, actual
  `<k> 1 ~> .K </k>`, exit 1.

`prove.sh` recognizes these as expected failures and itself exited 0 on two
complete consecutive runs.

## Gate results

### Gate A — PASS

- A1: The exact function body and binding execute. Changing the initial count
  from 0 to 1 invalidates the theorem and exposes actual result 1.
- A2: There are no operational bridges. The circularity enumerates and
  preserves the exact reachable configuration cells.
- A3: Lookup, argument evaluation, call framing, builtin calls, loop control,
  return, and frame pop execute under the fixed semantics. Dynamic Int dispatch
  is connected to the fixed subsort rules by guarded total projection.
- A4: The extension equations are terminating, covered, and consistent on
  overlaps.
- A5: The empty input is a realizable witness. Its false result mutation fails;
  `[15]` also rejects the opposite value.

### Gate B — PASS

The HumanEval contract's material domain is arbitrary finite integer arrays:
all negative, zero, positive, and arbitrarily large integers are included, and
there is no list-length bound. Integers at most 10 and all negative integers are
proved not to contribute. For integers greater than 10, `specialCount` states
exactly the first/last odd decimal-digit property. The implementation, summary,
and prompt examples agree.

The task's “array of numbers” is interpreted as an integer array because the
contract applies first and last decimal digits as integer properties. Python
values of unrelated or non-integral classes are not silently included by the
formal precondition.

K `Int` and Python integers are both unbounded. The input is represented by the
supplied semantics' documented read-only bare `list(ValSeq)` form; the program
does not mutate it.

### Gate C — PASS

Every assumption and artifact is named below, all recorded commands are
reproducible, and the empirical evidence uses an oracle independent of the
proof equations.

## Trust boundary

| Trusted component | Influence | Dependents | Evidence |
|---|---|---|---|
| Supplied read-only MPY semantics | Defines Python execution, cells, list iteration, calls, operators, strings, and builtins | All claims | LLVM prompt-example smoke run and body/result mutations |
| K compiler, Haskell backend, SMT reasoning, and reachability logic | Establishes `#Top` under the compiled theory | Formal proof | K v7.1.293; repeat aggregate runs |
| K STRING hook `Int2String` and supplied `strToCodes` rules | Fix decimal integer character codes and therefore both digit predicates | `firstDecimalCode`, `lastDecimalCode`, `specialCount` | Ground K runs plus independent CPython decimal-string oracle |
| Partial-correctness interpretation | Does not establish a separate termination theorem | Reported theorem scope | Explicitly stated here |

There is no proof-local trusted primitive and no trusted proof claim.

## Empirically supported facts

`smoke.py` duplicates the exact solution body and checks both prompt examples
and the empty input under LLVM. All assertions complete with `NoExc` and exit
code 0.

`test_solution.py` compares `solution.specialFilter` with an independent oracle
that tests membership of the first and last decimal characters in
`{"1","3","5","7","9"}`. Its 1006 cases comprise:

- both prompt examples and the empty input;
- every integer from -500 through 2000 in one list;
- explicit threshold, endpoint-digit, and mixed cases;
- integers with 80, 100, and 120 decimal places;
- 1000 deterministic random lists of lengths 0 through 39 with values sampled
  from `[-10^30, 10^30)`.

It reports zero mismatches. This finite evidence supports the decimal
representation bridge; the universal list theorem comes from `kprove`, not
from testing.

## Excluded behavior

- Non-integer list elements are outside the integer-array contract and formal
  precondition.
- The theorem is relative to the supplied MPY semantics and its K hooks; it is
  not a proof of the implementation of K or CPython.
- No separate total-correctness or resource-bound theorem is claimed.
