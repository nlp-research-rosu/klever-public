VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, the translated `can_arrange`
function returns the largest index `i > 0` for which
`not (arr[i] >= arr[i - 1])`; it returns `-1` if no such index exists.

The proof is symbolic and unbounded. It ranges over every finite `ValSeq`
satisfying `scanDefined(VS, 0, 0)`, not over a fixed collection of lengths.
That domain contains:

- empty and singleton lists with any represented value;
- arbitrarily long lists whose adjacent values are any mixture of `Int`,
  `Bool`, and `Float`; and
- arbitrarily long lists of `Str` values.

The prompt's no-duplicate premise is not needed by either the implementation or
the proof, so the theorem is stronger in that dimension.

This is a partial-correctness result under the supplied semantics. The final
`KPROVE_PASSED` runner marker records successful positive proof execution and
is separate from this `VALIDATED` proof-quality judgment.

## Formal claims

`SPEC.can-arrange-loop` is the loop circularity. It starts at the exact
`#loop(list(VS), Name("value"), BODY)` term reached by the fixed `For`
semantics, with the exact one-element `Return` statement-list continuation,
function frame, bindings, empty heap, stack, exception, and return cells. Its
precondition is:

```k
I >=Int 0 andBool scanDefined(VS, I, P)
```

It consumes the entire symbolic suffix and changes `index` from `A` to
`arrangeSeq(VS, I, P, A)`. Final values of the internal locals `i`,
`previous`, and `value` are existentially abstracted because the immediately
following fixed `Return/#pop` removes that callee scope; none is observable or
used to compute the returned value after the loop.

`SPEC.can-arrange` starts from the initial MPY configuration, loads the exact
translated `FuncDef`, resolves and calls `can_arrange`, executes its body under
the fixed semantics, and reaches:

```k
arrangeSeq(VS, 0, 0, -1)
```

The structural equations for `arrangeSeq` scan indices in increasing order and
replace the accumulator with the current index exactly when `orderGe` is
false. Therefore its final accumulator is the largest qualifying index, or the
initial `-1` if no replacement occurs.

`check_program_identity.py` normalizes only explicit empty `.Stmts` markers and
checks that the regenerated `solution.mpy` `Module` term occurs in `spec.k`.
The clean run reported `program_identity=match`.

## Proof-extension inventory

### `isNumericVal` and `orderablePair`

- **Class:** definitional summaries.
- **Semantic role:** classify values; they do not replace execution.
- **Domain:** all `Val` values and all `Val × Val` pairs.
- **Matched context / justification scope:** pure function terms in any
  context. `isNumericVal` is exactly `isInt or isBool or isFloat`;
  `orderablePair` is exactly numeric×numeric or string×string.
- **State footprint:** none.
- **Value influence:** `scanDefined` preconditions and the `applyCmp` bridge
  guard.
- **Coverage/overlap:** one total equation per symbol; no overlapping cases.
- **Dependents:** both target claims and the guarded comparison bridge.

### `scanDefined`

- **Class:** definitional summary.
- **Semantic role:** names the comparison-defined input domain; it does not
  replace program execution.
- **Domain:** all `ValSeq × Int × Val`.
- **Matched context:** pure terms only.
- **Equations:** empty sequence → `true`; nonempty with `I == 0` skips the
  unrestricted first value and descends; nonempty with `I > 0` requires
  `orderablePair` and descends; nonempty with `I < 0` → `false`.
- **Coverage/overlap/descent:** empty/nonempty and `< 0`, `== 0`, `> 0`
  partition the full domain. Every recursive equation consumes one `vCons`.
- **State footprint:** none.
- **Value influence:** theorem applicability only.
- **Dependents:** loop and entry preconditions.

### `orderGe`

- **Class:** definitional summary, result-bearing.
- **Semantic role:** presents the fixed semantics' `>=` value for dynamic
  operands.
- **Domain:** all `Val × Val`. Ten disjoint orderable cases cover Int/Bool/Float
  combinations and Str×Str. A guarded fallback returns `false` only when
  `orderablePair` is false.
- **Matched context:** pure function terms in any context.
- **State footprint:** none.
- **Value influence:** comparison branch, `index`, returned result, and
  `arrangeSeq`.
- **Value justification:** the ten claims in `connection-spec.k`, compiled
  against `VERIFICATION-BASE`, prove each case against fixed `MPY` rules without
  importing the bridge. The definitions use the exact fixed symbols
  `boolAsInt`, `floatLt`, `ltIF`, `ltFI`, and `strLt`.
- **Coverage/overlap:** the ten static sort pairs are disjoint and collectively
  equal `orderablePair`; the fallback guard is their complement.
