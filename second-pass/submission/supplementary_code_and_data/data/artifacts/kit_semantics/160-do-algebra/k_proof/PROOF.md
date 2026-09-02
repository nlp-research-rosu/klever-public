VALIDATED

## What is proven

Under the supplied MPY semantics, the exact `do_algebra` body in
`solution.mpy` has the following partial-correctness property for every finite
input satisfying the HumanEval contract:

- `operator` is a nonempty list whose elements are exactly `"+"`, `"-"`,
  `"*"`, `"//"`, or `"**"`;
- `operand` is a list of non-negative integers;
- `len(operand) == len(operator) + 1`.

The function constructs the token string

```text
operand[0] operator[0] operand[1] ... operator[n-1] operand[n]
```

and returns the fixed semantics' `evalArith` value for that string.  The
supplied evaluator defines Python's relevant precedence levels and
right-associative exponentiation.  This is an unbounded structural theorem
over arbitrary finite `ValSeq` values, not a bounded unrolling or a finite set
of list sizes.

The proof is partial correctness.  If evaluation has no normal value (most
notably floor division by zero), it does not assert a returned integer.

## Formal claims

`spec.k` contains:

1. `SPEC.algebra-loop`, a circularity over arbitrary symbolic
   `NUMBERS:ValSeq` and `OPERATIONS:ValSeq`.  Its precondition
   `validAlgebraLists(NUMBERS, OPERATIONS)` describes the remaining paired
   input, including the appended empty final operator.  It proves the exact
   recursive string accumulator `runPairCodes` and the final loop bindings.
2. `SPEC.do-algebra`, the target claim.  It begins at the default module
   configuration, executes the exact translated function definition, resolves
   and invokes `do_algebra`, executes the loop and return/pop behavior, and
   stores the result in module variable `answer`.  It also constrains the final
   scopes, two heap allocations, heap location, stack, return state, exception
   state, and exit code.

The target precondition is:

```k
validAlgebraLists(
  OPERANDS,
  valSeqConcat(OPERATORS, vCons(str(.IntSeq), .ValSeq)))
andBool notBool (OPERATORS ==K .ValSeq)
```

The result is:

```k
evalArith(
  runPairCodes(
    .IntSeq,
    OPERANDS,
    valSeqConcat(OPERATORS, vCons(str(.IntSeq), .ValSeq))))
```

`validAlgebraLists` and `validAlgebraRest` recursively enforce all element
types, non-negativity, allowed operators, equal paired lengths after appending
`""`, and the unique final empty operator.  The separate nonempty condition
gives at least one source operator and therefore at least two operands.

## Proof-extension inventory

No proof-local rule intercepts a K control term, function invocation, loop,
return, frame, exception, heap update, or program-defined operation.  All
program statements execute under the fixed MPY rules.

### Dynamic-sort projections

| Extension | Class and semantic role | Domain and context | State/value justification | Dependents and validation |
|---|---|---|---|---|
| `definedProjectInt`, `definedProjectStr` | Definitional summaries; do not replace execution | Any `Val`; exact equations are fixed `isInt` and `isStrV` membership | Read no cells and define only the guard for the matching fixed subsort | The projection and dispatch rules; constructor cases, concrete MPY runs, and the complete proof |
| `projectIntTotal`, `projectStrTotal`; their `#Ceil` characterizations, cast orientations, and collapse rules | Derived guarded total-projection lemmas | Only where the corresponding membership predicate is true; no K continuation or cell is matched | The partial cast `{V}:>Int` or `{V}:>Str` fixes the value. Collapse and cast orientation agree on overlaps. Outside the guard the no-evaluator symbols remain opaque and are not used by a claim | `runPairCodes`, validity predicates, and dispatch twins; exercised over every symbolic list head by `SPEC.algebra-loop` |
| `codesOf`, `codesProject` | Definitional summaries | `codesOf` covers the sole `Str` constructor; `codesProject` composes it with the guarded string projection | Exact character-code sequence of the projected fixed-semantics string; no state or control effects | String-concatenation twin and `runPairCodes`; concrete and differential witnesses include all five operators |