- **Dependents:** the bridge, `arrangeSeq`, and both target claims.
- **Value validation:** the bridge-free opposite interpretation
  `2 >= 1 => false` is rejected with residual `true`.

### `arrangeSeq`

- **Class:** definitional summary, result-bearing.
- **Semantic role:** names the mathematical result of scanning the remaining
  suffix; it never rewrites a program term.
- **Domain:** all `ValSeq × Int × Val × Int`.
- **Matched context:** pure summary terms.
- **Equations:** empty returns the accumulator; `I == 0` consumes the first
  value without comparing; `I > 0` consumes one value and either records `I` or
  preserves the accumulator according to total `orderGe`; `I < 0` totalizes the
  off-domain case by returning the accumulator.
- **Coverage/overlap/descent:** guards partition integers, `orderGe` is Boolean,
  and every recursive case consumes one constructor.
- **State footprint:** none.
- **Value influence:** exact returned postcondition.
- **Justification:** its one-step equations are matched by the fixed loop body;
  `SPEC.can-arrange-loop` machine-checks the base and inductive obligations.
- **Dependents:** the loop and entry claims.

### Guarded `applyCmp(">=", V, W) => orderGe(V, W)`

- **Class:** operational bridge and result-bearing abstraction.
- **Semantic role:** refines the fixed dynamic comparison dispatch after both
  operands have already evaluated to `Val`.
- **Complete match domain:** every pure `applyCmp(">=", V, W)` subterm for
  which `orderablePair(V, W)` is true.
- **Matched context:** arbitrary pure term context. It does not match
  `Compare`, name lookup, operand evaluation, a continuation, or any cell.
- **Justification scope / containment:** `connection-spec.k` partitions the
  complete guard into the ten possible static sort pairs and proves equality
  using `connection-kompiled`, whose main module is `VERIFICATION-BASE` and
  therefore excludes this bridge. Because `applyCmp` is a pure fixed-semantics
  function with no cell access, those universal equations are
  context-independent.
- **State footprint:** reads/writes/abstracts no cells; changes no control,
  binding, evaluation order, exception, heap, stack, return, or output state.
- **Value influence:** selects the loop branch and therefore the returned
  index.
- **Value justification:** ten bridge-free universal connection claims plus
  the rejected opposite ground interpretation.
- **Dependents:** `SPEC.can-arrange-loop` and `SPEC.can-arrange`.
- **Control validation:** no control is displaced. LLVM execution exercises
  the original comparison semantics; the bridge only simplifies the resulting
  pure function term during proof.

### `SPEC.can-arrange-loop`

- **Class:** derived lemma / reachability circularity.
- **Semantic role:** executes the exact fixed loop body and summarizes its
  final `index`.
- **Matched context:** exact `#loop`, target name, body, return statement-list
  continuation, environment `1`, module and callee scopes, `scopeLoc 2`, empty
  heap, empty heap allocation counter, one exact call frame, `noRet`, `NoExc`,
  and exit code `0`.
- **State footprint:** reads and writes only the callee bindings used by the
  body. It preserves the input binding and every externally observable cell.
  The three non-result locals are explicitly abstracted only after all loop
  execution is complete.
- **Justification:** proved as a claim by the target `kprove` command.
- **Dependents:** whole-program claim.

## Exact commands and actual results

The complete reproducible command sequence is in `prove.sh`. The final clean
run was:

```bash
./prove.sh
```

It exited `0`.

Program generation and identity:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 check_program_identity.py
sha256sum solution.py solution.mpy
```

Actual output:

```text
program_identity=match
55fb363850438b52bf46ffbd52032faa378fc7e45e30058cc8facc809acc27a5  solution.py
9f1d45640db47460fac203bcb1f5997bc227f4812afe0fbffb26332c4df1329d  solution.mpy
```

Concrete LLVM semantics:

```bash
python3 py2mpy.py smoke.py > smoke.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Both commands exited `0`; `krun` ended with `<k> .K </k>`, `NoExc`, and exit
code `0`. The compiler emitted supplied-semantics exhaustiveness/unused-variable
warnings; none was a stuck execution.

Bridge-free connection proof:

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-SPEC
```

Actual result: `#Top`, exit `0`. The ten claims emitted
`WarnTrivialClaim` because fixed `applyCmp` and `orderGe` simplified to the same
term before a reachability step; the bridge is absent from this definition.

Positive target proof:

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

Actual result: `#Top`, exit `0`. This single positive target command proves both
the loop circularity and the whole-program claim.

Independent differential test:

```bash
python3 differential_test.py
```

Actual output:

```text
cases=5970 mismatches=0
```

The oracle scans from right to left and returns the first qualifying index,
rather than reusing the forward accumulator or K summary equations. The sample
contains both prompt examples, boundaries, all distinct permutations of seven
integers through length five, deterministic mixed numeric arrays, strings,
infinities, and a NaN witness.