The `#Ceil` and orientation rules are the guarded total-projection idiom: the
match domain is exactly the fixed partial-cast domain.  The rules have no
continuation, stack, environment, heap, return, or exception context and
therefore cannot discard or reorder execution.

### Guarded dispatch twins

| Extension | Class and semantic role | Complete match/guard | Fixed-rule equivalence and footprint | Dependents and validation |
|---|---|---|---|---|
| `applyBuiltin("str", V, .Vals)` simplification | Derived dispatch lemma | Exact builtin name, one positional value, no remaining arguments, and `definedProjectInt(V)` | Restates fixed `applyBuiltin("str", I:Int, .Vals)` with the exact guarded cast. It reads/writes no cells and has no control effect | Loop claim and target; projection connection, LLVM tests, 500 differential cases |
| `applyBin("+", str(A), V)` simplification | Derived dispatch lemma | Exact `"+"`, statically string left operand, and `definedProjectStr(V)` | Restates fixed string `applyBin("+", str(A), str(B))`; `codesProject(V)` is the exact cast string's codes. It reads/writes no cells and has no control effect | Loop claim and target; projection connection, all operator witnesses, mutation probes |

When either twin overlaps the original statically sorted MPY equation, the
projection collapse rule makes both right-hand sides identical.  Their guards
are neither weaker nor broader than the fixed rule's subsort match.

### Domain and result summaries

| Extension | Class | Coverage, overlap, and descent | Meaning and dependents |
|---|---|---|---|
| `allowedOperator` | Definitional summary | One total Boolean equation; exact disjunction of the five encoded strings | Formalizes the prompt's operator domain |
| `validAlgebraLists`, `validAlgebraRest` | Definitional summaries | Constructor case plus disjoint `owise` fallbacks; recursive calls consume one pair | Formalizes all finite valid input pairs and exposes the dynamic Int/Str guards |
| `runPairCodes` | Definitional summary | Empty-left, empty-right, and cons/cons cases cover zip truncation; recursive case consumes one pair | Exact recurrence of `expression += str(oprn) + oprt`; target postcondition and loop invariant |
| `lastPairValue` and its guarded simplification | Definitional summary / derived folding lemma | Singleton base; recursive fold only when the tail is itself valid; `owise` covers invalid shapes; recursion consumes one pair | Exact final `oprn` binding in the loop claim |
| `SPEC.algebra-loop` | Derived reachability circularity | Exact loop term and exact real invocation scopes; arbitrary valid finite tails | Fixed MPY iteration, tuple binding, lookup, calls, concatenation, assignment, and loop control execute. It is the machine-checked base/step invariant used by the target |

All equations are structurally descending or nonrecursive.  Guarded overlaps
agree, and all total functions have constructor/`owise` coverage or are the
explicit guarded no-evaluator projections described above.

## Reproducible commands and actual outputs

The complete recorded runner is:

```bash
./prove.sh
```

Actual final result: exit `0`.

The key commands inside it are:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled
```

Actual results: both generation commands exited `0`; LLVM compilation exited
`0` with only supplied-semantics exhaustiveness/unused-variable warnings.
`krun` exited `0` with final `<k> .K </k>`, `<env> 0 </env>`,
`<stack> .List </stack>`, `<ret> noRet </ret>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`.  The smoke artifact contains four assertions,
including precedence, right-associative exponentiation, and floor division.

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.algebra-loop

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual results: Haskell compilation exited `0` with only the supplied
`str.k` unused-variable warnings.  The focused loop proof printed `#Top` and
exited `0`.  The complete proof, with the loop circularity active for the
target claim, printed `#Top` and exited `0`.

```bash
python3 test_solution.py
```

Actual output and exit:

```text
tested=500 skipped_zero_division=46 mismatches=0
Exit: 0
```

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit `1`, `WarnStuckClaimState`; the residual completed with
`answer |-> 9` while the mutation demanded `10`.

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit `1`, `WarnStuckClaimState`; changing the initial expression
from `""` to `"1"` completed with `answer |-> 19` while the original property
demanded `9`.

## Gate results

### Gate A — PASS

- A1: The target starts with the exact `FuncDef` AST appearing in
  `solution.mpy`, performs module binding and name lookup, calls that closure,
  and executes every program-defined statement.  There is no program-body
  oracle or invocation shortcut.  The body mutation is rejected and changes
  the concrete result from `9` to `19`.
- A2: The target constrains the observable result and exact final module
  scopes, heap allocations, heap location, stack, return state, exception
  state, and exit code.  The loop invariant preserves all framed cells and
  changes only the three actual loop locals.
- A3: Fixed MPY rules perform callee/argument evaluation, tuple binding,
  lookup, left-to-right binary evaluation, return, and frame pop.  The two
  dynamic dispatch lemmas have exact fixed-rule guards and no control context.
- A4: Projection values are connected to fixed partial casts; summary
  equations are guarded, constructor-covering, and descending.  No
  inconsistent or result-postulating equation was found.
- A5: The prompt example is a realizable witness.  The false result `10` is
  rejected with actual result `9`.

### Gate B — PASS

The formal precondition covers arbitrary finite lists across the full material
HumanEval domain: every permitted length, every non-negative K integer, and
all five allowed operator strings.  It imposes no finite size bound.  The
result summary is connected to fixed execution by the loop claim, and the
human-facing evaluation is the supplied, defined `evalArith` operation.

Division-by-zero inputs are not silently narrowed out.  They lie in the
structural domain, but the theorem is partial correctness and asserts no
normal integer result where the specified evaluation is undefined.  CPython's
`ZeroDivisionError` object is outside this reference semantics' exception
model; this boundary does not omit any normally returning contract case.

### Gate C — PASS

Every proof-local symbol and rule is inventoried above.  All cited artifacts
exist, `prove.sh` reproduces the commands, positive and negative exit statuses
were checked, and empirical evidence is labeled finite rather than universal.

## Trust boundary

- The supplied read-only MPY semantics, including `evalArith`, Python integer
  string conversion, K integer arithmetic hooks, list/zip behavior, and
  function-frame machinery, is the fixed semantic trust base.
- The K compiler, Haskell prover/backend, LLVM backend, and SMT/term-rewriting
  implementation are trusted tooling.
- The reference semantics models unbounded mathematical integers, which agrees
  with the material Python integer behavior here.
- It does not model CPython's `ZeroDivisionError` object/trace for `// 0`.
  The theorem is conditional on normal termination and does not substitute a
  return value for that case.
- There are no proof-local trusted primitives, result-bearing oracles, or
  operational bridges.

## Empirically supported facts

- `smoke.py`/`smoke.mpy` checks four concrete programs under LLVM:
  the prompt example gives `9`; `2 ** 3 ** 2` gives `512`; `7 // 3 + 1`
  gives `3`; and `10 - 2 * 3` gives `4`.
- `test_solution.py` uses an independently written Python expression builder
  and CPython `eval` as the oracle.  A deterministic sample of 500 normally
  evaluating inputs of one to three operators had zero mismatches.  Forty-six
  generated division-by-zero inputs were recorded and skipped rather than
  assigned a fabricated value.
- These finite tests support implementation-to-intent alignment; the
  universal result comes from `kprove`, not from testing.

## Excluded behavior

Inputs with an empty operator list, unequal list lengths, negative or
non-integer operands, or operator strings outside the five named operations
are outside the source contract and formal precondition.  Exceptional behavior
and termination are not claimed beyond the fixed semantics and the
partial-correctness boundary described above.