Negative validation probes:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY

kprove body-mutation-spec.k \
  --definition verification-kompiled \
  --spec-module BODY-MUTATION-SPEC

kprove connection-negative-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-NEGATIVE-SPEC
```

Each exited `1` with `WarnStuckClaimState`, as expected:

- false result probe: residual `<k> -1 ~> .K </k>` instead of `0`;
- body mutation (`return 0`): residual `<k> 0 ~> .K </k>` instead of `-1`;
- opposite comparison interpretation: residual `<k> true ~> .K </k>` instead
  of `false`.

Complete logs are under `evidence/`.

## Gate results

### Gate A — PASS

- **A1:** the exact translated function is embedded in the whole-program claim,
  loaded, bound, called, and executed by fixed semantics. The identity check
  passes. The material `return 0` body mutation is rejected.
- **A2:** no program state transition is skipped. The sole bridge is a pure
  comparison function equation with an empty state footprint.
- **A3:** fixed `Compare` semantics performs lookup and left-to-right operand
  evaluation before producing `applyCmp`; the bridge only matches evaluated
  `Val` operands. Ten bridge-free connection claims cover its complete guard.
- **A4:** all proof-local total functions have complete, terminating,
  pairwise-consistent equations. The earlier off-domain totality gap in
  `arrangeSeq` was removed before this report.
- **A5:** the empty list is a realizable precondition witness. The false result
  and opposite comparison interpretations are both rejected.

### Gate B — PASS

- **B1:** the theorem is unbounded over the full list structure represented by
  the supplied semantics wherever the program's performed `>=` operations are
  defined. It covers all modeled numeric and string element classes and
  arbitrary singleton values. It imposes no finite length bound and does not
  strengthen the no-duplicate premise.
- **B2:** CPython value classes/orderings absent from the fixed model are a
  recorded model boundary, not a candidate-imposed bound. These include custom
  objects and lexicographic/subset orderings of nested lists, tuples, and sets.
  The supplied semantics represents those container values but does not define
  their `>=` dispatch. Multi-element inputs with genuinely undefined CPython
  comparisons (for example `None >= None`) are contract-inherent exceptional
  cases rather than return-producing inputs.
- **B3:** `arrangeSeq` definitionally scans increasing indices and retains the
  latest match; the loop circularity formally connects that summary to fixed
  execution. The independent reverse oracle supplies additional intent
  evidence.
- **B4:** the implementation uses the contract's literal `not >=` predicate,
  including its behavior on unordered float values, rather than assuming `<`
  is equivalent.

### Gate C — PASS

Every command, mutation, result, and test scope above has an existing artifact
and log. Formal facts, model-conditional conclusions, finite evidence, and
excluded behavior are separated explicitly.

## Trust boundary

| Component | Status and influence | Dependents | Evidence |
|---|---|---|---|
| Supplied `MPY` operational semantics | Fixed trusted foundation; controls binding, calls, iteration, comparisons, and return state | All claims | LLVM smoke run and exact imports |
| `floatLt`, `ltIF`, `ltFI` | Supplied opaque/`[concrete]` float primitives; their Boolean values can affect the returned index | Float cases of `orderGe`, target claims | Bridge-free symbolic connection to the fixed symbols, concrete mixed-float LLVM cases, CPython differential cases |
| Float edge fidelity | Conditional on the supplied primitive contract. This report does not assert independently proved IEEE-754 equivalence for every NaN, signed-zero, infinity, or rounding edge | Float-input adequacy | Finite infinity/NaN differential witnesses only |
| `strLt` and string representation | Supplied code-sequence model; symbolic theorem uses that model's lexicographic equations | String case of `orderGe` | Bridge-free string connection claim and LLVM/differential string cases |
| K/Haskell backend and SMT solver | Trusted proof engine and arithmetic reasoning | All machine-checked claims | K v7.1.293 command outputs |

The guarded comparison bridge is not a trust assumption: its complete
orderable domain is connected to fixed semantics by `connection-spec.k`.

## Excluded or conditional behavior

- The source task's material container is a finite Python list. Tuple, string,
  iterator, and arbitrary user-object arguments are not claimed as alternative
  `arr` container types.
- Adjacent value pairs for which CPython raises `TypeError` do not have a
  return-value obligation.
- CPython-supported orderings not modeled by the supplied semantics (notably
  nested list/tuple lexicographic comparison, set inclusion comparison, custom
  `__ge__`, and Unicode/model differences) remain explicit language-model
  boundaries.
- Termination and resource bounds are not claimed beyond K reachability
  partial correctness, although the implementation consumes one finite list
  element per iteration.
